-- Active: 1708460552950@@dpg-cnai9lmn7f5s73fpfdfg-a.oregon-postgres.render.com@5432
CREATE DATABASE cyberlink_careersdb;
USE cyberlink_careersdb;
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    salary NUMERIC,
    currency VARCHAR(10),
    responsibilities TEXT,
    requirements TEXT
);
