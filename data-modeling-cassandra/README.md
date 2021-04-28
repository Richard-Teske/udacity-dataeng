## Project: Data Modeling with Cassandra

![cassandra-logo](images/cassandralogo.png)

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