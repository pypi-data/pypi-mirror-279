--@ Path_links table shows the trajectory in detail for each path logged in the Path table.
--@ Each record in the Path_links table is a link that was traversed by a vehicle.
--@

CREATE TABLE "Path_links" (

  "object_id" INTEGER NOT NULL,                          --@ The identifier for the path to which this link belongs (foreign key to Path table)
  "index" INTEGER NOT NULL,                              --@ Sequence number for this link within the overall path 
  "value_link" INTEGER NOT NULL DEFAULT 0,               --@ The link which makes up this part of the overall path (foreign key to Link table)
  "value_dir" INTEGER NOT NULL,                          --@ The direction of travel on the link {0: a->b, 1: b->a}
  "value_entering_time" INTEGER NOT NULL DEFAULT 0,      --@ Time seconds when the vehicle entered this link (units: seconds)
  "value_travel_time" INTEGER NOT NULL DEFAULT 0,        --@ Time spent traversing this link (units: seconds)
  "value_delayed_time" INTEGER NOT NULL DEFAULT 0,       --@ Delay time experienced when traversing this link (units: seconds)
  "value_exit_position" REAL NULL DEFAULT 0,             --@ Cumulative distance along this trajectory at the end of this link (units: meters)
  "value_enter_energy_level" REAL NULL DEFAULT 0,        --@ If electric vehicle, battery level when starting to traverse the link (units: Wh)
  "value_exit_energy_level" REAL NULL DEFAULT 0,         --@ If electric vehicle, battery level after traversing the link and consuming energy (units: Wh)
  "value_enter_battery_SoC" REAL NULL DEFAULT 0,         --@ If electric vehicle, battery state of charge when starting to traverse the link (units: % [0.0,1.0])
  "value_exit_battery_SoC" REAL NULL DEFAULT 0,          --@ If electric vehicle, battery state of charge after traversing the link and consuming energy (units: % [0.0,1.0])
  "value_routed_travel_time" REAL NULL DEFAULT 0,        --@ Travel time from the router required to traverse this link (units: seconds)
  "value_Number_of_Switches" INTEGER NOT NULL DEFAULT 0, --@ Cumulative number of switches up to and including while traversing this link
  "value_Switch_Cause" TEXT NOT NULL DEFAULT '',         --@ If switching/rerouting occured, string describing the cause of switch

  CONSTRAINT "object_id_fk"
    FOREIGN KEY ("object_id")
    REFERENCES "Path" ("id")
    ON DELETE CASCADE)