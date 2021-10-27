
CREATE TABLE IF NOT EXISTS staging_events (
	artist varchar,
	auth varchar,
	firstname varchar,
	gender varchar,
	iteminsession bigint,
	lastName varchar,
	length numeric,
	level varchar,
	LOCATION varchar,
	method varchar,
	page varchar,
	registration varchar,
	sessionid bigint,
	song varchar,
	status bigint,
	ts bigint,
	useragent varchar,
	userid bigint
);

CREATE TABLE IF NOT EXISTS staging_songs (
	num_songs int,
	artist_id varchar,
	artist_name varchar,
	artist_latitude numeric,
	artist_longitude numeric,
	artist_location varchar,
	song_id varchar,
	title varchar,
	duration numeric,
	"year" int
);


CREATE TABLE IF NOT EXISTS songs (
	songid varchar NOT NULL,
	title varchar,
	artistid varchar,
	"year" int,
	duration numeric,
	CONSTRAINT songs_pkey PRIMARY KEY (songid)
);

DROP TABLE songplays;
CREATE TABLE IF NOT EXISTS songplays (
	songplay_id varchar NOT NULL,
	start_time timestamp NOT NULL,
	userid int NOT NULL,
	"level" varchar,
	songid varchar,
	artistid varchar,
	sessionid int,
	location varchar,
	user_agent varchar,
	CONSTRAINT songplays_pkey PRIMARY KEY (songplay_id)
);

CREATE TABLE IF NOT EXISTS artists (
	artistid varchar NOT NULL,
	name varchar,
	location varchar,
	lattitude numeric,
	longitude numeric
);

CREATE TABLE IF NOT EXISTS users (
	userid int NOT NULL,
	first_name varchar,
	last_name varchar,
	gender varchar,
	"level" varchar,
	CONSTRAINT users_pkey PRIMARY KEY (userid)
);


CREATE TABLE IF NOT EXISTS artists (
	artistid varchar NOT NULL,
	name varchar,
	LOCATION varchar,
	lattitude numeric,
	longitude numeric
);

CREATE TABLE IF NOT EXISTS "time" (
	start_time timestamp NOT NULL,
	"hour" int,
	"day" int,
	week int,
	"month" varchar,
	"year" int,
	weekday varchar,
	CONSTRAINT time_pkey PRIMARY KEY (start_time)
);