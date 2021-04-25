# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL, 
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
    artist_name TEXT,
    artist_location TEXT,
    artist_latitude TEXT,
    artist_longitude TEXT
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

# INSERT RECORDS

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
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, artist_name, artist_location, artist_latitude, artist_longitude )
VALUES (%s, %s, %s, %s, %s)
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, s.artist_id
FROM songs as s
LEFT JOIN artists a ON a.artist_id = s.artist_id
WHERE s.title LIKE %s
AND a.artist_name LIKE %s
AND s.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]