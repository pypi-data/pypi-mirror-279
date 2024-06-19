drop table if exists edges;
create temp table edges as
SELECT link * 2 as edge_id, node_a, node_b, length, geo from supply.link where lanes_ab > 0 and type <> 'WALKWAY'  and type <> 'BIKEWAY'  and type <> 'BUSWAY'  and type <> 'LIGHTRAIL'  and type <> 'HEAVYRAIL'  and type <> 'FERRY'
UNION
--select link * 2 + 1 as edge_id, node_b, node_a, length, MakeLine(ST_DissolvePoints(geo),0) from supply.link where lanes_ba > 0 and type <> 'WALKWAY'  and type <> 'BIKEWAY'  and type <> 'BUSWAY'  and type <> 'LIGHTRAIL'  and type <> 'HEAVYRAIL'  and type <> 'FERRY'
select link * 2 + 1 as edge_id, node_b, node_a, length, geo from supply.link where lanes_ba > 0 and type <> 'WALKWAY'  and type <> 'BIKEWAY'  and type <> 'BUSWAY'  and type <> 'LIGHTRAIL'  and type <> 'HEAVYRAIL'  and type <> 'FERRY'

order by edge_id;

CREATE INDEX edge_idx
ON "edges"
(
edge_id
);

drop table if exists link_MEP_calculations;
create table link_MEP_calculations as
SELECT (2*z.value_link + z.value_dir) as edge, 
l.node_a as 'from',
l.node_b as 'to',
l.length as 'distance',

avg(case
when z.value_entering_time >= 7*3600 and z.value_entering_time <= 9*3600 then z.value_travel_time
else null end) as ttime_ampeak,

avg(case
when z.value_entering_time >= 16*3600 and z.value_entering_time <= 18*3600 then z.value_travel_time
else null end) as ttime_pmpeak,

avg(case
when z.value_entering_time < 7*3600 or (z.value_entering_time > 9*3600 and z.value_entering_time < 16*3600) or z.value_entering_time > 18*3600 then z.value_travel_time
else null end) as ttime_offpeak,

avg(case
when z.value_entering_time >= 7*3600 and z.value_entering_time <= 9*3600 then z.value_travel_time
else null end) as weighted_generalized_ttime_ampeak,

avg(case
when z.value_entering_time >= 16*3600 and z.value_entering_time <= 18*3600 then z.value_travel_time
else null end) as weighted_generalized_ttime_pmpeak,

avg(case
when z.value_entering_time < 7*3600 or (z.value_entering_time > 9*3600 and z.value_entering_time < 16*3600) or z.value_entering_time > 18*3600 then z.value_travel_time
else null end) as weighted_generalized_ttime_offpeak,

--'geo' as WKT
astext(e.geo) as WKT

FROM "Vehicle_Type" v, fuel_type f, powertrain_type p, automation_type a, vehicle_class c, vehicle x, path y, path_links z, trip q, supply.link l, edges e

where
v.powertrain_type = p.type_id and 
v.vehicle_class = c.class_id and 
v.fuel_type = f.type_id and 
v.automation_type = a.type_id and
z.value_link = l.link and

z.object_id = y.id and
y.vehicle = x.vehicle_id and
x.type = v.type_id and
y.id = q.path and
z.value_travel_time > 0 and
e.edge_id = 2*z.value_link + z.value_dir

group by z.value_link, z.value_dir
order by z.value_link, z.value_dir;

insert into link_MEP_calculations
select 
    edge_id as 'edge',
    node_a as 'from',
    node_b as 'to',
    length as 'distance',
    NULL ttime_ampeak,
    NULL ttime_pmpeak,
    NULL ttime_offpeak,
    NULL weighted_generalized_ttime_ampeak,
    NULL weighted_generalized_ttime_pmpeak,
    NULL weighted_generalized_ttime_offpeak,
    --'geo' as WKT
    astext(geo) as WKT
from edges
where edge_id not in (select edge from link_MEP_calculations);

update link_MEP_calculations
set ttime_ampeak = (select case
    when link_MEP_calculations.edge%2 = 0 then l.length/l.fspd_ab
    when link_MEP_calculations.edge%2 = 1 then l.length/l.fspd_ba
    else null end
    from supply."link" l where l.link = cast((link_MEP_calculations.edge)/2 as int))
where ttime_ampeak is NULL;

update link_MEP_calculations
set ttime_pmpeak = ttime_ampeak
where ttime_pmpeak is NULL;

update link_MEP_calculations
set ttime_offpeak = ttime_ampeak
where ttime_offpeak is NULL;

update link_MEP_calculations
set weighted_generalized_ttime_ampeak = ttime_ampeak
where weighted_generalized_ttime_ampeak is NULL;

update link_MEP_calculations
set weighted_generalized_ttime_pmpeak = ttime_pmpeak
where weighted_generalized_ttime_pmpeak is NULL;

update link_MEP_calculations
set weighted_generalized_ttime_offpeak = ttime_offpeak
where weighted_generalized_ttime_offpeak is NULL;

--.headers on 
--.mode csv 
--.output "network_results.csv" 
--select * from link_MEP_calculations;

--.exit