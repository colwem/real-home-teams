drop table if exists players_t;
drop table if exists high_school_t;

create table high_school_t
(city varchar(100),
state varchar(100),
pfr_high_school_id varchar(15) unique key,
`name` varchar(200));

load data local infile '/Users/ColwellBC/workshop/closest-team/closest_team/closest_team/csv/school.csv'
into table high_school_t
fields terminated by ',' enclosed by '"'
lines terminated by '\r\n'
ignore 1 lines;

create table players_t 
(birthplace varchar(200),
`name` varchar(100),
url varchar(300),
birthday varchar(400),
college varchar(300),
pfr_player_id varchar(40),
high_school varchar(300),
pfr_high_school_id varchar(40));

load data local infile '/Users/ColwellBC/workshop/closest-team/closest_team/closest_team/csv/player.csv'
into table players_t
fields terminated by ',' enclosed by '"'
lines terminated by '\r\n'
ignore 1 lines;

ALTER TABLE `players_t` 
    add column `player_t_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT FIRST,
	add column `birth_city` varchar(40),
	add column `birth_state` varchar(40);

ALTER TABLE `high_school_t` 
    add column `high_school_t_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT FIRST,
	add column `country` varchar(40),
	add column `url` varchar(300),
	add column `latitude` double,
    add column `longitude` double;

ALTER TABLE `high_school_t` 
	add column `latitude` float(20),
    add column `longitude` float(20);

Alter table `players_t`
	add column `high_school_t_id` int(11);

UPDATE players_t pt 
    JOIN high_school_t hst ON pt.pfr_high_school_id = hst.pfr_high_school_id 
SET pt.high_school_t_id = hst.high_school_t_id;

update `high_school_t`
set name='Mt. Juliet',
	city='Mt. Juliet',
	state='Tennessee'
where pfr_high_school_id='93ba10f3';

update `high_school_t`
set name=null,
	city=null,
	state=null,
	country='England'
where pfr_high_school_id='93bf78ad';

update `high_school_t`
set name=null,
	city=null,
	state=null,
	country='Canada'
where pfr_high_school_id='93be1a52';

update `high_school_t`
set name='St. Joseph\'s',
	city=null,
	state=null,
	country='Canada'
where pfr_high_school_id='93be6a5a';

update `high_school_t`
set name='Kilpatrick School',
	city=null,
	state=null,
	country='Panama'
where pfr_high_school_id='93bb6a4a';

update high_school_t
set country = state,
    state = null
where state in ( 'Panama Canal Zone', 
    'Austria', 
    'Bolivia', 
    'Cyprus', 
    'Ireland', 
    'Virgin Islands', 
    'Tonga', 
    'Czech Republic', 
    'Panama', 
    'Kenya', 
    'Croatia', 
    'Elkhorn', 
    'Italy', 
    'South Africa', 
    'Estonia', 
    'South Korea', 
    'Brazil', 
    'New Zealand', 
    'France', 
    'Bahamas', 
    'Barbados', 
    'Denmark', 
    'Wales', 
    'Mexico', 
    'Spain', 
    'Sweden', 
    'Norway', 
    'Japan', 
    'Nigeria', 
    'American Samoa', 
    'England', 
    'Australia', 
    'Germany', 
    'Canada');

update high_school_t
set country = 'USA'
where country is null;

update high_school_t h
set h.url = concat(
	'http://www.pro-football-reference.com/schools/high_schools.cgi?id=',
	h.pfr_high_school_id);

Alter table `high_school_t`
	modify column `latitude` double,
    modify column `longitude` double;

Alter table `high_school_t`
	modify column name varchar(50),
    modify column state varchar(21),
    modify column city varchar(30), 
	modify column pfr_high_school_id varchar(9),
	modify column country varchar(20),
	modify column url varchar(80);

drop table if exists stadiums;

create table stadiums
(   name varchar(200),
    team varchar(300),
    location varchar(300)
);

load data local infile '/Users/ColwellBC/workshop/closest-team/closest_team/closest_team/wikipedia_stadium_list.csv'
into table stadiums
fields terminated by ',' enclosed by '"'
lines terminated by '\r\n'
ignore 1 lines;

alter table stadiums
	add column stadium_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT FIRST,
	add column latitude double,
    add column longitude double;

select * 
from stadiums;






select count(1) as `done` , 9677 - count(1) as `left` , count(1) / 9677.0 as `pct`
from high_school_t
where closest_stadium_id is not null;

select count(1)
from high_school_t;

select * from players_t;