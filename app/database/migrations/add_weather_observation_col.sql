ALTER TABLE weather_observation
  ADD COLUMN apparent_temperature NUMERIC,
  ADD COLUMN is_day INTEGER,
  ADD COLUMN precipitation NUMERIC,
  ADD COLUMN wind_speed_10m NUMERIC;
