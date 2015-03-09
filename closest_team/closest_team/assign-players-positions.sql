
alter table players_t add column `pos` varchar(100);

alter table players_t add index `players_t_pos_idx` (`pos`);

alter table players_t add index `players_t_high_school_t_id_idx` (`high_school_t_id`);