
alter table high_school_t add column coordinates POINT;

update high_school_t
set coordinates = point(longitude, latitude)
where longitude is not null and latitude is not null;

alter table stadiums add column coordinates POINT;

update stadiums
set coordinates = point(longitude, latitude)
where longitude is not null and latitude is not null;

create table hs_s_distance as 
select s.stadium_id as `stadium_id`, hs.high_school_t_id as `high_school_t_id`, 
		3959 * asin(
			sqrt(
				power(
					sin((y(s.coordinates) - y(hs.coordinates)) * pi()/180/2), 2
				) + 
				cos(y(s.coordinates) * pi()/180) * 
				cos(y(hs.coordinates) * pi()/180) * 
				power( 
					sin((x(s.coordinates) - x(hs.coordinates)) * pi()/180/2), 2
				)
			)
		) as `distance`
from stadiums s, high_school_t hs;

update high_school_t set closest_stadium_id = null;

update high_school_t hs
	left join 
	(
		select hsd.high_school_t_id as `hs_id`, hsd.stadium_id as `s_id`
		from hs_s_distance hsd
			inner join
			(
				select d.high_school_t_id as `hs_id`, min(d.distance) `distance`
				from hs_s_distance d
				group by d.high_school_t_id
			) b on hsd.high_school_t_id = b.hs_id and
				hsd.distance = b.distance
	) s on s.hs_id = hs.high_school_t_id
set hs.closest_stadium_id = s.s_id;

drop table hs_s_distance;
