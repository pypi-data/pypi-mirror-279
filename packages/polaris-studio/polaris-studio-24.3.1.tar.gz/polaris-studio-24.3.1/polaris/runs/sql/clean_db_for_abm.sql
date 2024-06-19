pragma foreign_keys = off;

delete from activity;
delete from path_links;
delete from path;
delete from path_multimodal_links;
delete from path_multimodal;
delete from path_units;




delete from trip where type <> 22; -- DELETE NON-EXTERNAL TRIPS

update trip set vehicle = NULL, person = NULL, path = NULL, path_multimodal = NULL, experienced_gap = 1.0;

pragma foreign_keys = on;
