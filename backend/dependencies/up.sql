drop table agg_events;

CREATE TABLE agg_events (
    id SERIAL PRIMARY KEY,
    service_id VARCHAR,
    branch_id VARCHAR,
    w_start TIMESTAMP,
    w_end TIMESTAMP,
    total_load INT
);

DROP TABLE branches;

CREATE TABLE branches (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    address VARCHAR,
    geometry POINT
);

DROP TABLE services;

create table services (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    juridical BOOLEAN
);

DROP TABLE branches_services;

CREATE TABLE branches_services (
    id SERIAL PRIMARY KEY,
    branch_id INT,
    service_id INT
);
