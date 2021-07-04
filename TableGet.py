'''
Author: Iccccy.xie
Date: 2021-07-03 13:48:33
LastEditTime: 2021-07-03 20:59:53
LastEditors: Iccccy.xie(binicey@outlook.com)
FilePath: \GradeTableGet_BIT\TableGet.py
'''
#!/usr/bin/env python
#要安装的工具包 beautifulSoup4和selenium

import requests
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup


#登录包
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()    
print('准备登陆jwc网站...')
#发送请求
driver.get(r"http://jwms.bit.edu.cn/jsxsd/kscj/cjcx_list")
wait = WebDriverWait(driver,5)
#重要：暂停1分钟进行预登陆，此处填写账号密码及验证


dictCookies = driver.get_cookies()
while(len(dictCookies)>1):
    dictCookies = driver.get_cookies()
cookie=dict(dictCookies[0])['value']


cookie


cookie='JSESSIONID='+cookie

url1='http://jwms.bit.edu.cn/jsxsd/kscj/cjcx_list'
headers1={
'Host': 'jwms.bit.edu.cn',
'Connection': 'keep-alive',
'Content-Length': '26',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
'Origin': 'http://jwms.bit.edu.cn',
'Content-Type': 'application/x-www-form-urlencoded',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Referer': 'http://jwms.bit.edu.cn/jsxsd/kscj/cjcx_query?Ves632DSdyV=NEW_XSD_XJCJ',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': cookie,
}
# 获取成绩网页
def start(url,headers):
    r=requests.get(url,headers=headers)
    return r
r=start(url1,headers1)
# print(r.text)


soup=BeautifulSoup(r.text,features="lxml")


# print(soup.prettify())
#print(list(enumerate(soup.td.next_siblings)))


# for i in soup.findAll('table'):
#     print(i)


GradeTable=dict(enumerate(soup.findAll('table')[1]))


GradeTable=list(GradeTable.values())


# print(GradeTable[2])


GradeTable_new=[]
for i in GradeTable:
    if len(str(i))>20:
        GradeTable_new.append(i)
    # print(len(GradeTable[i]))


TableTitle=GradeTable_new[0]
GradeItem=GradeTable_new[1:]


GradeTable_out=[]
for i in GradeItem:
    GradeI=[]
    for j in i.findAll('td'):
        GradeI.append(j.string)
    GradeTable_out.append(GradeI)


titleString=[]
for i in TableTitle.find_all('th'):
    titleString.append(i.string)


table=pd.DataFrame(GradeTable_out,columns=titleString)

#输出
table.to_csv('Grade.csv',encoding='gbk')
# print(table)
print("success！")

