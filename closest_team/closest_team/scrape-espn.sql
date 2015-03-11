select p.college
from players_t p
	join player_seasons ps on ps.player_id = p.player_t_id
where ps.year = 2014;

CREATE TABLE `espn_roster_players` (
`espn_roster_player_id` INTEGER AUTO_INCREMENT PRIMARY KEY,
`name`                 VARCHAR(27) NOT NULL,
`team`                 VARCHAR(3) NOT NULL,
`pos`                  VARCHAR(2) NOT NULL,
`age`                  VARCHAR(2) NOT NULL,
`college`              VARCHAR(30) NOT NULL,
`exp`                  INTEGER NOT NULL,
`ht`                   INTEGER NOT NULL,
`no`                   INTEGER DEFAULT NULL,
`wt`                   INTEGER NOT NULL);

CREATE TABLE `espn_depth_positions` (
`espn_depth_position_id` INTEGER AUTO_INCREMENT PRIMARY KEY,
`team`                 VARCHAR(3) NOT NULL,
`formation`             VARCHAR(13) NOT NULL,
`position`              VARCHAR(4) NOT NULL,
`starter`               VARCHAR(27) NOT NULL,
`second`                   VARCHAR(23) DEFAULT NULL,
`third`                   VARCHAR(20) DEFAULT NULL,
`fourth`                   VARCHAR(20) DEFAULT NULL);

DROP TABLE `espn_depth_positions`;
DROP TABLE `espn_roster_players`;

select count(*) 
from espn_roster_players
where pos = 'DB';

select * 
from players_t
where name like "%Peterson%";

select *
from player_seasons
where player_id = 1046;

select * 
from players_t
limit 100;