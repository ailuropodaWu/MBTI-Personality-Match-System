select 
	star_sign,
	cast(count(star_sign) as float) * 100 / 
		(select count(index) from matched_index natural join subject_star_sign)
		as percentage
from matched_index natural join subject_star_sign
group by star_sign
order by percentage desc