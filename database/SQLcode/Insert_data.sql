insert into area(area)
select distinct area
from reply;

insert into hometown(num, area)
select distinct num, area 
from reply;

insert into school(school_name, study_group)
select distinct school_name, study_group
from reply;

insert into study(num, school_name, study_group)
select distinct num, school_name, study_group
from reply;

insert into star_sign(star_sign)
select distinct star_sign
from reply;

insert into subject_star_sign(num, star_sign)
select distinct num, star_sign 
from reply;

insert into subject(num, email, gender, age)
select distinct num, email, gender, age
from reply;

insert into test_result(num, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11,
						q12, q13, q14, q15, q16, mbti_result)
select distinct num, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13,
				q14, q15, q16, mbti_result
from reply