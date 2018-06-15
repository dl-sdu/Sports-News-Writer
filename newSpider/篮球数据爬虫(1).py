# -*- coding:utf-8 -*-
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from distutils import log
import os
import sys
from selenium.webdriver.common.action_chains import *
import re
import xlrd
import xlwt
import json
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def setpl():
    global page_list
    page_list = 4056
    global cangoin

def isNBA(url):
    driver.get(url)
    #driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    div_m = soup.find('div', class_='main_data')
    div_c = div_m.find('div', class_='cont_figure')
    div_l = div_c.find('div', class_='cont_figure_lis')
    div = div_l.find_all('div', recursive=False)
    for d in div:
        dd = d.find_all('div', recursive=False)[2]
        dp = dd.find('p')
        if dp.get_text()=='NBA':
            dzb = d.find_all('div', recursive=False)[3]
            dfl = dzb.find('div', class_='cont_figure_li03_m')
            span = dfl.find('span', class_='cRed')
            sa = span.find('a')
            print(sa['href'])
            url_into = sa['href']
            #print(21321)
            print(url_into)
            #print(213)
            search(url_into)
            print(cangoin)
            if not cangoin:
                p = dfl.find('p', recursive=False)
                a = p.find('a', text='战报')
                print (a['href'])
                url_zb = a['href']
                getzb(url_zb)
        else:
            print ('不在')
            print (dp.get_text())

def getzb(url):
    global page_list
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    db = soup.find('div', class_='blkContainerSblk')
    dbody = db.find('div', id='artibody')
    ps = dbody.find_all('p', recursive=False)
    page_list = page_list - 1
    write_path = 'D:\其他\战报\\' + str(page_list-1) + '.txt'
    fo = open(write_path, "w", encoding='utf-8')
    for p in ps:
        pt = p.get_text()
        print(pt)
        fo.write(pt.replace(' ', ''))
        fo.write('\n')
    fo.close()

def search(url_into):
    print(1)
    print(url_into)
    driver.get(url_into)
    driver.get(url_into)
    global page_return
    global real_name
    global real_time
    soup = BeautifulSoup(driver.page_source, 'lxml')

    if cangoin:
        getnews(url_into)

    tab_zb = driver.find_element_by_xpath('/html/body/section[2]/div/div[1]/div[1]/a[4]').click()#'a[tab()="live"]'
    ActionChains(driver).click(tab_zb)

    #body = soup.find('body', ppccont='news')
    #print (body['class'])

    span = soup.find('span', class_='qq_spanoption')
    as_ = span.find('a', class_='qq_login_h')
    print (as_['href'])
    id = as_['href'][-10:]
    href='http://api.sports.sina.com.cn/pbp/?format=json&source=web&withhref=1&mid='+id+'&pid=&eid=0&dpc=1'
    de_json(href)
    #print (soup.prettify())
    a = soup.find('a', tab='live')
    print(a['class'])

    # div = soup.find('div', class_='ppc03_cast_cont', stype='auto')
    # print (div['scrolling'])
    # if(div!=None):
    #     #div = soup.find('div', class_='ppc03_cast_tabs clearfix')
    #     ol = div.find('ol', recursive=False)
    #     print (ol['class'])
    #     div_d = div.find('div', recursive=False)
    #     print (div_d['class'])
    #     guest = div_d.find('div', class_ ="ppc03_cast_select bselector01 fr")
    #     select = guest.find('select')
    #     option = select.find('option')
    #     print (select.name)
    #     #guest = div_d.find('a', tab = 'guest', recursive=True)
    #     print (guest.get_text())
    #     li = ol.find_all('li', recursive=False)
    #     li = ol.find_all(re.compile("^li"))
    #     divs = ol.find_all('div', class_ = 'ppc03_cast_score fr')
    #     #print (divs[0].get_text())
    #     #print (ol.descendants[0])
    #     for l in li:
    #         div1 = l.find('div', recursive=False)#, class_='ppc03_cast_time f1' c
    #         print ('哈哈哈哈哈')
    #         print (l['nid'],'hhhhhhhhhh')
    #         real_name.append(div1.get_text())
    #         print (div1)
    #     print('hehehe')
    #     print (real_name)
    # else:
    #     return
    # page_return=1

def getnews(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    divc = soup.find('div', class_='barticle_content')
    ps = divc.find_all('p', recursive=False)
    write_path = 'D:\其他\战报\\'+str(page_list)+'.txt'
    fo = open(write_path, "w", encoding='utf-8')
    for p in ps:
        pt = p.get_text()
        print (pt)
        fo.write(pt.replace(' ', ''))
        fo.write('\n')
    fo.close()

def de_json(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    print (soup.prettify())
    pre = soup.find('pre')
    json_t = pre.get_text()
    json_string = json.loads(json_t)
    #print (json_string)

    workbook = xlwt.Workbook()  # excle打开
    sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    write_path = 'D:\其他\直播\\'+str(page_list-1)+'.xls'
    #page_list = page_list-1

    page_in_list = 0
    for i in json_string['result']['data']['pbp_msgs']:
        #ele = json_string[i]
        #print (i.key)
        print (i)
        print (json_string['result']['data']['pbp_msgs'][i]['team_name'])
        print (json_string['result']['data']['pbp_msgs'][i]['game_clock'])
        des = json_string['result']['data']['pbp_msgs'][i]['description']
        txt = re.sub(r'<.*?>','',des)
        #print(re.match(r'>[\u4e00-\u9fa5]*<', des))
        #if re.match(r'>[\u4e00-\u9fa5]*<', des):
            #txt = re.match(r'>[\u4e00-\u9fa5]*<', des)[1:-1] + re.match(r'a>[\u4e00-\u9fa5]*',des)[2:]
            #print('Yesyesyes')
        #else:
            #txt = des
        print (txt)
        print (json_string['result']['data']['pbp_msgs'][i]['home_score'])
        print (json_string['result']['data']['pbp_msgs'][i]['visitor_score'])
        #print (i['game_clock'])
        #print ('\n')

        sheet1.write(page_in_list, 0, json_string['result']['data']['pbp_msgs'][i]['team_name'])
        sheet1.write(page_in_list, 1, json_string['result']['data']['pbp_msgs'][i]['game_clock'])
        sheet1.write(page_in_list, 2, txt)
        sheet1.write(page_in_list, 3, json_string['result']['data']['pbp_msgs'][i]['home_score'])
        sheet1.write(page_in_list, 4, json_string['result']['data']['pbp_msgs'][i]['visitor_score'])
        page_in_list = page_in_list + 1
    workbook.save(write_path)
    page_in_list = page_in_list + 1

    #json=soup.prettify()
    #json_string = json.load(json)
    #for i in [0:565]

chromedriver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
driver=webdriver.Chrome(chromedriver)
#driver=webdriver.Chrome()
global page_list
global cangoin
cangoin=0
setpl()
page_return=1
real_name=[]
driver.implicitly_wait(2)
url='http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=2012-06-06'
#isNBA(url)
print('url1 is done!')
url2='http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=all&scheduledate=2014-02-10'
#isNBA(url2)
#search('http://sports.sina.com.cn/nba/live.html?id=2014101502')
i='2012'
m='06'
n='06'
#isNBA('http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)

print(1)

years=['2012','2013','2014','2015','2016','2017']
mouth=['01','02','03','04','05','06','07','08','09','10','11','12']
days1=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
days2=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
days3=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']
days4=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29']

'''
i='2012'
m='06'
for k in range(28):
    n=days3[k]
    isNBA('http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)

'''
for i in years[0:]:
    if (i == '2012' ):
        for m in mouth[5:]:  # 每次出问题记得更改
            if (m in ['01','03','05','07','08','10','12']):
                for n in days2[:]:
                     print(i + '-' + m + '-' + n)
                     print(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                     isNBA('http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)

            elif (m in ['02']):
                for n in days4:
                    print(i + '-' + m + '-' + n)
                    isNBA(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
            else:
                for n in days1:
                    if (m=='06' and n =='02'):
                        continue
                    print(i + '-' + m + '-' + n)
                    print(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    isNBA(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
    elif (i=='2016'):
        for m in mouth[5:]:  # 每次出问题记得更改
            if (m in ['01','03','05','07','08','10','12']):
                for n in days2[:]:
                     print(i + '-' + m + '-' + n)
                     print(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                     isNBA('http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)

            elif (m in ['02']):
                for n in days4:
                    print(i + '-' + m + '-' + n)
                    isNBA(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
            else:
                for n in days1:
                    print(i + '-' + m + '-' + n)
                    print(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    isNBA(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
    else:
        for m in mouth[0:]:  # 每次出问题记得更改
            if (m in ['01','03','05','07','08','10','12']):
                if (i == '2014' and m=='08'):
                  cangoin=1
                  for n in days2:
                    print(i + '-' + m + '-' + n)
                    isNBA('http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
            elif (m in ['02']):
                for n in days3:
                    print(i + '-' + m + '-' + n)
                    isNBA(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
            else:
                for n in days1:
                    print(i + '-' + m + '-' + n)
                    isNBA(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)


driver.quit()









