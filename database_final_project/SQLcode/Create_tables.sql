drop table if exists subject;
drop table if exists area;
drop table if exists hometown;
drop table if exists school;
drop table if exists study;
drop table if exists star_sign;
drop table if exists subject_star_sign;
drop table if exists test_result;

create table subject
(
	index int,
	email varchar(50),
	gender varchar(5),
	age int,
	primary key (index)
);

create table test_result
(
	index int,
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
	mbti_result varchar(5),
	primary key (index)
);

create table school
(
	school_name varchar(20),
	study_group varchar(20),
	primary key(school_name,study_group)
);

create table study
(
	index int,
	school_name varchar(20),
	study_group varchar(20),
	primary key(index)
);

create table area
(
	area varchar(10),
	primary key(area)
);

create table hometown
(
	index int,
	area varchar(10),
	primary key(index)
);

create table star_sign
(
	star_sign varchar(10),
	primary key(star_sign)
);

create table subject_star_sign
(
	index int,
	star_sign varchar(10),
	primary key(index)
);