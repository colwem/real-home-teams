DROP TABLE IF EXISTS `espn_depth_positions`;
DROP TABLE IF EXISTS `espn_roster_players`;

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

create index ps_player_id_uniform_number_idx on player_seasons (player_id, uniform_number);
create index erp_name_idx on espn_roster_players (name);
create index p_name_idx on players_t (name);

update players_t set pos = null;
alter table players_t add column active bool default false;

update players_t p1
	join (	select distinct rp.pos as `pos`, rp.name, p.player_t_id as `id`
			from espn_roster_players rp 
				join players_t p 
					on p.name = rp.name
				join player_seasons ps 
					on ps.player_id = p.player_t_id 
						and ps.uniform_number = rp.no) jp
		on jp.id = p1.player_t_id
set p1.pos = jp.pos,
	p1.active = true;
    
select name, pos, weighted_av
from players_t
where active is true
order by weighted_av desc;

select ps.*
from player_seasons ps
	join players_t p on p.player_t_id = ps.player_id
where p.name = 'Adrian Peterson';

select distinct pos
from players_t
order by pos;