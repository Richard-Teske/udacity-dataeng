## Project: Data Warehouse on AWS

<br>

## Configurations

To run a postgres docker container locally:<br>
`docker run --name postgres-pagila -p 5432:5432 -e POSTGRES_PASSWORD=student -e POSTGRES_USER=student -e POSTGRES_DB=pagila -d postgres`

To install pagila database, we need to follow a few steps:
1. Download pagila scripts to create schema & insert data. You can download them from https://www.postgresql.org/ftp/projects/pgFoundry/dbsamples/pagila/pagila/
2. Change the owner name inside script from "**postgres**" to "**student**"
3. With a postgres container running, execute the **pagila-schema.sql** file to create schema: <br>
`cat $(pwd)/udacity-dataeng/cloud-data-warehouse/pagila-scripts/pagila-schema.sql | docker exec -i postgres-pagila psql -U student -d pagila` 
4. Final, insert data in your tables: <br> 
`cat $(pwd)/udacity-dataeng/cloud-data-warehouse/pagila-scripts/pagila-data.sql | docker exec -i postgres-pagila psql -U student -d pagila`

Reminder: If you're in local repository, change the location where your files are

Now you can select some data:<br>
`docker exec -it postgres-pagila psql -U student -d pagila -c "SELECT * FROM {table_name} LIMIT 5"`


![img-language-table](images/img-language-table.png)


## Learning Path

### Introduction

What is a data warehouse?

- Data warehouse is a copy of transaction data specifically structured for **query** and **data analysis**. (*ref. Kimball*)
- It is a subject-oriented, integrated, nonvolatile, and time-variant collection of data in **support of management's decisions**. (*ref. Inmon*)
- DW is a system that retrieves and consolidates data **periodically** from the source into a **dimensional** or **normalized** data store. It usually keeps years of **history** and is queried for *business intelligence* or other **analytical activities**. It is typically updated in **batches**. (*ref. Rainardi*)

<br>

### Dimensional Modelling

Relational databases became hard to analytics due joins that we have to do for analytical insights and it's difficult to understand. Dimensional modelling comes to make it more easy.

There's 2 types of dimensional modelling 

**Star Schema** (left) and **Snow Flake** (right)

![star-schema-vs-snow-flake](images/star-schema-vs-snow-flake.png)

<br>

### Facts Tables
* Record business events
* Columns recorded events in **quantifiable metrics**
* Numeric & Additive
* e.g: quantity of an item, duration of a call, a rating

### Dimension Tables
* Record the context of business events (who, what, where, why, how)
* Columns contain **attributes**
* e.g: Customer name, Item color, etc...

