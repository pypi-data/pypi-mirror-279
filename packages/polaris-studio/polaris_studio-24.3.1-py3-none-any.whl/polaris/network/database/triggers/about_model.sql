--##
create trigger if not exists prevent_delete_version before delete on About_Model
when
old.infoname = "network_model_version"
begin
    select raise(ROLLBACK, "You cannot delete this record");
end;

--##
create trigger if not exists prevent_change_version before update on About_Model
when
    old.infoname = "network_model_version"
begin
    select raise(ROLLBACK, "You cannot make changes to this record outside the API");
end;