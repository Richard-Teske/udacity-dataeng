## Project: Data Modeling with Postgres

### Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

### Project Description

In this project, you'll apply what you've learned on data modeling with Postgres and build an ETL pipeline using Python. To complete the project, you will need to define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.


### FACT TABLES

1. **songplays** - records in log data associated with song plays
    * *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

<br>

### DIMENSION TABLES

2. **users** - users in the app
    * *user_id, first_name, last_name, gender, level*

3. **songs** - songs in music database
    * *song_id, title, artist_id, year, duration*

4. **artists** - artists in music database
    * *artist_id, name, location, latitude, longitude*

5. **time** - timestamps of records in songplays broken down into specific units
    * *start_time, hour, day, week, month, year, weekday*

<br>

To run a postgre container locally:

`docker run -p 5432:5432 -e POSTGRES_PASSWORD=student -e POSTGRES_USER=student -e POSTGRES_DB=sparkifydb -d postgres`