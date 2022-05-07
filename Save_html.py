#!/usr/bin/env python
# -*- coding:utf-8 -*-

from dataclasses import dataclass
import sqlite3
from jinja2 import Environment, FileSystemLoader


def dict_factory(cursor, row):
    # sqlite默认输出元祖、这里改为输出字典形式
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def sql_data():
    # 从sqlite数据库里面读取数据、并返回数据
    book_data = []
    con = sqlite3.connect('weread.db')
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('SELECT * FROM WEREAD')
    #print(cur.fetchone())
    for x in cur.fetchall():
        book_data.append(x)
    con.close()
    return book_data


def save_html():
    # 用jinja2 写入html
    data = sql_data()
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('weread/template.html') # 导入模版
    with open('weread/godly.html', 'w+', encoding='utf-8') as f:
        out = template.render(data=data)
        f.write(out)
        f.close()

if __name__ == "__main__":
    save_html()