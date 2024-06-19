CREATE TABLE IF NOT EXISTS "Toll_Pricing" (
    "link"         INTEGER NOT NULL,
    "dir"          INTEGER NOT NULL DEFAULT 0,
    "start_time"   INTEGER NOT NULL DEFAULT 0,
    "end_time"     INTEGER NOT NULL DEFAULT 0,
    "price"        REAL    NOT NULL DEFAULT 0,

    CONSTRAINT "link_fk" FOREIGN KEY("link") REFERENCES "Link"("link") DEFERRABLE INITIALLY DEFERRED
);