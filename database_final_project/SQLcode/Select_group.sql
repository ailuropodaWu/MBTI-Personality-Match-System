select 
	study_group,
	cast(count(study_group) as float) * 100 / 
		(select count(index) from matched_index natural join study)
		as percentage
from matched_index natural join study
group by study_group
order by percentage desc