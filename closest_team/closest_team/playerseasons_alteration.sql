select * from player_seasons;

truncate table player_seasons;

select coalesce(scoring_av, ''), coadefense_av, kicking_av,
passing_av,receiving_and_rushing_av,returns_av, scoring_av) av
from player_seasons
limit 10;


select count(*),
IFNULL(scoring_av IS NOT NULL, 0) +
IFNULL(defense_av IS NOT NULL, 0) +
IFNULL(kicking_av IS NOT NULL, 0) +
IFNULL(passing_av IS NOT NULL, 0) +
IFNULL(receiving_and_rushing_av IS NOT NULL, 0) +
IFNULL(returns_av IS NOT NULL, 0) num_fields
from player_seasons
group by num_fields;

select scoring_av, defense_av, kicking_av,
passing_av,receiving_and_rushing_av,returns_av
from player_seasons
where IFNULL(scoring_av IS NOT NULL, 0) +
IFNULL(defense_av IS NOT NULL, 0) +
IFNULL(kicking_av IS NOT NULL, 0) +
IFNULL(passing_av IS NOT NULL, 0) +
IFNULL(receiving_and_rushing_av IS NOT NULL, 0) +
IFNULL(returns_av IS NOT NULL, 0) = 2;

alter table player_seasons add column `av` int(11) default null;

update player_seasons
	set av = coalesce(defense_av, kicking_av,
	passing_av, receiving_and_rushing_av, returns_av, scoring_av);

select count(*) 
from player_seasons
where av is null;

select p.name 
from players_t p join player_seasons ps on p.pfr_player_id = ps.player_id
limit 10;

alter table player_seasons add column `pfr_player_id` VARCHAR(10) NOT NULL;

update player_seasons
set pfr_player_id = player_id;



alter table player_seasons 
modify column `player_id` VARCHAR(20) DEFAULT NULL;

update player_seasons
set player_id = NULL;

alter table player_seasons 
modify column `player_id` INT(11);

alter table players_t modify column `pfr_player_id` VARCHAR(10) NOT NULL;

alter table players_t add unique key `pfr_player_id_idx` (`pfr_player_id`);

alter table player_seasons add index `pfr_player_id_idx` (`pfr_player_id`);

update player_seasons ps join players_t p on p.pfr_player_id = ps.pfr_player_id
set ps.player_id = p.player_t_id;

alter table player_seasons 
modify column `player_id` INT(11) NOT NULL;

select count(*) from player_seasons;

select player_id from player_seasons where player_id is not null limit 10;

select MAX(LENGTH(pfr_player_id)) from players_t;

select  `scoring_team`,
        `scoring_playoffs_team`,
        `returns_team`,
        `returns_playoffs_team`,
        `receiving_and_rushing_team`,
        `receiving_and_rushing_playoffs_team`,
        `passing_team`,
        `passing_playoffs_team`,
        `passing_advanced_team`,
        `kicking_team`,
        `defense_team`,
        `defense_playoffs_team`
from player_seasons        
limit 10;



select count(1), length(`year`) len from player_seasons group by len; 

select `year`, SUBSTRING(`year`, 1, 4) subs from player_seasons where length(`year`) > 4;

alter table player_seasons add column all_pro bool;

alter table player_seasons add column pro_bowl bool;

update player_seasons
set `year` = SUBSTRING(`year`, 1, 4) 
where length(`year`) > 4;

select `year`
from player_seasons
where year like "%*";

alter table player_seasons modify column `year` int(11);


select count(*),
IFNULL(`scoring_team` IS NOT NULL, 0) +
IFNULL(`scoring_playoffs_team` IS NOT NULL, 0) +
IFNULL(`returns_team` IS NOT NULL, 0) +
IFNULL(`returns_playoffs_team` IS NOT NULL, 0) +
IFNULL(`receiving_and_rushing_team` IS NOT NULL, 0) +
IFNULL(`receiving_and_rushing_playoffs_team` IS NOT NULL, 0) +
IFNULL(`passing_team` IS NOT NULL, 0) +
IFNULL(`passing_playoffs_team` IS NOT NULL, 0) +
IFNULL(`passing_advanced_team` IS NOT NULL, 0) +
IFNULL(`kicking_team` IS NOT NULL, 0) +
IFNULL(`defense_team` IS NOT NULL, 0) +
IFNULL(`defense_playoffs_team` IS NOT NULL, 0) num_fields
from player_seasons
group by num_fields;

 select `scoring_playoffs_team`,
`returns_team`,
`returns_playoffs_team`,
`receiving_and_rushing_team`,
`receiving_and_rushing_playoffs_team`
`passing_team`,
`passing_playoffs_team`,
`passing_advanced_team`,
`kicking_team`,
`defense_team`,
`defense_playoffs_team`
from player_seasons
where IFNULL(`scoring_team` IS NOT NULL, 0) +
IFNULL(`scoring_playoffs_team` IS NOT NULL, 0) +
IFNULL(`returns_team` IS NOT NULL, 0) +
IFNULL(`returns_playoffs_team` IS NOT NULL, 0) +
IFNULL(`receiving_and_rushing_team` IS NOT NULL, 0) +
IFNULL(`receiving_and_rushing_playoffs_team` IS NOT NULL, 0) +
IFNULL(`passing_team` IS NOT NULL, 0) +
IFNULL(`passing_playoffs_team` IS NOT NULL, 0) +
IFNULL(`passing_advanced_team` IS NOT NULL, 0) +
IFNULL(`kicking_team` IS NOT NULL, 0) +
IFNULL(`defense_team` IS NOT NULL, 0) +
IFNULL(`defense_playoffs_team` IS NOT NULL, 0) > 7;

alter table `player_seasons` add index `player_id_idx` (`player_id`);

alter table `players_t` add column `weighted_av` FLOAT;

select name, weighted_av from players_t where weighted_av is not null order by weighted_av desc;



SELECT `t1`.`player_t_id`, `t1`.`pfr_high_school_id`,
`t1`.`high_school_t_id`, `t1`.`birthday`, `t1`.`birthplace`, `t1`.`birth_city`,
`t1`.`birth_state`, `t1`.`college`, `t1`.`high_school`, `t1`.`name`,
`t1`.`pfr_player_id`, `t1`.`url`, `t1`.`birthday_date`, `t1`.`weighted_av`,
`t2`.`av`, `t2`.`year` FROM `players_t` AS t1 JOIN `player_seasons`
AS t2 ON (`t1`.`player_t_id` = `t2`.`player_id`) WHERE `t2`.`av` IS NOT NULL
AND `t2`.`year` IS NOT NULL AND `t1`.`birthday_date` is not null ORDER BY `t1`.`birthday_date` desc LIMIT 1000