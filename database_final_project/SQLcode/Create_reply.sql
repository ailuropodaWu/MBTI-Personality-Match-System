drop table if exists reply cascade;
drop table if exists mbti_match cascade;

create table reply
(
	index int,
	email varchar(50),
	q1	int,
	q2	int,
	q3	int,
	q4	int,
	q5	int,
	q6	int,
	q7	int,
	q8	int,
	q9	int,
	q10	int,
	q11	int,
	q12	int,
	q13	int,
	q14	int,
	q15	int,
	q16 int,
	school_name varchar(20),
	gender varchar(5),
	study_group varchar(20),
	star_sign varchar(5),
	age	int,
	area varchar(10),
	mbti_result varchar(5),
	primary key(index)
);

create table mbti_match
(
	asked_mbti varchar(5),
	suitable_mbti varchar(5),
	primary key (asked_mbti,suitable_mbti)
);

copy reply(index, email, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, 
			q11, q12, q13, q14, q15, q16, school_name, gender, study_group,
		   star_sign, age, area, mbti_result)
from 'D:\111-1\Data_Base\Final_project\Reply.csv'
delimiter ','
csv header;

copy mbti_match(asked_mbti, suitable_mbti)
from 'D:\111-1\Data_Base\Final_project\MBTI_match.csv'
delimiter ','
csv header;