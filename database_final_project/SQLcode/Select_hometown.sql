select 
	area,
	cast(count(area) as float) * 100 / 
		(select count(index) from matched_index natural join hometown)
		as percentage
from matched_index natural join hometown 
group by area
order by percentage desc