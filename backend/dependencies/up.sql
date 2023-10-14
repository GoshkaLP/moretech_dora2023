drop table agg_events;

CREATE TABLE agg_events (
    id SERIAL PRIMARY KEY,
    service_id VARCHAR,
    branch_id VARCHAR,
    w_start TIMESTAMP,
    w_end TIMESTAMP,
    total_load INT
);

create table branches (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    address VARCHAR,
    latitude VARCHAR,
    longitude VARCHAR
);

create table services (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    juridical BOOLEAN
);

CREATE TABLE branches_services (
    id SERIAL PRIMARY KEY,
    branch_id INT REFERENCES branches(id),
    service_id INT REFERENCES services(id)
);
