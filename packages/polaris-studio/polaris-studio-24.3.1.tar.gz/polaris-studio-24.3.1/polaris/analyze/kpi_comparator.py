# matplotlib 3.8 should have type hints, until then we just ignore
import logging
from re import Pattern
import traceback
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import seaborn as sns  # type: ignore
from matplotlib import pyplot as plt  # type: ignore
from polaris.analyze.result_kpis import ResultKPIs
from polaris.utils.pandas_utils import filter_df


class KpiComparator:
    """This class provides an easy way to group together multiple runs of POLARIS and compare their outputs. Runs KPIs are
    added along with a string based name which is used as the label for that run in any subsequent plots which are
    generated.

    ::

        from polaris.analyze.kpi_comparator import KpiComparator

        results = KpiComparator()
        results.add_run(ResultKPIs.from_iteration(ref_project_dir / f"{city}_iteration_2"), 'REF_iteration_2')
        results.add_run(ResultKPIs.from_iteration(eval_project_dir / f"{city}_iteration_2"), 'EVAL_iteration_2')

    Metric comparison plots can then be generated in a notebook using:

    ::

        results.plot_mode_share()
        results.plot_vmt()
        results.plot_vmt_by_link_type()

    Any number of runs can be added using `add_run` up to the limit of readability on the generated plots.

    The object can also be used to generate a set of csv files for input into Excel (if you really have to use Excel):

    ::

        results.dump_to_csvs(output_dir = "my_csv_dump_dir")
    """

    def __init__(self):
        self.runs = {}
        self.results = None

    def add_run(self, kpi: ResultKPIs, run_id: str):
        if kpi is None:
            return
        self.runs[run_id] = kpi

    def dump_to_csvs(self, output_dir, metrics_to_dump=None, result_processor=None, **kwargs):
        metrics = metrics_to_dump or ResultKPIs.available_metrics()
        metrics = set(metrics) - {"num_adults", "num_employed", "num_hh", "tts"}  # remove legacy scalar metrics
        for m in metrics:
            df = self._get_results(m, **kwargs)
            if result_processor:
                df = result_processor(df)
            if df is not None and isinstance(df, pd.DataFrame):
                df.to_csv(Path(output_dir) / f"{m}.csv")

        return metrics

    # We want our grid lines to sit behind our chart elements
    plt.rc("axes", axisbelow=True)

    def plot_everything(self, **kwargs):
        exclusions = ["plot_multiple_gaps", "plot_everything", "plot_multiple_vmt"]
        plot_methods = [e for e in dir(self) if e.startswith("plot_") and e not in exclusions]
        for p in plot_methods:
            if callable(self.__getattribute__(p)):
                fn = self.__getattribute__(p)
                fn(**kwargs)

    def plot_mode_share(self, **kwargs):
        df = self._get_results("mode_shares", **kwargs)
        df = df[~(df["mode"].str.contains("FAIL") | df["mode"].str.contains("NO_MOVE"))]
        if df is None or df.shape[0] == 0:
            logging.warning("There were no results for 'mode_shares'")
            return

        _, axes = plt.subplots(2, 2, figsize=(20, 10))

        def f(y, ax, title):
            sns.barplot(df, x="mode", y=y, hue="run_id", ax=ax)
            ax.set(title=title)
            ax.set_ylim([0, 0.90])
            KpiComparator._style_axes([ax], rotate_x_labels=False)

        f("total_pr", axes[0, 0], title="Total")
        f("HBW_pr", axes[1, 0], title="HBW")
        f("HBO_pr", axes[0, 1], title="HBO")
        f("NHB_pr", axes[1, 1], title="NHB")
        KpiComparator._style_axes(np.ravel(axes), rotate_x_labels=60)

    def plot_population(self, **kwargs):
        fig, ax = plt.subplots(figsize=(5, 5))
        _ = sns.barplot(ax=ax, data=self._get_results("population", **kwargs), x="run_id", y="num_persons")
        KpiComparator._style_axes([ax], rotate_x_labels=False)

    def plot_congestion_pricing(self, **kwargs):
        fig, ax = plt.subplots(figsize=(5, 5))
        p = sns.barplot(
            ax=ax,
            data=self._get_results("road_pricing", **kwargs),
            x="run_id",
            y="total_revenue",
        )
        p.set_title("Congestion Pricing Revenue")
        KpiComparator._style_axes([ax], rotate_x_labels=False)

    def plot_transit(self, **kwargs):
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        df = self._get_results("transit_boardings", **kwargs)
        df["mode-agency"] = df["mode"] + "-" + df["agency"]
        sns.barplot(data=df, x="mode-agency", y="boardings", hue="run_id", errorbar=None, ax=axes[0]).set_title(
            "Boardings"
        )
        sns.barplot(data=df, x="mode-agency", y="alightings", hue="run_id", errorbar=None, ax=axes[1]).set_title(
            "Alightings"
        )
        KpiComparator._style_axes(axes, rotate_x_labels=False)

    def plot_act_dist(self, act_type: Optional[str] = None, **kwargs):
        df = self._get_results("activity_distances", **kwargs)

        if act_type is not None:
            df = df[df["acttype"].str.upper() == act_type.upper()]
        if df is None or df.shape[0] == 0:
            logging.warning("There were no results for 'activity_distances'")
            return
        _, axes = plt.subplots(1, 3, figsize=(28, 5))
        sns.barplot(ax=axes[0], data=df, x="acttype", y="ttime_avg", hue="run_id")
        sns.barplot(ax=axes[1], data=df, x="acttype", y="dist_avg", hue="run_id")
        sns.barplot(ax=axes[2], data=df, x="acttype", y="count", hue="run_id")
        KpiComparator._style_axes(axes, rotate_x_labels=60)

    def plot_vmt(self, **kwargs):

        if "df" not in kwargs:
            df = self._get_results("vmt_vht", **kwargs).reset_index()

            if "mode" in kwargs:
                df = filter_df(df, {"mode": kwargs["mode"]})

            if df is None or df.shape[0] == 0:
                logging.warning("There were no results for 'vmt'")
                return

            df = df[~(df["mode"].str.contains("FAIL") | df["mode"].str.contains("NO_MOVE"))]
            df = df.groupby(["mode", "run_id"]).sum().reset_index()
        else:
            df = kwargs["df"]

        group_col = kwargs.get("group_by", "mode")
        groups = df[group_col].unique()
        colors = sns.color_palette(n_colors=len(groups))
        _, axes = plt.subplots(2, 2, figsize=(25, 13))

        x_col = kwargs.get("x", "run_id")

        legend = []
        for m, col in zip(groups, colors):
            df_ = df[df[group_col] == m]
            (line,) = axes[1, 1].plot(df_[x_col], df_["million_VMT"], color=col, marker="o", label=m)
            axes[0, 1].plot(df_[x_col], df_["speed_mph"], color=col, marker="o")
            axes[1, 0].plot(df_[x_col], df_["count"], color=col, marker="o")
            legend += [(line, m)]

        axes[1, 1].set_title("VMT (millions)")
        axes[0, 1].set_title("Speed (mi/h)")
        axes[1, 0].set_title("Number of trips")
        axes[0, 0].legend([e[0] for e in legend], [e[1] for e in legend], loc="center", fontsize=12)

        KpiComparator._style_axes([axes[1, 1], axes[0, 1], axes[1, 0]], rotate_x_labels=60)
        return df

    @staticmethod
    def _style_axes(axes, grid=True, rotate_x_labels=False):
        for ax in axes:
            if grid:
                ax.grid(True, which="both", axis="y", color="#000000", alpha=0.15, zorder=0)
            if rotate_x_labels:
                ax.tick_params(axis="x", rotation=rotate_x_labels)

    def plot_vmt_by_link_type(self, **kwargs):
        df = self._get_results("vmt_vht_by_link", **kwargs)
        df = df.groupby(["type", "run_id"]).sum().reset_index()

        def add_speed(label, hours):
            vmt = df[[f"vmt_{i}" for i in hours]]
            vht = df[[f"vht_{i}" for i in hours]]
            df[f"speed_{label}"] = vmt.sum(axis=1) / vht.sum(axis=1)

        add_speed("daily", ["daily"])
        add_speed("am_peak", [6, 7, 8])
        add_speed("pm_peak", [15, 16, 17])
        add_speed("off_peak", set(range(0, 24)) - {6, 7, 8} - {15, 16, 17})

        _, axes = plt.subplots(2, 2, figsize=(15, 11))
        axes = np.ravel(axes)
        _ = sns.barplot(df, x="type", y="vmt_daily", hue="run_id", ax=axes[0], errorbar=None)
        _ = sns.barplot(df, x="type", y="speed_off_peak", hue="run_id", ax=axes[1], errorbar=None)
        _ = sns.barplot(df, x="type", y="speed_am_peak", hue="run_id", ax=axes[2], errorbar=None)
        _ = sns.barplot(df, x="type", y="speed_pm_peak", hue="run_id", ax=axes[3], errorbar=None)
        KpiComparator._style_axes(axes, rotate_x_labels=30)

        return df

    def plot_gaps(self, **kwargs):
        df = self._get_results("gaps", **kwargs)
        if df is None or df.shape[0] == 0:
            logging.warning("No gap data for this run")
            return
        fig = plt.figure(figsize=(16, 6))
        colors = sns.color_palette(n_colors=3)
        fig.gca().plot(df["run_id"], df["relative_gap"], color=colors[0], marker="o")
        fig.gca().plot(df["run_id"], df["relative_gap_abs"], color=colors[1], marker="o")
        fig.gca().plot(df["run_id"], df["relative_gap_min0"], color=colors[2], marker="o")
        fig.gca().legend(["relative_gap", "relative_gap_abs", "relative_gap_min0"])
        KpiComparator._style_axes([fig.gca()], rotate_x_labels=30)
        return df

    @staticmethod
    def plot_multiple_gaps(kpi_results):
        fig = plt.figure(figsize=(16, 6))
        colors = sns.color_palette(n_colors=len(kpi_results))
        i = 0
        for id, k in ((id, k) for id, k in kpi_results.items() if k is not None):
            df = k._get_results("gaps", False, False)
            if df is None:
                logging.error("df is None?")
                continue
            df = df.sort_values("run_id")
            fig.gca().plot(df["run_id"], df["relative_gap"], color=colors[i], marker="o", label=id)
            i = i + 1
        fig.gca().grid(True, which="both", color="#000000", alpha=0.2)

    def plot_pax_in_network(self, **kwargs):
        df = self._get_results("summary", **kwargs)
        df = df[df.simulated_time < 86340]
        df.sort_values("simulated_time", inplace=True)

        # this has a problem if there are missing values in teh summary file, filter to X to select only the bits that exist for all summary files
        fig = plt.figure(figsize=(16, 6))
        run_ids = df.run_id.unique()
        colors = sns.color_palette(n_colors=len(run_ids))
        for run_id, color in zip(run_ids, colors):
            df_ = df[df.run_id == run_id]
            fig.gca().plot(df_["simulated_time"] / 3600, df_["pax_in_network"], color=color)

        KpiComparator._style_axes([fig.gca()], rotate_x_labels=False)
        fig.gca().legend(run_ids)

    def plot_network_gaps(self, **kwargs):
        _, axes = plt.subplots(2, 2, figsize=(15, 15))

        df = self._get_results("network_gaps_by_link_type", **kwargs)
        sns.barplot(df, x="link_type", y="abs_gap", hue="run_id", ax=axes[0, 0], errorbar=None).set_title("Gap (abs)")
        sns.barplot(df, x="link_type", y="gap", hue="run_id", ax=axes[0, 1], errorbar=None).set_title("Gap")
        KpiComparator._style_axes(axes[0, :], rotate_x_labels=60)

        df = self._get_results("network_gaps_by_hour", **kwargs)
        df.fillna(0.0, inplace=True)  # early morning hours have some weird values
        sns.lineplot(df, x="hour", y="abs_gap", hue="run_id", ax=axes[1, 0], errorbar=None).set_title("Gap (abs)")
        sns.lineplot(df, x="hour", y="gap", hue="run_id", ax=axes[1, 1], errorbar=None).set_title("Gap")
        KpiComparator._style_axes(axes[1, :], rotate_x_labels=False)

    def plot_skim_stats(self, show_min_max=False, **kwargs):
        df = self._get_results("skim_stats", **kwargs)
        df.sort_values("interval", inplace=True)
        if df is None or df.empty:
            logging.warn("No skim stats to plot")
            return

        def f(metric, mode, ax, ylabel):
            df_ = df[(df.metric == metric) & (df["mode"] == mode)]
            run_ids = df.run_id.unique()
            colors = sns.color_palette(n_colors=len(run_ids))
            line_width = 3
            for run_id, color in zip(run_ids, colors):
                df__ = df_[df_.run_id == run_id]
                x = (df__["interval"] / 60).astype(int)

                ax.plot(x, df__["avg"], linestyle="-", color=color, label=run_id, linewidth=line_width)
                line_width -= 0.5
                if show_min_max:
                    ax.plot(x, df__["min"], linestyle="--", color=color)
                    ax.plot(x, df__["max"], linestyle="--", color=color)

            ax.legend()
            ax.set_xticks(x)
            ax.set_ylabel(ylabel)

        _, axes = plt.subplots(4, 1, figsize=(20, 5 * 4))
        f("time", "Auto", ax=axes[0], ylabel="Time (min)")
        f("distance", "Auto", ax=axes[1], ylabel="Distance (m)")
        f("time", "Bus", ax=axes[2], ylabel="Bus Time (min)")
        f("time", "Rail", ax=axes[3], ylabel="Rail Time (min)")
        KpiComparator._style_axes(axes)
        plt.suptitle("Skim change over time (min/max dashed, avg solid)")
        plt.show(block=False)
        return df

    # Utility methods

    def _get_results(self, result_name, **kwargs):
        """Collates together dataframes from each run and annotates them appropriately."""
        run_ids = self._limit_run_ids(**kwargs)
        skip_cache = kwargs.get("skip_cache", False)
        force_cache = kwargs.get("force_cache", False)
        dfs = [
            self._maybe_metric(result_name, kpi, run_id, skip_cache=skip_cache, force_cache=force_cache)
            for run_id, kpi in self.runs.items()
            if run_id in run_ids
        ]
        dfs = [df for df in dfs if df is not None]
        if not dfs:
            return None

        df = pd.concat(dfs)
        if kwargs.get("sort_key", None) is not None:
            df.sort_values(by="run_id", key=kwargs["sort_key"], inplace=True)
        else:
            df.sort_values(by="run_id", inplace=True)
        if kwargs.get("df_transform", None) is not None:
            df = kwargs["df_transform"](df)
        return df

    def _limit_run_ids(self, **kwargs):
        limit_runs = kwargs.get("limit_runs", None)
        if limit_runs is None:
            return set(self.runs.keys())

        # limit runs
        if isinstance(limit_runs, int):
            # limit_runs is a number of runs to show (either first N if N>0, or last N otherwise)
            run_ids = [self.runs.keys()]
            return set(run_ids[-limit_runs:]) if limit_runs > 0 else set(run_ids[:-limit_runs])
        elif isinstance(limit_runs, Pattern):
            return {r for r in self.runs.keys() if limit_runs.match(r)}
        return set(limit_runs)

    def _maybe_metric(self, metric, kpi, run_id, skip_cache, force_cache):
        try:
            return self._add_run_attributes(
                kpi.get_cached_kpi_value(metric, skip_cache=skip_cache, force_cache=force_cache), run_id
            )
        except Exception:
            tb = traceback.format_exc()
            logging.info(f"Exception while getting {metric} for {run_id}")
            logging.info(tb)
            return None
        finally:
            kpi.close()

    def _add_run_attributes(self, df, run_id):
        return df if df is None or not isinstance(df, pd.DataFrame) else df.assign(run_id=run_id)
