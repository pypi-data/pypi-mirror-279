--.headers on 
--.mode csv 
--.output "vehicle_trajectory.csv" 

drop table if exists vehicle_trajectory;
create table vehicle_trajectory as
select 
    path.id as trip, 
    path.vehicle, 
    vehicle.type as veh_type, 
    case trip.mode
      when 0 then "SOV"
      when 1 then "AUTO"
      when 2 then "HOV"
      when 3 then "TRUCK"
      when 4 then "BUS"
      when 5 then "RAIL"
      when 6 then "NONMOTORIZED"
      when 7 then "BICYCLE"
      when 8 then "WALK"
      when 9 then "TAXI"
      when 10 then "SCHOOLBUS"
      when 11 then "PARK_AND_RIDE"
      when 12 then "KISS_AND_RIDE"
      when 13 then "PARK_AND_RAIL"
      when 14 then "KISS_AND_RAIL"
      when 15 then "TNC_AND_RIDE"
      when 16 then "TNC_AND_RAIL"
      when 17 then "MD_TRUCK"  
      when 18 then "HD_TRUCK"
      when 19 then "BPLATE"
      when 20 then "LD_TRUCK"
      when 21 then "RAIL_NEST"
      when 22 then "BUS40"
      when 23 then "BUS60"
      when 24 then "PNR_BIKE_NEST"
    end as 'mode',
    path_links.[index] as link_number, 
    path_links.value_link as link_id, 
    path_links.value_dir as link_dir, 
    path_links.value_entering_time as entering_time, 
    path_links.value_travel_time as travel_time, 
    round(path_links.value_exit_position - a.link.length,2) as start_position, 
    round(a.link.length,2) as length, 
    a.link.length / (path_links.value_travel_time - path_links.value_delayed_time) as actual_speed, 
    case when path_links.value_dir = 0 then a.link.fspd_ab else a.link.fspd_ba end as free_flow_speed, 
    path_links.value_delayed_time as stopped_time, 
    path_links.value_exit_position as stop_position,
    path_links.value_enter_energy_level as enter_energy_level,    
    path_links.value_exit_energy_level as exit_energy_level,
    path_links.value_enter_battery_SoC as enter_SoC,    
    path_links.value_exit_battery_SoC as exit_SoC
from path, path_links, a.link, vehicle, trip 

where
    path.id = path_links.object_id and 
    path_links.value_link = a.link.link and 
    path_links.[index]+1 < path.num_links and 
    vehicle.vehicle_id = path.vehicle and 
    path_links.value_travel_time >0 and 
    trip.path = path.id and
    trip.mode <> 9 and
    trip.has_artificial_trip = 0
order by 
    path.vehicle, 
    path_links.value_entering_time
; 

--.headers off
insert into vehicle_trajectory
select 
    path.id as TNC_trip, 
    path.vehicle, 
    vehicle.type as veh_type, 
    case TNC_trip.mode
      when 0 then "SOV"
      when 1 then "AUTO"
      when 2 then "HOV"
      when 3 then "TRUCK"
      when 4 then "BUS"
      when 5 then "RAIL"
      when 6 then "NONMOTORIZED"
      when 7 then "BICYCLE"
      when 8 then "WALK"
      when 9 then "TAXI"
      when 10 then "SCHOOLBUS"
      when 11 then "PARK_AND_RIDE"
      when 12 then "KISS_AND_RIDE"
      when 13 then "PARK_AND_RAIL"
      when 14 then "KISS_AND_RAIL"
      when 15 then "TNC_AND_RIDE"
      when 16 then "TNC_AND_RAIL"
      when 17 then "MD_TRUCK"  
      when 18 then "HD_TRUCK"
      when 19 then "BPLATE"
      when 20 then "LD_TRUCK"
      when 21 then "RAIL_NEST"
      when 22 then "BUS40"
      when 23 then "BUS60"
      when 24 then "PNR_BIKE_NEST"
    end as 'mode',
    path_links.[index] as link_number, 
    path_links.value_link as link_id, 
    path_links.value_dir as link_dir, 
    path_links.value_entering_time as entering_time, 
    path_links.value_travel_time as travel_time, 
    round(path_links.value_exit_position - a.link.length,2) as start_position, 
    round(a.link.length,2) as length, 
    a.link.length / (path_links.value_travel_time - path_links.value_delayed_time) as actual_speed, 
    case when path_links.value_dir = 0 then a.link.fspd_ab else a.link.fspd_ba end as free_flow_speed, 
    path_links.value_delayed_time as stopped_time, 
    path_links.value_exit_position as stop_position,
    path_links.value_enter_energy_level as enter_energy_level,    
    path_links.value_exit_energy_level as exit_energy_level,
    path_links.value_enter_battery_SoC as enter_SoC,    
    path_links.value_exit_battery_SoC as exit_SoC
from path, path_links, a.link, vehicle, TNC_trip 

where
    path.id = path_links.object_id and 
    path_links.value_link = a.link.link and 
    path_links.[index]+1 < path.num_links and 
    vehicle.vehicle_id = path.vehicle and 
    path_links.value_travel_time >0 and 
    TNC_trip.path = path.id and
    TNC_trip.mode = 9

order by 
    path.vehicle, 
    path_links.value_entering_time
; 

--.headers on 
--.mode csv 
--.output "trajectory_transit.csv" 
drop table if exists transit_trajectory;
create table transit_trajectory as
select
    a.value_transit_vehicle_trip as trip,  
    a.value_transit_vehicle_trip + 100000000 as vehicle,  
    10009 as veh_type, 
    'TRANSIT_BUS' as mode,
    a.value_transit_vehicle_stop_sequence as link_number,  
    a.value_link as link_id,    
    a.value_dir as link_dir,    
    a.value_act_departure_time as entering_time,    
    a.value_act_travel_time as travel_time,    
    round(a.value_start_position,2) as start_position,    
    round(a.value_length,2) as length,    
    round(a.value_speed,2) as actual_speed,    
    round(a.value_speed+5,2) as free_flow_speed,   
    b.value_act_dwell_time as stopped_time,  
    round(a.value_exit_position,2) as stop_position  
    
from transit_vehicle_links a, transit_vehicle_links b 
where 
    a.value_link <> -1
    and a.value_transit_vehicle_trip = b.value_transit_vehicle_trip
    and a.value_transit_vehicle_stop_sequence + 1 = b.value_transit_vehicle_stop_sequence
    and a.value_link_type = 12
;

--.exit 
