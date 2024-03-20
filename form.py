from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Email

class MyForm(FlaskForm):
    Gender = SelectField(u'你的性別', choices=[('male','男'),('female','女')])
    Age = IntegerField(u'你的年齡',validators=[DataRequired(), NumberRange(min=0, max=100, message='')])
    Area = SelectField(u'你來自的地區', choices=[('北部','北部'),('中部','中部'),('南部','南部'),('東部','東部'),('離島','離島'),('外國人','外國人')])
    School = StringField(u'你的學校，請輸入全名',validators=[DataRequired()])
    Study_group = SelectField(u'你的類組', choices=[('文法商','文法商'),('理工','理工'),('生醫農','生醫農'),('其它','其它')])
    Star_sign = SelectField(u'你的星座', choices=[('牡羊座','牡羊座'),('金牛座','金牛座'),('雙子座','雙子座'),('巨蟹座','巨蟹座'),('獅子座','獅子座'),('處女座','處女座'),('天秤座','天秤座'),('天蠍座','天蠍座'),('射手座','射手座'),('摩羯座','摩羯座'),('水瓶座','水瓶座'),('雙魚座','雙魚座')])
    Q1 = SelectField(u'Q1 : 我樂於"參加聚會"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q2 = SelectField(u'Q2 : 我喜歡探討"未知的知識"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q3 = SelectField(u'Q3 : 我善於闡述"我的感受"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q4 = SelectField(u'Q4 : 我喜歡"按照計劃"行事', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q5 = SelectField(u'Q5 : 我偏好"安靜的場域"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q6 = SelectField(u'Q6 : 我喜歡到"未曾去過"的地方旅行', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q7 = SelectField(u'Q7 : 我看待世界"重視邏輯"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q8 = SelectField(u'Q8 : 我的生活環境"整潔"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q9 = SelectField(u'Q9 : 我喜歡交"很多朋友"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q10 = SelectField(u'Q10 : 我對這個世界"充滿好奇" "', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q11 = SelectField(u'Q11 : 我能感受到環境，及人們"細微的變化"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q12 = SelectField(u'Q12 : 我是個"準時"的人', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q13 = SelectField(u'Q13 : 我更喜歡"獨處"的時間', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q14 = SelectField(u'Q14 : 我忠於"傳統"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q15 = SelectField(u'Q15 : 我"避免爭執"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q16 = SelectField(u'Q16 : 我的行為模式"易於預測"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    submit = SubmitField('Submit')

def get_data(form, conn):
    '''
    get data
    '''
    gender = form.Gender.data
    age = form.Age.data
    area = form.Area.data
    school = form.School.data
    study_group = form.Study_group.data
    star_sign = form.Star_sign.data
    q1 = int(form.Q1.data)
    q2 = int(form.Q2.data)
    q3 = int(form.Q3.data)
    q4 = int(form.Q4.data)
    q5 = int(form.Q5.data)
    q6 = int(form.Q6.data)
    q7 = int(form.Q7.data)
    q8 = int(form.Q8.data)
    q9 = int(form.Q9.data)
    q10 = int(form.Q10.data)
    q11 = int(form.Q11.data)
    q12 = int(form.Q12.data)
    q13 = int(form.Q13.data)
    q14 = int(form.Q14.data)
    q15 = int(form.Q15.data)
    q16 = int(form.Q16.data)

    mind = -(q1-3)+(q5-3)-(q9-3)+(q13-3)
    energy = (q2-3)+(q6-3)+(q10-3)-(q14-3)
    nature = (q3-3)-(q7-3)+(q11-3)+(q15-3)
    tactics = -(q4-3)-(q8-3)-(q12-3)-(q16-3)

    mbti = ('E' if mind<=0 else 'I') + ('S' if energy<=0 else 'N') + ('T' if nature<=0 else 'F') + ('J' if tactics<=0 else 'P')
    
    '''
    Database update
    '''
    cursor = conn.cursor()
    cursor.execute("""
        select max(num) from test_result;
    """)
    num = list(cursor.fetchall())[0][0] + 1
    cursor.execute(f"""
        insert into subject(num, gender, age)
        VALUES ({num},'{gender}','{age}');"""
    )
    cursor.execute(f"""
        insert into test_result(num, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11,
                                q12, q13, q14, q15, q16, mbti_result)
        VALUES ({num}, {q1}, {q2}, {q3}, {q4}, {q5}, {q6}, {q7}, {q8}, {q9}, {q10}, {q11}, {q12}, {q13},
                        {q14}, {q15}, {q16}, '{mbti}');
    """)
    cursor.execute(f"""
        insert into study(num, school_name, study_group)
        VALUES ({num}, '{school}', '{study_group}');
    """)
    cursor.execute(f"""
        insert into subject_star_sign(num, star_sign)
        VALUES ({num}, '{star_sign}');
    """)
    cursor.execute(f"""
        insert into hometown(num, area)
        VALUES ({num}, '{area}');
    """)
    conn.commit()
    return mbti, gender, age
