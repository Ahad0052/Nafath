DROP DATABASE IF EXISTS MOVIE_DB;
CREATE DATABASE MOVIE_DB1;
USE MOVIE_DB1;

CREATE TABLE PROD (
  P_ID INT PRIMARY KEY,
  PNAME VARCHAR(50),
  ADDRESS VARCHAR(100)
);

DESCRIBE PROD;

CREATE TABLE Moviec (
  M_ID INT PRIMARY KEY,
  actor_ID VARCHAR(50),
  rol VARCHAR(100),
  PID INT,
  status1 VARCHAR(20) DEFAULT 'active'
);
alter table Moviec add column title varchar(700);
alter table Moviec add constraint con unique(title);
ALTER TABLE Moviec 
ADD CONSTRAINT fk_prod FOREIGN KEY (PID) REFERENCES PROD(P_ID) ON DELETE CASCADE;

DESCRIBE Moviec;

CREATE TABLE gener (
  gener_id INT,
  name1 VARCHAR(50),
  CONSTRAINT pk_gener PRIMARY KEY (gener_id)
);

DESCRIBE gener;

CREATE TABLE actor (
  actor_id INT PRIMARY KEY,
  age int,
  name1 VARCHAR(50),
  dob DATE
);
alter table actor add constraint c check (age > 0);

ALTER TABLE actor 
MODIFY actor_id  int NOT NULL;

CREATE TABLE director (
  director_id INT PRIMARY KEY,
  name1 VARCHAR(50),
  dob DATE,
  act VARCHAR(50) 
);

CREATE TABLE movie_gener (
  generid INT,
  movieid INT,
  CONSTRAINT fk_mg1 FOREIGN KEY (generid) REFERENCES gener(gener_id) ON DELETE CASCADE,
  CONSTRAINT fk_mg2 FOREIGN KEY (movieid) REFERENCES Moviec(M_ID) ON DELETE CASCADE
);

CREATE TABLE movie_director (
  dirid INT,
  mid INT,
  role1 VARCHAR(70),
  CONSTRAINT fk_md1 FOREIGN KEY (dirid) REFERENCES director(director_id) ON DELETE CASCADE,
  CONSTRAINT fk_md2 FOREIGN KEY (mid) REFERENCES Moviec(M_ID) ON DELETE CASCADE
);

CREATE TABLE movie_actor (
  actid INT,
  moid INT,
  role1 VARCHAR(70),
  CONSTRAINT fk_ma1 FOREIGN KEY (actid) REFERENCES actor(actor_id) ON DELETE CASCADE,
  CONSTRAINT fk_ma2 FOREIGN KEY (moid) REFERENCES Moviec(M_ID) ON DELETE CASCADE
);


CREATE TABLE quots (
  actid INT,
  moid INT,
  text1 VARCHAR(70),
  CONSTRAINT fk_q1 FOREIGN KEY (actid) REFERENCES actor(actor_id) ON DELETE CASCADE,
  CONSTRAINT fk_q2 FOREIGN KEY (moid) REFERENCES Moviec(M_ID) ON DELETE CASCADE
);

SELECT name1, dob, (YEAR(CURDATE()) - YEAR(dob)) AS age FROM actor;

SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'MOVIE_DB1';

show tables; 
-- comment

ALTER TABLE actor MODIFY actor_id INT AUTO_INCREMENT;

use movie_db1;
ALTER TABLE actor ADD INDEX idx_name (age);


insert into prod
values (100, 'netflix','la');

insert into prod
(P_ID,PNAME,ADDRESS)
values (101, 'netflix','la');

SELECT * FROM PROD;

INSERT INTO actor
values (201,36,"michiel",'1999-09-11');
select * from actor;

INSERT INTO actor
values (202,30,"s",'1999-09-11');
select * from actor;

INSERT INTO director
values (300,"steve",'1967-01-11','direct only'),
(301,"donald",'1979-11-14','direct only');
select * from director;

INSERT INTO gener
values (400,"comedy"),
(401,"drama");
select * from gener;

INSERT INTO moviec
values (500,200,'teacher',100,"ongoing","sss"),
(501,201,'teacher',101,"ongoing","xxx");
select * from moviec;

INSERT INTO movie_actor
values(200,500,"homeless"),
(201,501,"good");
select * from movie_actor;

insert into movie_director
values(300,500,"directing"),
(301,501,"directing");
select * from movie_director;

insert into movie_gener
values(400,500),
(401,501);
select * from movie_gener;

insert into quots
values(200,500,"hello world"),
(201,501,"hi");
select * from quots;

update actor 
set age = 5
where actor_id = 200;

select * from actor;

update actor
set name1 = 'someone'
where actor_id in (202);
select * from actor;

use movie_db1;

update actor
set age = 4
where age in (30);
select * from actor;

select p_id,pname from prod;

select p_id as prod_ID from prod;
select * from prod;

select name1,age + 5 as  newage from actor;

