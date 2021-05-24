import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_logs"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_logs (
    artist TEXT,
    auth TEXT,
    firstName TEXT,
    gender TEXT,
    itemInSession INTEGER,
    lastName TEXT,
    length FLOAT,
    level TEXT,
    location TEXT,
    method TEXT,
    page TEXT,
    registration FLOAT,
    sessionId INTEGER,
    song TEXT,
    status INTEGER,
    ts TIMESTAMP,
    userAgent TEXT,
    userId INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs INTEGER,
    artist_id TEXT,
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_location TEXT,
    artist_name TEXT,
    song_id TEXT,
    title TEXT,
    duration FLOAT,
    year INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id INTEGER IDENTITY(0,1), 
    start_time TIMESTAMP, 
    user_id INTEGER, 
    level TEXT, 
    song_id TEXT, 
    artist_id TEXT, 
    session_id INTEGER, 
    location TEXT, 
    user_agent TEXT
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    level TEXT
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS "songs" (
    song_id TEXT NOT NULL,
    title TEXT,
    artist_id TEXT,
    year INTEGER,
    duration NUMERIC(10, 2)
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id TEXT NOT NULL,
    name TEXT,
    location TEXT,
    latitude TEXT,
    longitude TEXT
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP, 
    hour INTEGER,
    day INTEGER, 
    week INTEGER,
    month INTEGER,  
    year INTEGER, 
    weekday INTEGER
);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_logs
FROM {}
IAM_ROLE {}
REGION {}
FORMAT AS JSON {}
TIMEFORMAT 'epochmillisecs';
""").format(config.get("S3", "LOG_DATA"), config.get("IAM_ROLE", "ARN"), config.get("S3", "REGION"), config.get("S3", "LOG_JSONPATH"))

staging_songs_copy = ("""
COPY staging_songs
FROM {}
IAM_ROLE {}
REGION {}
FORMAT AS JSON 'auto'
TIMEFORMAT 'epochmillisecs';
""").format(config.get("S3", "SONG_DATA"), config.get("IAM_ROLE", "ARN"), config.get("S3", "REGION"))

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time , 
    user_id , 
    level , 
    song_id , 
    artist_id , 
    session_id , 
    location , 
    user_agent )
SELECT      DISTINCT
            l.ts,
            l.userId,
            l.level,
            s.song_id,
            s.artist_id,
            l.sessionId,
            l.location,
            l.userAgent
FROM        staging_songs s
JOIN        staging_logs l ON s.artist_name = l.artist
WHERE       l.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT      DISTINCT
            l.userId,
            l.firstName,
            l.lastName,
            l.gender,
            l.level
FROM        staging_logs l
WHERE       l.userId IS NOT NULL
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT      DISTINCT
            s.song_id,
            s.title,
            s.artist_id,
            s.year,
            s.duration
FROM        staging_songs s
WHERE       s.song_id IS NOT NULL
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude )
SELECT      DISTINCT
            s.artist_id,
            s.artist_name,
            s.artist_location,
            s.artist_latitude,
            s.artist_longitude
FROM        staging_songs s
WHERE       s.artist_id IS NOT NULL
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT      DISTINCT
            l.ts,
            EXTRACT(HOUR FROM l.ts),
            EXTRACT(DAY FROM l.ts),
            EXTRACT(WEEK FROM l.ts),
            EXTRACT(MONTH FROM l.ts),
            EXTRACT(YEAR FROM l.ts),
            EXTRACT(WEEKDAY FROM l.ts)
FROM        staging_logs l
WHERE       l.ts IS NOT NULL
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]
