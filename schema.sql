-- Author: Mohammed Ali
-- Date: 2023-04-16


-- drop tables in case they exist
drop table if exists task_completions;
drop table if exists tasks;
drop table if exists materials;
drop table if exists users;
drop table if exists collectors;
drop table if exists businesses;
drop table if exists current_tasks;


-- create tables
CREATE TABLE businesses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL
);

CREATE TABLE collectors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    address TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    hash TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    points INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE materials (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    condition TEXT NOT NULL,
    collector_id INTEGER NOT NULL,
    FOREIGN KEY (collector_id) REFERENCES collectors (id)
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    points INTEGER NOT NULL,
    collector_id INTEGER NOT NULL,
    FOREIGN KEY (collector_id) REFERENCES collectors (id)
);

-- create current_tasks table

CREATE TABLE current_tasks (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- create task_completions table

CREATE TABLE task_completions (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    completion_date TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
