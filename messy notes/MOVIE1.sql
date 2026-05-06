
CREATE DATABASE MOVIE_DB2;
USE MOVIE_DB2;

-- =========================
-- TABLE: PROD
-- =========================
CREATE TABLE PROD (
  P_ID INT PRIMARY KEY,
  PNAME VARCHAR(50),
  ADDRESS VARCHAR(100)
);

INSERT INTO PROD VALUES
(100,'Netflix','USA'),
(101,'Amazon Prime','USA'),
(102,'Disney+','USA'),
(103,'HBO Max','USA'),
(104,'Apple TV','USA'),
(105,'Hulu','USA'),
(106,'Sony Pictures','USA'),
(107,'Warner Bros','USA'),
(108,'Universal','USA'),
(109,'Paramount','USA');

-- =========================
-- TABLE: ACTOR
-- =========================
CREATE TABLE actor (
  actor_id INT PRIMARY KEY,
  age INT,
  name1 VARCHAR(50),
  dob DATE
);

INSERT INTO actor VALUES
(201,34,'John Carter','1991-02-11'),
(202,29,'Mike Ross','1996-05-21'),
(203,40,'Steve Hill','1985-09-01'),
(204,31,'David Stone','1994-03-12'),
(205,27,'Chris Evan','1998-07-19'),
(206,36,'Robert King','1989-11-30'),
(207,45,'Tom Hardy','1980-01-15'),
(208,28,'Alex White','1997-06-22'),
(209,33,'James Bond','1992-08-09'),
(210,38,'Bruce Wayne','1987-12-25');

-- =========================
-- TABLE: DIRECTOR
-- =========================
CREATE TABLE director (
  director_id INT PRIMARY KEY,
  name1 VARCHAR(50),
  dob DATE,
  act VARCHAR(50)
);

INSERT INTO director VALUES
(301,'Steven Spielberg','1960-12-01','Direct only'),
(302,'Christopher Nolan','1970-07-30','Direct only'),
(303,'James Cameron','1955-08-16','Direct only'),
(304,'Quentin Tarantino','1963-03-27','Direct only'),
(305,'Martin Scorsese','1942-11-17','Direct only'),
(306,'Ridley Scott','1937-02-12','Direct only'),
(307,'Peter Jackson','1961-10-31','Direct only'),
(308,'Denis Villeneuve','1967-05-03','Direct only'),
(309,'Guy Ritchie','1968-09-10','Direct only'),
(310,'Tim Burton','1958-08-25','Direct only');

-- =========================
-- TABLE: GENER
-- =========================
CREATE TABLE gener (
  gener_id INT PRIMARY KEY,
  name1 VARCHAR(50)
);

INSERT INTO gener VALUES
(400,'Comedy'),
(401,'Drama'),
(402,'Action'),
(403,'Sci-Fi'),
(404,'Horror'),
(405,'Romance'),
(406,'Thriller'),
(407,'Fantasy'),
(408,'Adventure'),
(409,'Mystery');

-- =========================
-- TABLE: MOVIEC
-- =========================
CREATE TABLE Moviec (
  M_ID INT PRIMARY KEY,
  actor_ID VARCHAR(50),
  rol VARCHAR(100),
  PID INT,
  status1 VARCHAR(20) DEFAULT 'active',
  title VARCHAR(700) UNIQUE,
  FOREIGN KEY (PID) REFERENCES PROD(P_ID) ON DELETE CASCADE
);

INSERT INTO Moviec VALUES
(500,'201','Hero',100,'active','The Last Mission'),
(501,'202','Detective',101,'active','City Lights'),
(502,'203','Villain',102,'active','Dark Empire'),
(503,'204','Teacher',103,'active','School of Life'),
(504,'205','Agent',104,'active','Secret Code'),
(505,'206','Doctor',105,'active','Healing Hands'),
(506,'207','Soldier',106,'active','War Zone'),
(507,'208','Student',107,'active','Future World'),
(508,'209','Spy',108,'active','Hidden Truth'),
(509,'210','Boss',109,'active','Gotham Nights');

-- =========================
-- TABLE: MOVIE_ACTOR
-- =========================
CREATE TABLE movie_actor (
  actid INT,
  moid INT,
  role1 VARCHAR(70),
  FOREIGN KEY (actid) REFERENCES actor(actor_id) ON DELETE CASCADE,
  FOREIGN KEY (moid) REFERENCES Moviec(M_ID) ON DELETE CASCADE
);

INSERT INTO movie_actor VALUES
(201,500,'Lead'),
(202,501,'Detective'),
(203,502,'Villain'),
(204,503,'Teacher'),
(205,504,'Agent'),
(206,505,'Doctor'),
(207,506,'Soldier'),
(208,507,'Student'),
(209,508,'Spy'),
(210,509,'Boss');

-- =========================
-- TABLE: MOVIE_DIRECTOR
-- =========================
CREATE TABLE movie_director (
  dirid INT,
  mid INT,
  role1 VARCHAR(70),
  FOREIGN KEY (dirid) REFERENCES director(director_id) ON DELETE CASCADE,
  FOREIGN KEY (mid) REFERENCES Moviec(M_ID) ON DELETE CASCADE
);

INSERT INTO movie_director VALUES
(301,500,'Directed'),
(302,501,'Directed'),
(303,502,'Directed'),
(304,503,'Directed'),
(305,504,'Directed'),
(306,505,'Directed'),
(307,506,'Directed'),
(308,507,'Directed'),
(309,508,'Directed'),
(310,509,'Directed');

-- =========================
-- TABLE: MOVIE_GENER
-- =========================
CREATE TABLE movie_gener (
  generid INT,
  movieid INT,
  FOREIGN KEY (generid) REFERENCES gener(gener_id) ON DELETE CASCADE,
  FOREIGN KEY (movieid) REFERENCES Moviec(M_ID) ON DELETE CASCADE
);

INSERT INTO movie_gener VALUES
(400,500),
(401,501),
(402,502),
(403,503),
(404,504),
(405,505),
(406,506),
(407,507),
(408,508),
(409,509);

-- =========================
-- TABLE: QUOTS
-- =========================
CREATE TABLE quots (
  actid INT,
  moid INT,
  text1 VARCHAR(70),
  FOREIGN KEY (actid) REFERENCES actor(actor_id) ON DELETE CASCADE,
  FOREIGN KEY (moid) REFERENCES Moviec(M_ID) ON DELETE CASCADE
);

INSERT INTO quots VALUES
(201,500,'I will return'),
(202,501,'Truth wins'),
(203,502,'Power is everything'),
(204,503,'Learn and grow'),
(205,504,'Mission accepted'),
(206,505,'Save lives'),
(207,506,'Never give up'),
(208,507,'Dream big'),
(209,508,'Stay hidden'),
(210,509,'I am the night');

-- =========================
-- QUICK TEST
-- =========================
SELECT * FROM PROD;
SELECT * FROM actor;
SELECT * FROM director;
SELECT * FROM gener;
SELECT * FROM Moviec;

select distinct age,name1 from actor;

select distinct address from prod;

select * from moviec limit 5;

select  * from actor where age >30;

select  * from actor where age >30 and age < 40;

select  * from actor where age between 30 and 40;

select * from actor where actor_id > any (select actor_id from actor where actor_id in (204,206,209));

select * from actor where name1 like '_a%'; 

select * from actor where name1 is not null;

select * from actor order by age asc;

select * from actor order by age asc, name1 desc;
ALTER TABLE Moviec
ADD COLUMN duration INT;

select year1 from moviec;
UPDATE Moviec SET duration = 120 WHERE M_ID = 500;
UPDATE Moviec SET duration = 110 WHERE M_ID = 501;
UPDATE Moviec SET duration = 130 WHERE M_ID = 502;
UPDATE Moviec SET duration = 140 WHERE M_ID = 503;
UPDATE Moviec SET duration = 150 WHERE M_ID = 504;
UPDATE Moviec SET duration = 160 WHERE M_ID = 505;
UPDATE Moviec SET duration = 170 WHERE M_ID = 506;
UPDATE Moviec SET duration = 190 WHERE M_ID = 507;

ALTER TABLE Moviec
ADD COLUMN year1 year;

UPDATE Moviec SET year1 = 2014 WHERE M_ID = 500;
UPDATE Moviec SET year1 = 2015 WHERE M_ID = 501;
UPDATE Moviec SET year1 = 2016 WHERE M_ID = 502;
UPDATE Moviec SET year1 = 2014 WHERE M_ID = 503;
UPDATE Moviec SET year1 = 2014 WHERE M_ID = 504;
UPDATE Moviec SET year1 = 2014 WHERE M_ID = 505;
UPDATE Moviec SET year1 = 2013 WHERE M_ID = 506;
UPDATE Moviec SET year1 = 2000 WHERE M_ID = 507;

-- Find movies whose duration is greater than ALL movies released in 2014.
select duration from Moviec 
where duration > all (select duration from Moviec where year1 = 2014); 

-- Find movies that have NOT been acted in by "Steve Hill"
select moid from movie_actor
where actid not ;

-- Retrieve movies whose duration is greater than ANY Sci-Fi movie duration.

-- 8-Find movies that have no genre assigned.


-- Retrieve movies that feature both Actor 1 and Actor 2 in the same movie (without JOIN)
SELECT moid
FROM movie_actor
WHERE actid = 100
AND moid IN (
    SELECT moid
    FROM movie_actor
    WHERE actid = 201
);

select * from movie_actor;
select * from actor ;
select * from movie_actor;