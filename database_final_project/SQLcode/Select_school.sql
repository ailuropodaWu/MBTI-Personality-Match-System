select 
	school_name,
	cast(count(school_name) as float) * 100 / 
		(select count(index) from matched_index natural join study)
		as percentage
from matched_index natural join study
group by school_name
order by percentage desc