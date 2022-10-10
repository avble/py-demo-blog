CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL
);

CREATE TABLE posts(
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	content TEXT NOT NULL,
	created_date TEXT NOT NULL
);