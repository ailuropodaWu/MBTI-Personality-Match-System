create or replace view matched_mbti as
(
	select suitable_mbti
	from mbti_match
	where asked_mbti = 'ENFP'
);

create or replace view matched_index as
(
	select index, matched_mbti
	from subject natural join test_result, matched_mbti
	where age between 19 - 2 and 19 + 2 and 
	gender = '女' and mbti_result = suitable_mbti
);
