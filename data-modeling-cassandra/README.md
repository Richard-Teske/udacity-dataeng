## Project: Data Modeling with Cassandra

![cassandra-logo](images/cassandralogo.png)

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

They'd like a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions, and wish to bring you on the project. Your role is to create a database for this analysis. You'll be able to test your database by running queries given to you by the analytics team from Sparkify to create the results.

## Dataset

For this project, you'll be working with one dataset: **event_data**. The directory of CSV files partitioned by date

Example of file name and content:

`event_data/2018-11-01-events.csv`

![event_datafile](images/image_event_datafile_new.jpg)

## Project Template

* You will process the event_datafile_new.csv dataset to create a denormalized dataset
* You will model the data tables keeping in mind the queries you need to run
* You have been provided queries that you will need to model your data tables for
* You will load the data into tables you create in Apache Cassandra and run your queries

## Project Steps & Pipeline

1. Design tables to answer the queries outlined in the project template
2. Write Apache Cassandra CREATE KEYSPACE and SET KEYSPACE statements
3. Develop your CREATE statement for each of the tables to address each question
4. Load the data with INSERT statement for each of the tables
5. Include IF NOT EXISTS clauses in your CREATE statements to create tables only if the tables do not already exist. We recommend you also include DROP TABLE statement for each table, this way you can run drop and create tables whenever you want to reset your database and test your ETL pipeline
6. Test by running the proper select statements with the correct WHERE clause

## Configurations

To run a Cassandra container locally:

`docker run -p 9042:9042 --name cassandra -d cassandra:4.0`

## Learning Path

### Introduction

Apache Cassandra is a Open Source NoSQL database, your architecture is oriented by queries, **one query one table**. Also is a distribuited databases which increase your performance.

Cassandra uses your own query language (CQL), but it's similar to SQL. <br>
*JOINS, GROUP BY or sub queries are not supported*

When to use NoSQL databases:<br>
* High availability
* Large amount of data
* Linear scalability
* Low latency
* Fast reads and write

### Dernomalization

Denormalization in Apache Cassandra it's a important thing to know, the tables are defined based on your queries, so **think your queries first**. There's no JOINS!

That's one thing that make Cassandra fast, tables only have data used by a single query.

**You don't have to concern about duplicate data.**

### Primary Key & Partition Key

Primary key is what identify a single data in databases. Apache Cassandra uses the primary key to partitionate the data into multiples nodes.

* Primary key must be **unique**
* The primary key is made up of either just the **partition key** or may also include **additional clustering columns**
* It could be defined by a **simple** primary key (only one column) or **composite** (more then one column) that will be unified into a single value
* The **partition key** will determinate the **distribution of data** across multiple nodes 

Primary Key Example:

```sql
CREATE TABLE music_library
(
    year int,
    artist_name text,
    album_name text,
    PRIMARY KEY (year)
)
```

Clustering Columns

* Will sort the data in **DESC** order
* More than one clustering column can be added

```sql
CREATE TABLE music_library
(
    year int,
    artist_name text,
    album_name text,
    PRIMARY KEY ((year), artist_name, album_name)
)
```

When creating a query using this clustering column table, the data is showed ordered by columns order in create table statement. All columns are sorted **descending**

Remember that: in this example, the primary key is **composite** (year, artist_name, album_name), **partition key** is year column and **clustering columns** are artist_name and album_name that will be ordered descending