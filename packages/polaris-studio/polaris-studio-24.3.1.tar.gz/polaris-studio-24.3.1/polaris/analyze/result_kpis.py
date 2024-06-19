import logging
import traceback
from pathlib import Path
from shutil import rmtree

import diskcache as dc  # type: ignore
import numpy as np
import pandas as pd
from polaris.demand.demand import Demand
from polaris.runs.calibrate import activity_generation, destination_choice, mode_choice, timing_choice
from polaris.runs.calibrate.utils import calculate_rmse
from polaris.runs.convergence.convergence_config import ConvergenceConfig
from polaris.runs.convergence.convergence_iteration import ConvergenceIteration
from polaris.runs.gap_reporting import load_gaps
from polaris.runs.polaris_inputs import PolarisInputs
from polaris.runs.results.h5_results import H5_Results
from polaris.runs.scenario_compression import ScenarioCompression
from polaris.runs.summary import load_summary
from polaris.runs.wtf_runner import render_wtf_file, render_sql, sql_dir
from polaris.utils.database.db_utils import (
    attach_to_conn,
    commit_and_close,
    has_table,
    read_and_close,
    safe_connect,
)
from polaris.utils.database.standard_database import DatabaseType
from polaris.utils.dict_utils import denest_dict
from polaris.utils.optional_deps import check_dependency


class ResultKPIs:
    """
    This class provides an easy way to extract relevant metrics for a single simulation run of POLARIS.
    The easiest way to generate an instance is via the factory method `from_iteration` which takes the path to the
    outputs of a simulation run (or a :func:`~Polaris.runs.convergence.ConvergenceIteration`)

    ::

        from polaris.analyze.result_kpi import ResultKPIs

        kpis = ResultKPIs.from_iteration(ref_project_dir / f"{city}_iteration_2")

    Metric comparison plots can then be generated in a notebook using:

    ::

        results = KpiComparator()
        results.add_run(kpis, 'an-artitrary-label')
        results.plot_mode_share()
        results.plot_vmt()
        results.plot_vmt_by_link_type()

    Any number of runs can be added using `add_run` up to the limit of readability on the generated plots.
    """

    result_time_step = 3600

    def __init__(self, inputs: PolarisInputs, cache_file: Path, population_scale_factor: float):
        self.cache = self._load_cache(cache_file)
        self.inputs = inputs
        self.population_scale_factor = population_scale_factor

    @classmethod
    def from_iteration(cls, iteration: ConvergenceIteration, **kwargs):
        """Create a KPI object from a ConvergenceIteration object."""
        if iteration.output_dir is None or iteration.files is None:
            raise RuntimeError("Given iteration doesn't have a defined output dir")
        return cls.from_args(iteration.files, iteration.output_dir, **kwargs)

    @classmethod
    def from_dir(cls, iteration_dir: Path, **kwargs):
        """Create a KPI object from a given directory."""
        if "db_name" in kwargs:
            inputs = PolarisInputs.from_dir(iteration_dir, db_name=kwargs["db_name"])
            del kwargs["db_name"]
        else:
            inputs = PolarisInputs.from_dir(iteration_dir)
        return cls.from_args(inputs, iteration_dir, **kwargs)

    @classmethod
    def from_args(
        cls,
        files: PolarisInputs,
        iteration_dir: Path,
        cache_name: str = "kpi.cache",
        clear_cache=False,
        exit_if_no_cache=False,
        population_scale_factor=None,
    ):
        cache_file = Path(iteration_dir) / cache_name
        if cache_file.exists() and clear_cache:
            rmtree(cache_file)

        if population_scale_factor is None:
            population_scale_factor = ConvergenceConfig.from_dir(iteration_dir).population_scale_factor

        if not cache_file.exists() and exit_if_no_cache:
            return None

        return cls(files, cache_file, population_scale_factor)

    def _load_cache(self, cache_dir) -> dc.Cache:
        if cache_dir is None:
            return None

        # make sure we never leave open connections to the cache lying around
        def create_and_close(cache_dir_):
            c = dc.Cache(cache_dir_)
            c.close()
            return c

        try:
            return create_and_close(cache_dir)
        except Exception:
            (Path(cache_dir) / "cache.db").unlink(missing_ok=True)
            return create_and_close(cache_dir)

    def cache_all_available_metrics(self, verbose=True, metrics_to_cache=None):
        if metrics_to_cache is None:
            metrics_to_cache = self.available_metrics()
        for m in metrics_to_cache:
            try:
                self.get_cached_kpi_value(m)
            except Exception:
                logging.warning(f"failed: {m}")
                if verbose:
                    tb = traceback.format_exc()
                    print(tb, flush=True)
        self.cache.close()

    @classmethod
    def available_metrics(self):
        return [e.replace("metric_", "") for e in dir(self) if e.startswith("metric_")]

    def close(self):
        self.cache.close()

    def get_kpi_value(self, kpi_name):
        attr_name = f"metric_{kpi_name}"
        if hasattr(self, attr_name) and callable(self.__getattribute__(attr_name)):
            return self.__getattribute__(attr_name)()
        raise RuntimeError(f"it seems we don't have a way to compute: {kpi_name}")

    def get_cached_kpi_value(self, kpi_name, skip_cache=False, force_cache=False):
        try:
            if self.cache is None:
                return self.get_kpi_value(kpi_name)

            def generate():
                logging.debug(f"Generating KPI value {kpi_name}")
                self.cache.set(kpi_name, self.get_kpi_value(kpi_name))

            if skip_cache:
                generate()
            elif kpi_name not in self.cache:
                if force_cache:
                    return None
                generate()

            return self.cache.get(kpi_name)
        finally:
            # Any time we read or write to the cache - we need to close it!
            self.cache.close()

    def has_cached_kpi(self, kpi_name):
        try:
            return self.cache is not None and kpi_name in self.cache
        finally:
            # Any time we read or write to the cache - we need to close it!
            self.cache.close()

    def cached_metrics(self):
        try:
            return set() if self.cache is None else set(self.cache.iterkeys())
        finally:
            # Any time we read or write to the cache - we need to close it!
            self.cache.close()

    def metric_summary(self):
        return load_summary(self.inputs.summary, raise_on_error=False)

    def metric_gaps(self):
        return load_gaps(self.inputs.gap)

    @staticmethod
    def one_value(conn, query, default=0):
        return conn.execute(query).fetchone()[0] or default

    def metric_population(self):
        columns = ["num_persons", "num_employed", "num_hh"]
        where_clauses = ["1==1", "person.age > 16", "work_location_id > 1"]
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            vals = [ResultKPIs.one_value(conn, f"SELECT count(*) FROM person WHERE {w};") for w in where_clauses]
            return pd.DataFrame([vals], columns=columns)

    def metric_num_adults(self):
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return ResultKPIs.one_value(conn, "SELECT count(*) FROM person WHERE person.age > 16;")

    def metric_num_employed(self):
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return ResultKPIs.one_value(conn, "SELECT count(*) FROM person WHERE work_location_id > 1;")

    def metric_num_persons_by_age_band_5(self):
        return self._metric_num_persons_by_age_band_x(5)

    def metric_num_persons_by_age_band_10(self):
        return self._metric_num_persons_by_age_band_x(10)

    def _metric_num_persons_by_age_band_x(self, x):
        query = f""" SELECT {x} * (person.age / {x}) as bucket, count(*)
                     FROM person
                     GROUP BY (person.age / {x}); """
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return pd.read_sql(query, conn)

    def metric_num_hh(self):
        query = """ SELECT count(*) as num_hh FROM household;"""
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return conn.execute(query).fetchone()[0] or 0

    def metric_num_hh_by_hh_size(self):
        query = """ SELECT q.hh_size, count(*) as num_hh
                     FROM (SELECT person.household, count(*) as hh_size
                           FROM person
                           GROUP BY person.household) as q
                     GROUP BY q.hh_size;"""
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return pd.read_sql(query, conn)

    def metric_tts(self):
        # If Trip table is empty we return 0 as the execute.fetchone()[0] will return None
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return conn.execute('SELECT SUM(end-start) from trip WHERE "end">"start"').fetchone()[0] or 0

    def metric_distance_by_act_type(self):
        query = """ SELECT activity.type as acttype, avg(trip.travel_distance)/1609.3 as dist_avg
                    FROM trip
                    JOIN person ON trip.person = person.person
                    JOIN household ON person.household = household.household
                    JOIN activity ON activity.trip = trip.trip_id
                    WHERE person.age > 16
                      AND trip.end - trip.start > 0
                      AND trip.end - trip.start < 10800
                    GROUP BY ACTTYPE; """
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return pd.read_sql(query, conn)

    def metric_planned_modes(self):
        query = """Select activity.mode, count(*) as mode_count
                   FROM activity JOIN person ON activity.person = person.person
                   WHERE activity.start_time > 122 and activity.trip = 0 and person.age > 16
                   GROUP BY activity.mode"""
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return pd.read_sql(query, conn)

    def metric_executed_modes(self):
        query = """Select activity.mode, count(*) as mode_count
                   FROM activity JOIN person ON activity.person = person.person
                   WHERE activity.start_time > 122 and activity.trip <> 0 and person.age > 16
                   GROUP BY activity.mode"""
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return pd.read_sql(query, conn)

    def metric_mode_shares(self):
        sql = render_wtf_file(sql_dir / "mode_share.template.sql", self.population_scale_factor)
        df = self._add_mode_names(self._slow_fast(sql, "mode_distribution_adult"))

        cols = ["HBW", "HBO", "NHB", "total"]
        df[[f"{c}_pr" for c in cols]] = df[cols] / df[cols].sum()
        return df

    def _add_mode_names(self, df):
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            mode_lookup = Demand.load_modes(conn)
        df["mode"] = df["mode"].apply(lambda m: mode_lookup.get(m, f"{m}_Unknown"))
        return df

    def metric_executed_activity_mode_share_by_income(self):
        sql = """
            Select
                income_quintile_fn as INCOME_QUINTILE,
                sum (case when activity.mode in (transit_modes) then 1.0 else 0.0 end)/(count(*) + 0.0) as transit_share,
                sum (case when activity.mode in ('TAXI') then 1.0 else 0.0 end)/(count(*) + 0.0) as tnc_share,
                sum (case when activity.mode in ('SOV', 'HOV') then 1.0 else 0.0 end)/(count(*) + 0.0) as auto_share,
                sum (case when activity.mode in ('WALK', 'BIKE') then 1.0 else 0.0 end)/(count(*) + 0.0) as active_share,
                sum (case when activity.mode not in (transit_modes, 'TAXI', 'SOV', 'HOV', 'WALK', 'BIKE') then 1.0 else 0.0 end)/(count(*) + 0.0) as other_share
            FROM
                activity, person, trip, household
            WHERE
                activity.start_time > 122 and
                activity.trip = trip.trip_id and
                trip."end" - trip."start" > 2 and
                activity.person = person.person and
                person.household = household.household and
                activity.mode not like 'FAIL%'
            GROUP BY
                INCOME_QUINTILE;
        """
        return self._slow_fast(sql, "executed_activity_mode_share_by_income")

    def metric_activity_start_distribution(self):
        sql = render_wtf_file(sql_dir / "activity_start_distribution.template.sql", self.population_scale_factor)
        return self._slow_fast(sql, "Activity_Start_Distribution")

    def metric_activity_duration_distribution(self):
        sql = """
            SELECT
                type as act_type,
                cast(start_time/3600 as int) as start_time,
                avg(duration) as average_duration,
                scaling_factor * count(*) as num_activities
            FROM Activity
            WHERE start_time > 122 and trip <> 0
            GROUP BY 1,2;
        """
        return self._slow_fast(sql, "Activity_Duration_Distribution")

    def metric_vmt_vht(self):
        sql_slow = """
            SELECT mode,
                   scaling_factor*sum(travel_distance)/1609.3/1000000.0 as million_VMT,
                   scaling_factor*sum(end-start)/3600.0/1000000.0 as million_VHT,
                   sum(travel_distance)/1609.3 / (sum(end-start)/3600.0) as speed_mph,
                   scaling_factor*count(*) as count
            FROM trip
            WHERE "end" > "start"
            AND (
                    (mode IN (0,9) AND has_artificial_trip <> 1)  -- skip stuck auto trips
                 OR (mode NOT IN (0,9))                           -- non-auto modes
            )
            GROUP BY mode;
        """
        return self._add_mode_names(self._slow_fast(sql_slow, "vmt_vht_by_mode")).set_index("mode")

    def metric_ev_charging(self):
        sql = """
            SELECT
                "Location_Type",
                "is_tnc_vehicle",
                scaling_factor * sum("Energy_Out_Wh"- "Energy_In_Wh")/1000000.0 as total_energy_charged_MWh,
                scaling_factor * sum(Time_Start - Time_In)/3600.0 as total_wait_hours,
                scaling_factor * sum(Time_Out - Time_Start)/3600.0 as total_charge_hours,
                scaling_factor * sum(charged_money) as total_charged_dollars,
                scaling_factor * sum(case when "Energy_Out_Wh"- "Energy_In_Wh">0 then 1 else 0 end) as positive_charge_count,
                scaling_factor * count(*) as charge_count,
                sum("Energy_Out_Wh"- "Energy_In_Wh")/1000.0/sum(case when "Energy_Out_Wh"- "Energy_In_Wh">0 then 1 else 0 end) as average_energy_charged_kWh,
                sum(Time_Start - Time_In)/60.0/count(*) as average_wait_minutes,
                sum(Time_Out - Time_Start)/60.0/sum(case when "Energy_Out_Wh"- "Energy_In_Wh">0 then 1 else 0 end) as average_charge_minutes,
                sum(charged_money)/sum(case when "Energy_Out_Wh"- "Energy_In_Wh">0 then 1 else 0 end) as average_paid_dollars_per_event,
                sum(charged_money)*1000.0/sum("Energy_Out_Wh"- "Energy_In_Wh") as averaged_paid_dollars_per_kWh
            FROM "EV_Charging"
            group BY 1,2;
        """
        return self._slow_fast(sql, "ev_charge_summary_2")

    def metric_vmt_vht_by_link(self):
        h5_results = H5_Results(ScenarioCompression.maybe_extract(self.inputs.result_h5))

        scale_factor = 1.0 / self.population_scale_factor
        lengths = h5_results.get_vector("link_moe", "link_lengths") / 1609.3
        counts = h5_results.get_array("link_moe", "link_out_volume") * scale_factor
        travel_times = h5_results.get_array("link_moe", "link_travel_time") / 3600.0

        # Construct an aggregation matrix (num_timesteps x num_hours)
        new_num_steps = int(86400 / self.result_time_step)
        aggregation_vector = np.zeros((h5_results.num_timesteps, new_num_steps))
        ratio = int(h5_results.num_timesteps / new_num_steps)
        for u in range(new_num_steps):
            aggregation_vector[u * ratio : (u + 1) * ratio, u] = 1

        vht = pd.DataFrame((counts * travel_times).T @ aggregation_vector, columns=[f"vht_{i}" for i in range(0, 24)])
        vmt = pd.DataFrame((counts * lengths).T @ aggregation_vector, columns=[f"vmt_{i}" for i in range(0, 24)])
        vht["vht_daily"] = vht.sum(axis=1) / 1000000
        vmt["vmt_daily"] = vmt.sum(axis=1) / 1000000

        return pd.concat([self.load_link_types(), vht, vmt], axis=1)

    def load_link_types(self):
        with safe_connect(ScenarioCompression.maybe_extract(self.inputs.supply_db)) as conn:

            def sql(linknr, lanes):
                return f"""
                    SELECT {linknr},type,z.zone
                    FROM link l, node n, zone z
                    WHERE {lanes}
                    AND l.node_a = n.node AND n.zone = z.zone and l.type not in ('LIGHTRAIL', 'HEAVYRAIL', 'WALKWAY')
                    """

            linknr_ab, lanes_ab = "2*link     as linknr", "lanes_ab>0"
            linknr_ba, lanes_ba = "(2*link+1) as linknr", "lanes_ba>0"
            return pd.read_sql(f"{sql(linknr_ab, lanes_ab)} UNION {sql(linknr_ba, lanes_ba)} ORDER BY linknr", conn)

    def metric_activity_distances(self):
        sql = render_wtf_file(sql_dir / "travel_time.template.sql", self.population_scale_factor)
        return self._slow_fast(sql, "ttime_By_ACT_Average")

    def _slow_fast(self, slow_sql, table_name, db_type=DatabaseType.Demand, attach_db_type=None):
        """Utility method to read analytics data from table. Uses slow query to create it if table doesn't exist."""
        with commit_and_close(ScenarioCompression.maybe_extract(self._get_db(db_type))) as conn:
            if has_table(conn, table_name):
                return pd.read_sql(sql=f"SELECT * FROM {table_name};", con=conn)
            if attach_db_type is not None:
                attach_to_conn(conn, {"a": ScenarioCompression.maybe_extract(self._get_db(attach_db_type))})
            conn.execute(f"CREATE TABLE {table_name} AS {render_sql(slow_sql, self.population_scale_factor)}")
            return pd.read_sql(sql=f"SELECT * FROM {table_name};", con=conn)

    def _get_db(self, db_type: DatabaseType):
        if db_type == DatabaseType.Demand:
            return self.inputs.demand_db
        if db_type == DatabaseType.Supply:
            return self.inputs.supply_db
        if db_type == DatabaseType.Results:
            return self.inputs.result_db

    def metric_tnc_times_by_tnc_operator(self):
        sql_slow = """SELECT
                        tnc_operator,
                        service_mode,
                        avg(assignment_time-request_time)/60.0 as time_to_assign,
                        avg(pickup_time-request_time)/60.0 as wait,
                        avg(dropoff_time-pickup_time)/60.0 as ivtt,
                        count(*) as demand
                    FROM
                        "TNC_Request"
                    where
                        assigned_vehicle is not null
                    group by
                        tnc_operator,
                        service_mode;
        """
        return self._slow_fast(sql_slow, "tnc_times_by_tnc_operator")

    def metric_pmt_pht_by_tnc_mode(self):
        sql_slow = """SELECT service_mode, sum(distance) as pmt,
                             sum(dropoff_time-request_time)/3600 as pht,
                             count(*) as demand_unscaled
                      FROM TNC_Request
                      GROUP BY service_mode;
        """
        return self._slow_fast(sql_slow, "pmt_pht_by_tnc_mode")

    def metric_vmt_vht_by_tnc_mode(self):
        sql_slow = """SELECT
                        mode,
                        sum(travel_distance)/1609.34 as vmt,
                        sum(end-start)/3600 as vht
                      FROM TNC_Trip
                      WHERE "end">="start"
                      GROUP BY mode;
        """
        return self._slow_fast(sql_slow, "vmt_vht_by_tnc_mode")

    def metric_vmt_vht_by_tnc_operator(self):
        sql_slow = """SELECT
                        tnc_operator,
                        case
                            when final_status = -1 then 'PICKUP'
                            when final_status = -2 then 'DROPOFF'
                            when final_status = -4 then 'CHARGING'
                        end as status,
                        sum(travel_distance)/1609.34 as vmt,
                        sum(end-start)/3600 as vht
                    FROM TNC_Trip
                    WHERE "end">="start"
                    Group by
                        tnc_operator,
                        status;
        """
        return self._slow_fast(sql_slow, "vmt_vht_by_tnc_operator")

    def metric_empty_vmt_vht_by_tnc_operator(self):
        sql_slow = """SELECT
                        tnc_operator,
                        case
                            when passengers = 0 then 'UNOCCUPIED'
                            else 'OCCUPIED'
                        end as occupied_status,
                        sum(travel_distance)/1609.34 as vmt,
                        sum(end-start)/3600 as vht
                    FROM TNC_Trip
                    WHERE "end">="start"
                    Group by
                        tnc_operator,
                        occupied_status;
        """
        return self._slow_fast(sql_slow, "empty_vmt_vht_by_tnc_operator")

    def metric_tnc_result_db_by_tnc_operator(self):
        sql_slow = """SELECT
                        tnc_operator,
                        avg(tot_pickups) as avg_trips_served,
                        avg(charging_trips) as avg_charging_trips,
                        avg(revenue) as avg_revenue,
                        sum(revenue) as total_revenue_unscaled,
                        sum(trip_requests) as total_requests_offered_to_op
                    FROM TNC_Statistics
                    Group by
                        tnc_operator;
        """
        return self._slow_fast(sql_slow, "tnc_result_db_by_tnc_operator", DatabaseType.Results)

    def metric_avo_by_tnc_operator(self):
        sql_slow = """
                SELECT
                    tnc_operator,
                    'AVO_trips' as metric,
                    avg(passengers) as AVO
                FROM TNC_Trip
                GROUP by
                    tnc_operator
                UNION
                SELECT
                    tnc_operator,
                    'AVO_dist' as metric,
                    sum(passengers*1.0*travel_distance)/sum(travel_distance) as AVO
                FROM TNC_Trip
                GROUP by
                    tnc_operator
                UNION
                SELECT
                    tnc_operator,
                    'AVO_trips_revenue' as metric,
                    avg(passengers) as AVO
                FROM TNC_Trip
                WHERE passengers > 0
                GROUP by tnc_operator
                UNION
                SELECT
                    tnc_operator,
                    'AVO_dist_revenue' as metric,
                    sum(passengers*1.0*travel_distance)/sum(travel_distance) as AVO
                FROM TNC_Trip
                WHERE passengers > 0 and travel_distance > 0
                GROUP by
                    tnc_operator;
        """
        return self._slow_fast(sql_slow, "avo_by_tnc_operator", DatabaseType.Demand)

    def metric_road_pricing(self):
        sql = """
            SELECT SUM(toll) as total_revenue, AVG(toll) as avg_price,
                   AVG(travel_distance) avg_dist, COUNT(*) as total_trips_sov
            from trip where mode=0 and person is not null;
            """
        with read_and_close(ScenarioCompression.maybe_extract(self.inputs.demand_db)) as conn:
            return pd.read_sql(sql, con=conn)

    def metric_transit_boardings(self):
        sql_slow = """
            SELECT
                ta.agency as agency,
                transit_mode_fn as "mode",
                scaling_factor*sum(tvl.value_boardings) as boardings,
                scaling_factor*sum(tvl.value_alightings) as alightings
            FROM
                "Transit_Vehicle_links" tvl,
                transit_vehicle tv,
                a.transit_trips tt,
                a.transit_patterns tp,
                a.transit_routes tr,
                a.transit_agencies ta
            where
                tvl.value_transit_vehicle_trip = tv.transit_vehicle_trip and
                tvl.value_transit_vehicle_trip = tt.trip_id and
                tp.pattern_id = tt.pattern_id and
                tr.route_id = tp.route_id AND
                tr.agency_id = ta.agency_id
            group by
                ta.agency,
                tv.mode
            order by
                ta.agency,
                tv.mode desc
            ;
        """
        return self._slow_fast(sql_slow, "boardings_by_agency_mode", attach_db_type=DatabaseType.Supply)

    # def metric_mode_distribution()

    def metric_network_gaps_by_link_type(self):
        sql_slow = """
            select a.link.type as link_type,
                   SUM(ABS(value_travel_time-value_routed_travel_time))/SUM(value_routed_travel_time) as abs_gap,
                   SUM(value_travel_time-value_routed_travel_time)/SUM(value_routed_travel_time) as gap,
                   cast(SUM(a.link.length)/1609 as int) as total_dist
            from a.link, path_links
            where value_travel_time >=0 and a.link.link=value_link
            group by 1
        """
        return self._slow_fast(sql_slow, "network_gaps_by_link_type", attach_db_type=DatabaseType.Supply)

    def metric_network_gaps_by_hour(self):
        sql_slow = """
            select cast(value_entering_time/3600 as int) as hour,
                   SUM(ABS(value_travel_time-value_routed_travel_time))/SUM(value_routed_travel_time) as abs_gap,
                   SUM(value_travel_time-value_routed_travel_time)/SUM(value_routed_travel_time) as gap
            from  path_links
            where value_travel_time >=0
            group by 1
        """
        return self._slow_fast(sql_slow, "network_gaps_by_hour")

    def metric_skim_stats(self):
        check_dependency("openmatrix")
        from polaris.skims.highway.highway_skim import HighwaySkim
        from polaris.skims.transit.transit_skim import TransitSkim

        hwy_skim = HighwaySkim.from_file(self.inputs.highway_skim)
        pt_skim_file = self.inputs.transit_skim
        if not pt_skim_file.exists():
            logging.debug(f"Skipping Transit skim metrics as file ({pt_skim_file}) not found")
            pt_skim = None
        else:
            pt_skim = TransitSkim.from_file(pt_skim_file)

        def f(skims, mode, interval, metric):
            mat = skims.get_skims(metric=metric, mode=mode, interval=interval)
            isfinite_mask = np.isfinite(mat)
            return {
                "interval": interval,
                "metric": metric,
                "mode": mode,
                "min": np.nanmin(mat[(mat > 0) & isfinite_mask], initial=0),
                "max": np.nanmax(mat[isfinite_mask], initial=10000),
                "avg": np.nanmean(mat[isfinite_mask]),
                # "std": mat[isfinite_mask].std(initial=10000),
            }

        df = pd.DataFrame([f(hwy_skim, "Auto", i, j) for i in hwy_skim.intervals for j in ["time", "distance"]])
        if pt_skim is None:
            return df

        df_transit = pd.DataFrame(
            [f(pt_skim, m, i, j) for i in pt_skim.intervals for j in ["time"] for m in ["Bus", "Rail"]]
        )
        return pd.concat([df, df_transit])

    def metric_rmse_vs_observed(self):
        columns = ["RMSE_activity", "RMSE_mode", "RMSE_mode_boardings", "RMSE_destination", "RMSE_timing"]
        targets_dir = ConvergenceConfig.from_dir(self.files.demand_db.parent).calibration.target_csv_dir
        if not targets_dir.exists():
            logging.warn("No calibration targets found for calculating RMSE")
            return pd.DataFrame(data=[[-1, -1, -1, -1, -1]], columns=columns)

        simulated = activity_generation.load_simulated(self.inputs.demand_db, False)
        target = activity_generation.load_target(targets_dir / "activity_generation_targets.csv")
        rmse_activity = calculate_rmse(simulated, target)

        simulated = destination_choice.load_simulated(self.inputs.demand_db)
        target = destination_choice.load_target(targets_dir / "destination_choice_targets.csv")
        rmse_destination = calculate_rmse(simulated, target)

        simulated = mode_choice.load_simulated(self.inputs, self.population_scale_factor, False)
        target = mode_choice.load_targets(targets_dir / "mode_choice_targets.csv")
        rmse_mode = calculate_rmse(denest_dict(simulated), denest_dict(target))

        target_boardings = mode_choice.load_target_boardings(targets_dir / "mode_choice_boarding_targets.csv")
        simulated_boardings = mode_choice.load_simulated_boardings(self.inputs, self.population_scale_factor)
        rmse_boardings = calculate_rmse(simulated_boardings, target_boardings)

        simulated = timing_choice.load_simulated(self.inputs, self.population_scale_factor, False)
        target = timing_choice.load_target(targets_dir / "timing_choice_targets.csv")
        rmse_timing = calculate_rmse(denest_dict(simulated), denest_dict(target))

        return pd.DataFrame(
            data=[[rmse_activity, rmse_mode, rmse_boardings, rmse_destination, rmse_timing]], columns=columns
        )
