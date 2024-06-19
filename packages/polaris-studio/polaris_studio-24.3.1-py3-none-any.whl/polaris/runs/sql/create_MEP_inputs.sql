DROP TABLE IF EXISTS activity_by_zone;  
create table activity_by_zone as
select l.zone as taz,  
    sum(CASE WHEN type= 'EAT OUT' THEN 1 END) as EAT_OUT,
    sum(CASE WHEN type= 'ERRANDS' THEN 1 END) as ERRANDS,
    sum(CASE WHEN type= 'HEALTHCARE' THEN 1 END) as HEALTHCARE,
    sum(CASE WHEN type= 'LEISURE' THEN 1 END) as LEISURE,
    sum(CASE WHEN type= 'PERSONAL' THEN 1 END) as PERSONAL,
    sum(CASE WHEN type= 'RELIGIOUS-CIVIC' THEN 1 END) as RELIGIOUS,
    sum(CASE WHEN type= 'SERVICE' THEN 1 END) as SERVICE,
    sum(CASE WHEN type= 'SHOP-MAJOR' THEN 1 END) as SHOP_MAJOR,
    sum(CASE WHEN type= 'SHOP-OTHER' THEN 1 END) as SHOP_OTHER,
    sum(CASE WHEN type= 'SOCIAL' THEN 1 END) as SOCIAL,
    sum(CASE WHEN type= 'WORK' THEN 1 END) as WORK,
    sum(CASE WHEN type= 'PART_WORK' THEN 1 END) as WORK_PART,
    sum(CASE WHEN type= 'WORK AT HOME' THEN 1 END) as WORK_HOME,
    sum(CASE WHEN type= 'SCHOOL' THEN 1 END) as SCHOOL,
    sum(CASE WHEN type= 'PICKUP-DROPOFF' THEN 1 END) as PICKUP,
    sum(CASE WHEN type= 'HOME' THEN 1 END) as HOME,
    sum(1) AS ACT_TOTAL
from activity, supply.location as l
where l.location = location_id
group by taz;

drop table if exists loc_parking_values;
create temp table loc_parking_values as 
select l.location as location, sum(p.space*l.distance)/ sum(p.space)/1.34112/60 + loc.avg_parking_cost /63.0*60.0 as gen_time_min, loc.zone as zone
from supply.location_parking as l, supply.parking as p, supply.location as loc
where l.parking = p.parking and loc.location = l.location and p.hourly < 120
group by l.location;

drop table if exists zone_parking;
create table zone_parking as 
select l.zone as taz, avg(gen_time_min) as time_gen_min
from loc_parking_values l, trip t
where l.location = t.destination
group by l.zone;

-- model_zones.csv file
drop table if exists model_zones;
create table model_zones as 
select zone, astext(geo) as WKT
from supply.zone;

-- blocks.csv file
drop table if exists blocks_mep;
create table blocks_mep as
SELECT location as block_id, x, y
FROM supply.location
ORDER BY ROWID;

--jobs.csv file (From Demand db)
drop table if exists jobs_mep;
create table jobs_mep as
select work_location_id as block_id, industry as sector_id, count(*) as job_count
from person
where block_id >= 0
group by block_id, sector_id;

--households.csv file
drop table if exists households_mep;
create table households_mep as
SELECT household, location as block_id, persons
FROM household
ORDER BY household;


--.headers on 
--.mode csv 


--.output "activities.csv" 
--select *
--from activity_by_zone
--; 

--.output "park_times.csv" 
--select *
--from zone_parking
--; 

--.output "tnc_wait_times.csv" 
drop table if exists tnc_wait_times;
create table tnc_wait_times as
select zone, start, end, avg_wait_minutes
from result.zonewaittimes
order by zone, start;
 


--.exit 
