#!/bin/bash

docker run --name postgres-pagila -p 5432:5432 \
    -e POSTGRES_PASSWORD=student \
    -e POSTGRES_USER=student \
    -e POSTGRES_DB=pagila \
    -d postgres

cat $(pwd)/udacity-dataeng/cloud-data-warehouse/pagila-scripts/pagila-schema.sql | \
    docker exec -i postgres-pagila psql -U student -d pagila

cat $(pwd)/udacity-dataeng/cloud-data-warehouse/pagila-scripts/pagila-data.sql | \
    docker exec -i postgres-pagila psql -U student -d pagila