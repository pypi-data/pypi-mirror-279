-- name: create_schema#
CREATE TABLE gists
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT,
    description    TEXT,
    gh_id          TEXT,
    public         INTEGER,
    starred        INTEGER,
    owner          TEXT,
    tags_str       TEXT,
    filenames_str  TEXT,
    extensions_str TEXT,
    content        TEXT
) STRICT