--@ This table contains vehicle trajectories when the traffic model is lagrangian coordinates
--@ and the write_lc_trajectory flag is enabled. It provides position, and vehicle speed
--@ along the link (and therefore more detailed than the path_links table)

CREATE TABLE IF NOT EXISTS "Path_units" (
  "object_id" INTEGER NOT NULL,                   --@ The identifier of the path this record is associated with (foreign key to Path table)
  "index" INTEGER NOT NULL,                       --@ Sequence number for this link within the overall path
  "value_link_uuid" INTEGER NOT NULL DEFAULT 0,   --@ The unidirectional link this record corresponds to (note this is not the id from the link table)
  "value_position" REAL NULL DEFAULT 0,           --@ The position of the vehicle along the link (units: meters)
  "value_speed" REAL NULL DEFAULT 0,              --@ Current speend (units: m/s)
  "value_queued" INTEGER NOT NULL,                --@ boolean flag - would the vehicle be able to proceed to next link aside any priority or intersection control
  "value_time_queued" INTEGER NOT NULL DEFAULT 0, --@ The time that the value_time_queued transitioed from 0 to 1 if value_queued=1 (units: simulation time step)
  "value_sim_index" INTEGER NOT NULL DEFAULT 0,   --@ The simulation index of the simulation (each step is one lagrangian coordinate time step. The time-step is simulation_interval_length/num_lagrangian_substeps)

  CONSTRAINT "object_id_fk"
    FOREIGN KEY ("object_id")
    REFERENCES "Path" ("id")
    ON DELETE CASCADE)