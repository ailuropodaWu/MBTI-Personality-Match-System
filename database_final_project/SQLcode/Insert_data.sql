insert into area(area)
select distinct area
from reply;

insert into hometown(index, area)
select distinct index, area 
from reply;

insert into school(school_name, study_group)
select distinct school_name, study_group
from reply;

insert into study(index, school_name, study_group)
select distinct index, school_name, study_group
from reply;

insert into star_sign(star_sign)
select distinct star_sign
from reply;

insert into subject_star_sign(index, star_sign)
select distinct index, star_sign 
from reply;

insert into subject(index, email, gender, age)
select distinct index, email, gender, age
from reply;

insert into test_result(index, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11,
						q12, q13, q14, q15, q16, mbti_result)
select distinct index, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13,
				q14, q15, q16, mbti_result
from reply