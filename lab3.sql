
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS movie_theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS screenings;

PRAGMA foreign_keys = ON;

CREATE TABLE customers(
	customer_username  TEXT,
	full_name  TEXT,
	password  TEXT,
	PRIMARY KEY (customer_username)
);

CREATE TABLE movies(
	imdb_key  TEXT,
	title  TEXT,
	production_year  INTEGER NOT NULL,
	runtime  INTEGER,
	PRIMARY KEY (imdb_key)
);

CREATE TABLE tickets(
	ticket_id  TEXT DEFAULT (lower(hex(randomblob(16)))),
	screening_id,
	customer_username TEXT,
	FOREIGN KEY (screening_id) REFERENCES screenings(screening_id),
	FOREIGN KEY (customer_username) REFERENCES customers(customer_username),
	PRIMARY KEY(ticket_id)
);

CREATE TABLE screenings(
	screening_id  TEXT DEFAULT (lower(hex(randomblob(16)))),
	imdb_key  TEXT,
	screening_time  TIME,
	screening_date DATE,
	movie_theater_name  TEXT,
	FOREIGN KEY (imdb_key) REFERENCES movies(imdb_key),
	FOREIGN KEY (movie_theater_name) REFERENCES movie_theaters(movie_theater_name),
	PRIMARY KEY (screening_id)
);

CREATE TABLE movie_theaters(
	movie_theater_name  TEXT,
	capacity  INTEGER NOT NULL CHECK (capacity > 0),
	movie_theater_chain TEXT,
	PRIMARY KEY (movie_theater_name)
);
-- Populate the students table.

INSERT
INTO   customers (customer_username, full_name, password)
VALUES ('coolusername1234', 'Anna Larsson', 'safepassword123'),
       ('movielover69', 'Gunnar Persson', 'Mittbarn18'),
       ('nicecinema', 'Britt-Marie Forfan', 'körabilärkul'),
       ('annas_filmserie', 'Olof Persson', 'vemaranna');

INSERT
INTO movie_theaters(movie_theater_name, capacity, movie_theater_chain)
VALUES	('24/7cinema', 4, '24/7'),
	('disney--', 2, 'internetcinemas') ,
	('coolcinema', 6, 'internetcinemas'),
	('thepiratebae', 2, 'sketchybios'),
	('netflix_and_chill_cinema', '112', 'internetcinemas');

INSERT
INTO movies(title, production_year, imdb_key, runtime)
VALUES  ('The Room', 2003, 'tt0368226', 99),
        ('The Disaster Artist', 2017, 'tt3521126', 104),
        ('Captain Fantastic', 2016, 'tt3553976', 118),
        ("Don't look up", 2021, 'tt11286314', 138);

INSERT
INTO screenings(movie_theater_name, imdb_key ,screening_date, screening_time)
VALUES  ('24/7cinema', 'tt0368226', '2022-02-01', '19:30'),
        ('disney--',"tt11286314", '2022-02-03', '19:00'),
        ('disney--',"tt11286314", '2022-02-04', '21:00'),
        ('disney--',"tt11286314", '2022-02-03', '21:00'),
        ('24/7cinema',"tt11286314", '2022-02-03', '19:15'),
        ('coolcinema','tt0368226', '2022-02-03', '19:30'),
        ('coolcinema', 'tt3521126', '2022-02-03', '21:30'),
        ('thepiratebae','tt0368226', '2022-02-05', '12:00'),
        ('thepiratebae', 'tt3521126', '2022-02-02', '19:30'),
        ('thepiratebae',"tt11286314", '2022-02-04', '19:30'),
        ('thepiratebae', 'tt3553976', '2022-02-06', '19:30'),
        ('netflix_and_chill_cinema','tt3553976','2022-02-03', '18:30'),
        ('netflix_and_chill_cinema',"tt11286314", '2022-02-04', '18:30');

INSERT
INTO tickets(screening_id, customer_username)
SELECT screening_id, 'movielover69'
FROM screenings
        

