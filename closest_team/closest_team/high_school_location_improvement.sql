select concat(name, " high school, ", city, " ", state) 
from high_school_t;

alter table high_school_t 
add column `latitude2` double,
add column `longitude2` double,
add column `full_address` varchar(100);

update high_school_t
set longitude = longitude2,
	latitude = latitude2;

alter table high_school_t
drop column `latitude2`,
drop column `longitude2`;