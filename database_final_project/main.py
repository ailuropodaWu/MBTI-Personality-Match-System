# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
import os
import sqlite3

from form import MyForm, get_data
from mbti import mbti_statement
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



'''
Function to get form data.
'''

@app.route('/',methods=['GET', 'POST'])
def index():
    form = MyForm()
    conn = sqlite3.connect('database-project.db', check_same_thread=False)
    db_engine = conn.cursor()
    if request.method == 'POST' and form.validate():
        '''
        mbti match query
        '''
        mbti, gender, age = get_data(form, conn)

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
        db_engine.executescript('''
            drop view matched_mbti;
            drop view matched_index;
        ''')
        conn.commit()
        db_engine.close()
        conn.close()
    else:
        conn = sqlite3.connect('database-project.db', check_same_thread=False)
        db_engine = conn.cursor()
        return render_template('layout.html',form=form)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)