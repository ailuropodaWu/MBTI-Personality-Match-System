select 
	school_name, study_group,
	cast(count(school_name) as float) * 100 / 
		(select count(index) from matched_index natural join study)
		as percentage
from matched_index natural join study
group by school_name, study_group
order by percentage desc