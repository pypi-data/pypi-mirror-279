--@ Table provides the aggregate information of the path traversed by a vehicle during simulation in POLARIS.
--@ The trajectory-specific information is logged in the Path_links table where Path (id) = Path_links (object_id)
--@

CREATE TABLE "Path" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,             --@ Unique identifier of this path record
  "traveler_id" INTEGER NOT NULL DEFAULT 0,                    --@ The person driving the vehicle along this path (foreign key to Person table)
  "origin_activity_location" INTEGER NOT NULL DEFAULT 0,       --@ Origin location from which this path started (foreign key to Location table)
  "destination_activity_location" INTEGER NOT NULL DEFAULT 0,  --@ Destination location at which this path ended (foreign key to Location table)
  "origin_link" INTEGER NOT NULL DEFAULT 0,                    --@ The id of the first link in the path sequence (foreign key to Link table)
  "destination_link" INTEGER NOT NULL DEFAULT 0,               --@ The id of the last link in the path sequence (foreign key to Link table)
  "num_links" INTEGER NOT NULL DEFAULT 0,                      --@ Total number of links that comprise this path
  "departure_time" INTEGER NOT NULL DEFAULT 0,                 --@ The time at which travel along the path began (units: seconds)
  "routed_time" INTEGER NOT NULL DEFAULT 0,                    --@ Travel time (as estimated by the router) to traverse the path (units: seconds)
  "travel_time" INTEGER NOT NULL DEFAULT 0,                    --@ Actual experienced travel time to traverse the path (units: seconds)
  "vehicle" INTEGER NULL,                                      --@ Vehicle that traversed the path (foreign key to Vehicle table)

  CONSTRAINT "vehicle_fk"
    FOREIGN KEY ("vehicle")
    REFERENCES "Vehicle" ("vehicle_id")
    DEFERRABLE INITIALLY DEFERRED)