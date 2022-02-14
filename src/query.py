CREATE_TABLE_MECH = """
    CREATE TABLE IF NOT EXISTS mech (
        mech_id INTEGER PRIMARY KEY,
        mech_name TEXT NOT NULL, 
        mech_model TEXT NOT NULL,
        mech_is_omnimech INTEGER
            NOT NULL
            CHECK (mech_is_omnimech = 0 OR mech_is_omnimech = 1),
        ts_insert TEXT,
        ts_update TEXT,
        ts_delete TEXT,
        UNIQUE (mech_name, mech_model) );"""
CREATE_TABLE_QUIRK = """
    CREATE TABLE IF NOT EXISTS quirk (
        quirk_id INTEGER PRIMARY KEY,
        mech_id INTEGER REFERENCES mech(mech_id) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE 
            DEFERRABLE INITIALLY DEFERRED,
        component TEXT NOT NULL,
        quirk_name TEXT NOT NULL,
        quirk_value REAL NOT NULL,
        ts_insert TEXT,
        ts_update TEXT,
        ts_delete TEXT,
        UNIQUE (mech_id, quirk_name));"""
UPSERT_MECH = """
    INSERT INTO mech (mech_name, mech_model, mech_is_omnimech, ts_insert)
    VALUES (?, ?, ?, datetime('now'))
    ON CONFLICT (mech_name, mech_model)
    DO UPDATE SET ts_update = datetime('now')
    RETURNING mech_id"""
UPSERT_QUIRK = """
    INSERT INTO quirk (mech_id, component, quirk_name, quirk_value, ts_insert)
    VALUES (?, ?, ?, ?, datetime('now'))
    ON CONFLICT 
    DO UPDATE SET quirk_value = excluded.quirk_value,
                  ts_update = datetime('now')"""
