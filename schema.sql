-- Author: Mohammed Ali
-- Date: 2023-04-16


-- drop tables in case they exist
drop table if exists task_completions;
drop table if exists tasks;
drop table if exists materials;
drop table if exists local_users;
drop table if exists collection_points;
drop table if exists businesses;


-- create tables
CREATE TABLE businesses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL
);

CREATE TABLE collection_points (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    address TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

CREATE TABLE local_users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL
);

CREATE TABLE materials (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    condition TEXT NOT NULL,
    collection_point_id INTEGER NOT NULL,
    FOREIGN KEY (collection_point_id) REFERENCES collection_points (id)
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    points INTEGER NOT NULL,
    collection_point_id INTEGER NOT NULL,
    FOREIGN KEY (collection_point_id) REFERENCES collection_points (id)
);

CREATE TABLE task_completions (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL,
    local_user_id INTEGER NOT NULL,
    completion_date TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id),
    FOREIGN KEY (local_user_id) REFERENCES local_users (id)
);
