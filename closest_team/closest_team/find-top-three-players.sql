create table stadium_player_positions (
	stadium_player_position_id int(11) primary key auto_increment,
	player_t_id int(11),
	stadium_id int(11),
	position_id int(11),
	ord int(1));

create table positions (
	position_id int(11) primary key auto_increment,
	name varchar(20));


update players_t
set pos = upper(pos);

insert into positions (name) values
('DE'),
('DT'),
('CB'),
('SS'),
('FS'),
('QB'),
('RB'),
('WR'),
('T'),
('G'),
('C');

select pt.name, pt.pos, s.team, spp.ord
from stadium_player_positions spp
	inner join players_t pt on spp.player_t_id = pt.player_t_id
	inner join stadiums s on spp.stadium_id = s.stadium_id;

truncate stadium_player_positions;