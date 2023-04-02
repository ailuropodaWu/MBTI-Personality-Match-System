# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_cors import CORS
from flask_bootstrap import Bootstrap
import os
import sqlite3
from flask_wtf.csrf import CSRFProtect

from database import build_the_db
from form import MyForm, get_data
'''
Service Initialization.
'''
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)
'''
Connect to database.
rds_host = "localhost"
rds_port = 5432
rds_user = "postgres"
rds_password = "13579753159"
rds_database = "data"
'''

build_the_db()
conn = sqlite3.connect('database-project.db', check_same_thread=False)
db_engine = conn.cursor()


'''
Function to get form data.
'''

@app.route('/',methods=['GET', 'POST'])
def index():
    mbti_statement = {
        'INTJ' :  ('建筑师','富有想象力和战略性的思想家，一切皆在计划之中。'),
        'INTP' :  ('逻辑学家','具有创造力的发明家，对知识有着止不住的渴望。'),
        'ENTJ' :  ('指挥官','大胆，富有想象力'),
        'ENTP' :  ('辩论家','聪明好奇的思想者，不会放弃任何智力上的挑战。'),

        'INFJ' :  ('提倡者','安静而神秘，同时鼓舞人心且不知疲倦的理想主义者。'),
        'INFP' :  ('调停者','诗意，善良的利他主义者，总是热情地为正当理由提供帮助。'),
        'ENFJ' :  ('主人公','富有魅力鼓舞人心的领导者，有使听众着迷的能力。'),
        'ENFP' :  ('竞选者' '热情，有创造力爱社交的自由自在的人，总能找到理由微笑。'),

        'ISTJ' :  ('物流师','实际且注重事实的个人，可靠性不容怀疑。'),
        'ISFJ' :  ('守卫者','非常专注而温暖的守护者，时刻准备着保护爱着的人们。'),
        'ESTJ' :  ('总经理','出色的管理者，在管理事情或人的方面无与伦比。'),
        'ESFJ' :  ('执政官','极有同情心，爱交往受欢迎的人们，总是热心提供帮助。'),

        'ISTP' :  ('鉴赏家','大胆而实际的实验家，擅长使用任何形式的工具。'),
        'ISFP' :  ('探险家','灵活有魅力的艺术家，时刻准备着探索和体验新鲜事物。'),
        'ESTP' :  ('企业家','聪明，精力充沛善于感知的人们，真心享受生活在边缘。'),
        'ESFP' :  ('表演者','自发的，精力充沛而热情的表演者－生活在他们周围永不无聊。')
    }
    form = MyForm()
    if request.method == 'POST' and form.validate():
        '''
        mbti match query
        '''
        mbti, gender, age = get_data(form, db_engine)

        if gender == 'male':
            gender = 'female'
        else:
            gender = 'male'
        '''
        check update
        '''
        '''
        db_engine.execute(f"""
            select * from hometown;
        """)
        datas = list(db_engine.fetchall())
        test = ""
        for data in datas:
            for i in data:
                test += str(i)
            test += "<br>"
        '''
        db_engine.executescript(f"""
            create temp view if not exists matched_mbti as
                select suitable_mbti
                from mbti_match
                where asked_mbti = '{mbti}';
            
            create temp view if not exists matched_index as
                select num
                from subject natural join test_result, matched_mbti
                where 
                age between '{age}' - 2 and '{age}' + 2 and 
                gender = '{gender}' and mbti_result = suitable_mbti;

            select 
                cast(count(num) as float) * 100 / (select count(num) from subject) 
                        as percentage
            from matched_index;
        """)
        
        datas = list(db_engine.fetchall())
        all_matched = ""
        for data in datas:
            for num in data:
                all_matched += str(num)
            all_matched += "% "
        all_matched = "在曾經參與此網站檢測的人當中，與你適配的異性有 : " + all_matched + "<br>"
        db_engine.execute(f"""
            
            select area,
	            cast(count(area) as float) * 100 / 
		        (select count(num) from matched_index natural join hometown) as percentage
            from matched_index natural join hometown 
            group by area
            order by percentage desc;
        """)
        datas = list(db_engine.fetchall())
        area_matched = ""
        for data in datas:
            for num in data:
                area_matched += str(num)
            area_matched += "% "
        area_matched = "配對對象的地區分布 : " + area_matched + "<br>"
        db_engine.execute(f"""
            select 
	            star_sign,
                cast(count(star_sign) as float) * 100 / 
                (select count(num) from matched_index natural join subject_star_sign)
                    as percentage
            from matched_index natural join subject_star_sign
            group by star_sign
            order by percentage desc
        """)
        datas = list(db_engine.fetchall())
        star_matched = ""
        for data in datas:
            for num in data:
                star_matched += str(num)
            star_matched += "% "
        star_matched = "配對對象的星座分布 : " + star_matched + "<br>"
        db_engine.execute(f"""
            select 
                school_name,
                cast(count(school_name) as float) * 100 / 
                    (select count(num) from matched_index natural join study)
                    as percentage
            from matched_index natural join study
            group by school_name
            order by percentage desc
        """)
        datas = list(db_engine.fetchall())
        school_matched = ""
        for data in datas:
            for num in data:
                school_matched += str(num)
            school_matched += "% "
        school_matched = "配對對象的學校分布 : " + school_matched + "<br>"
        return "你的性格是 : " + mbti + "<br>" + mbti_statement[mbti][0] + " : " + mbti_statement[mbti][1] + "<br>" + \
                all_matched + area_matched + star_matched + school_matched

    return render_template('layout.html',form=form)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)