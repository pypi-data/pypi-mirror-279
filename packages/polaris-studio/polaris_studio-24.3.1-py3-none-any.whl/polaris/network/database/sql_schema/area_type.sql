--@ Area types are used throughout the demand model to differentiate different
--@ regions within the modeled area (e.g. CBD, inner suburb, outer suburb,
--@ industrial).
--@

create TABLE IF NOT EXISTS "Area_Type" (
    "area_type" INTEGER NOT NULL PRIMARY KEY, --@ Unique identifier for the area type
    "name"      TEXT    NOT NULL DEFAULT '',  --@ Simple description of the area type
    "notes"     TEXT                          --@ User notes
);

INSERT INTO "Area_Type" VALUES (100,'default area type', 'default with no practical meaning');