select pt.name,
	pt.high_school,
	pt.birthplace,
	hst.name,
	pt.pfr_high_school_id,
	hst.pfr_high_school_id,
	hst.city,
	hst.state
FROM players_t pt 
	JOIN high_school_t hst 
		ON pt.high_school_t_id = hst.high_school_t_id;

select * 
from `high_school_t`
where not `city` > '';