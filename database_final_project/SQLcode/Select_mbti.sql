select 
	cast(count(index) as float) * 100 / (select count(index) from subject) 
			as percentage
from matched_index;
/*
//show the detail about how the matched mbti distributing

select
	matched_mbti, 
	cast(count(matched_mbti) as float) * 100 / (select count(index) from matched_index)
		as percentage
from matched_index
group by matched_mbti
order by percentage desc
*/
