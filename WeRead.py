#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ast import Try
import re
import os
from lib2to3.pgen2 import driver
from pyppeteer import launch
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import sqlite3


def get_weread(url):
    """用selenium爬取微信读书
    """
    global driver
    driver = webdriver.Chrome()
    driver.set_window_size(1024, 768)
    driver.get(url)
    for i in range(10):
        driver.execute_script("window.scrollBy(0,10000)")   #向下滚动
        sleep(1)

    # book = driver.find_element_by_xpath('//*[@id="routerView"]/div[2]/div[2]/ul/li/ul').text # 所有
    # book = driver.find_element_by_xpath('//*[@id="routerView"]/div[2]/div[2]/ul/li')  # 单本
    # html_doc = book.get_attribute('innerHTML')
    # print(book.get_attribute('innerHTML'))
    # bookParse(html_doc)

    book = driver.find_elements_by_xpath('//*[@id="routerView"]/div[2]/div[2]/ul/li')  # 获取单本书籍数据
    for x in book:
        html_doc = x.get_attribute('innerHTML')
        print("~~~~~~start~~~~~~~")
        book_parse(html_doc)


def book_parse(html_doc):
    """用re解析网页内容
    """
    try:
        bookUrl_re = re.compile(r'(/web/reader/[0-9a-zA-Z]*)') # 书籍url地址
        bookCover_re = re.compile(r'(https://.*.[jpg|png])(" alt)') # 书籍封面
        bookTitle_re = re.compile(r'(<p class="wr_bookList_item_title">)(.*)(</p><p class="wr_bookList_item_author">)') #书籍名
        bookAuthor_re = re.compile(r'(<p class="wr_bookList_item_author">.*">)(.*)(</a></p>)')  # 作者
        bookDesc_re = re.compile(r'(<p class="wr_bookList_item_desc">)(.*)(</p>)')  # 书籍简介

        bookUrl = "https://weread.qq.com" + bookUrl_re.search(html_doc).group(0)
        bookCover = bookCover_re.search(html_doc).group(1)
        bookTitle = bookTitle_re.search(html_doc).group(2)
        bookAuthor = bookAuthor_re.search(html_doc).group(2)
        bookDesc = bookDesc_re.search(html_doc).group(2)

        print(bookUrl)
        print(bookCover)
        print(bookTitle)
        print(bookAuthor)
        print(bookDesc)
        # to_csv.save_to_csv(bookTitle,bookAuthor,bookUrl, bookCover,bookDesc)
        save_db(bookTitle,bookAuthor,bookUrl, bookCover,bookDesc)
    except:
        pass

def save_db(bookTitle,bookAuthor,bookUrl, bookCover,bookDesc):
    """保存数据到sqlite
    """
    filename = "weread.db"

    # 判断文件是否存在
    if os.path.exists(filename):
        # 处理数据并写入
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO WEREAD(bookTitle,bookAuthor,bookUrl,bookCover,bookDesc) VALUES(?,?,?,?,?)", 
                (bookTitle,bookAuthor,bookUrl,bookCover,bookDesc))
        # c.execute("INSERT INTO WEREAD VALUES ('%s','%s','%s','%s','%s','%s')" % (2,bookTitle,bookAuthor,bookUrl,bookCover,bookDesc))
        conn.commit()
        conn.close()
    else:
         # 创建数据库 处理数据并写入
        conn = sqlite3.connect('weread.db')
        c = conn.cursor()
        c.execute("CREATE TABLE WEREAD \
            (bookTitle TEXT NOT NULL UNIQUE,\
                bookAuthor TEXT NOT NULL,\
                bookUrl TEXT NOT NULL,\
                bookCover TEXT NOT NULL,\
                bookDesc TEXT NOT NULL)")

        c.execute("INSERT OR IGNORE INTO WEREAD(bookTitle,bookAuthor,bookUrl,bookCover,bookDesc) VALUES(?,?,?,?,?)", 
                    (bookTitle,bookAuthor,bookUrl,bookCover,bookDesc))
        conn.commit()
        conn.close()

if __name__== "__main__":
    url = 'https://weread.qq.com/web/appcategory/newrating_publish'
    get_weread(url)