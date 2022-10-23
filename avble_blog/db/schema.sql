-- CREATE TABLE users (
-- 	id INTEGER PRIMARY KEY,
-- 	username TEXT NOT NULL,
-- 	passwd TEXT NOT NULL,
-- 	first_name TEXT NOT NULL,
-- 	last_name TEXT NOT NULL
-- );

-- CREATE TABLE posts(
-- 	id INTEGER PRIMARY KEY,
-- 	usr_id INTEGER 
-- 	title TEXT NOT NULL,
-- 	content TEXT NOT NULL,
-- 	created_date TEXT NOT NULL
-- );

create table version(
	id serial,
	ver integer unique
);

create table users(
	id serial,
	username text unique,
	passwd text,
	first_name text,
	last_name text
);

create table posts(
	id serial,
	title text,
	title_long text,
	content text,
	created_date timestamp
);