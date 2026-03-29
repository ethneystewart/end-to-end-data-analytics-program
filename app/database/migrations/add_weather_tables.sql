CREATE TABLE weather_raw (
    id SERIAL PRIMARY KEY,
    moodlog_id INTEGER NOT NULL UNIQUE REFERENCES moodlog(id),
    source TEXT NOT NULL,
    requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    raw_payload JSONB NOT NULL
);

CREATE TABLE weather_observation (
    id SERIAL PRIMARY KEY,
    moodlog_id INTEGER NOT NULL UNIQUE REFERENCES moodlog(id),
    temperature_2m NUMERIC,
    weather_code INTEGER
);
