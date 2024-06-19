pragma foreign_keys = off;

delete from path_multimodal;
delete from path_multimodal_links;

delete from trip where mode not in (0, 17, 18, 19, 20);

delete from path where id not in (select path from trip);
delete from path_links where object_id not in (select id from path);

update trip set path_multimodal = NULL;

pragma foreign_keys = on;
