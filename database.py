import sqlite3
import csv
import pandas

def build_the_db():
    conn = sqlite3.connect('./database/database-project.db')
    cursor = conn.cursor()

    f = open('database\SQLcode\Create_reply.sql')
    code = f.read()
    cursor.executescript(code)

    reply = pandas.read_csv('database\data\Reply.csv')
    reply.to_sql('reply', conn, if_exists='append', index = False)
    mbti_match = pandas.read_csv('database\data\MBTI_match.csv')
    mbti_match.to_sql('mbti_match', conn, if_exists='append', index = False)

    f = open('database\SQLcode\Create_tables.sql')
    code = f.read()
    cursor.executescript(code)

    f = open('database\SQLcode\Insert_data.sql')
    code = f.read()
    cursor.executescript(code)

    f.close()
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    build_the_db()