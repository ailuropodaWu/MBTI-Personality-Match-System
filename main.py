# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
import os
import base64
import codecs
import sqlite3
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties as font
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



def render(datas, figure_description='Figure'):
    if datas == None:
        return None
    font1 = font(fname='./static/NotoSansTC-ExtraBold.ttf')
    colors = ['yellow', 'red', 'green', 'orange', 'pink']
    fig = Figure()
    ax = fig.subplots()
    data_ratio = [v[1] for v in datas]
    data_label = [v[0] for v in datas]
    patches, l_text, p_text = ax.pie(x=data_ratio, 
                                     labels=data_label, 
                                     autopct="%1.2f%%", 
                                     wedgeprops = {"linewidth": 1, "edgecolor": "white"},
                                     colors=colors,
                                     shadow=True)
    for t in l_text:
        t.set_fontproperties(font1)
        t.set_color('white')
        t.set_fontsize('large')
    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<figure> \
                <img src='data:image/png;base64,{data}'/ style='margin-left: 25%; width: 50%'> \
                <figcaption style='text-align: center; color: #fff; font-weight: bold; font-size: 24px'>{figure_description}</figcaption> \
            </figure>" 


@app.route('/',methods=['GET', 'POST'])
def index():
    form = MyForm()
    conn = sqlite3.connect('./database/database-project.db', check_same_thread=False)
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
            
        
        db_engine.execute(f"""
            create temp view if not exists matched_mbti as
                select suitable_mbti
                from mbti_match
                where asked_mbti = '{mbti}';
        """)
        db_engine.execute(f"""
            create temp view if not exists matched_index as
                select num
                from subject natural join test_result, matched_mbti
                where 
                age between '{age}' - 2 and '{age}' + 2 and 
                gender = '{gender}' and mbti_result = suitable_mbti;
        """)
        db_engine.execute(f"""
            select cast(count(num) as float) * 100 / (select count(num) from subject) as percentage 
                from matched_index;
        """)
        
        datas = list(db_engine.fetchall())
        all_matched = ""
        print(datas)
        for data in datas:
            for num in data:
                all_matched += str(round(num, 2))
            all_matched += "% "
        all_matched = "<p style='text-align: center; color: #fff; font-weight: bold; font-size: 30px'>\
                        在曾經參與此網站檢測的人當中，與你適配的異性有 : " + all_matched + "<br>"
        db_engine.execute(f"""
            
            select area,
	            cast(count(area) as float) * 100 / 
		        (select count(num) from matched_index natural join hometown) as percentage
            from matched_index natural join hometown 
            group by area
            order by percentage desc;
        """)
        area_datas = list(db_engine.fetchall())

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
        star_datas = list(db_engine.fetchall())

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
        school_datas = list(db_engine.fetchall())

        ### reder the figure
        result = """
                <style>
                    html {
                        background: url('./static/form_background.jpg') no-repeat center center fixed;
                        -webkit-background-size: cover;
                        -moz-background-size: cover;
                        -o-background-size: cover;
                        background-size: cover;
                    }
                </style>
        
        """
        mbti_match = f"<p style='text-align: center; color: #fff; font-weight: bold; font-size: 30px'> 你的性格是 : \
                        {mbti} <br> {mbti_statement[mbti][0]}: {mbti_statement[mbti][1]}<br>"
        mbti_icon = f"<img src='./static/mbti_icon/{mbti}.png'/ style='width: 10%'>"
        result +=  mbti_match+ \
                mbti_icon + \
                all_matched + \
                render(area_datas, "來自的地區") + \
                render(star_datas, "星座比例") + \
                render(school_datas, "來自的學校")
        return result

        db_engine.executescript('''
            drop view matched_mbti;
            drop view matched_index;
        ''')
        conn.commit()
        db_engine.close()
        conn.close()
    else:
        conn = sqlite3.connect('./database/database-project.db', check_same_thread=False)
        db_engine = conn.cursor()
        return render_template('index.html',form=form)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)