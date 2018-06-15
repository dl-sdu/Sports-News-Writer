#encoding=utf-8
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
def search(url):
    print(1)
    print(url)
    driver.get(url)
    driver.get(url)
    global page_return
    global real_name
    global real_time
    soup = BeautifulSoup(driver.page_source, 'lxml')
    div = soup.find('div', class_='cont_figure_lis')
    if(div!=None):
     div = div.find_all('div', recursive=False)
     page_return=1
     for i in div:
        name_judge=0     #
        name=[]
        real_name = []
        real_time=[]
        #print(real_name)
        index = 0
        url_set = []
        page_return = 1
        #找到合适的战报等元素并进入
        if (i.find('div')):
            m = i('div')[2]
           # print(m.get_text())
            if (m.get_text().replace(" ", "").strip() == "" or '奥' in m.get_text() or '篮' in m.get_text()
                or '排' in m.get_text() or 'NBA' in m.get_text() or '网' in  m.get_text()
                or 'U' in m.get_text() or '抽签' in m.get_text() or '斯' in m.get_text()
                or '拳击'in m.get_text() or 'F'in m.get_text() or 'BA' in m.get_text()
                or '棋' in m.get_text() or '牌' in m.get_text() or '排球' in m.get_text()
                or '乒乓'in m.get_text() or '羽' in m.get_text() or '游泳' in m.get_text() or '亚俱杯' in m.get_text() or '东京赛'in m.get_text()
          or  '美传奇巨星' in m.get_text() or '新秀赛' in m.get_text() or '冰壶' in m.get_text() or 'NCAA' in m.get_text()):
                continue
            else:
                m=i.find_all('div',recursive=False)[1]
                for m_time in re.findall(r'[0-9]{2,2}',m.get_text()):
                    real_time.append(m_time)
                n = i.find_all('div',recursive=False)[3]
                #print(len(n.find_all('div')))
                if(len(n.find_all('div',recursive=False))!=3):
                  continue
                 # 选中中间那一栏
                n1 = n.find_all('div',recursive=False)[1]  # 选中中间有字的一栏
                if (n1.find('h4')):
                    #print(50)
                    n1_1 = n1.find('h4')
                    if (n1_1.find_all('a',recursive=False)):
                        for name_ in n1_1.find_all('a',recursive=False):
                            real_name.append(name_.get_text())
                        print(real_name)
                        for name_judge_ in real_name:
                            if ('篮' in name_judge_ or '排' in name_judge_  or '美传奇巨星' in name_judge_ or '李娜' in name_judge
                            or ('长春亚泰' in name_judge_ and real_time[0] == '07' and real_time[1] == '09')
                                or ('利物浦' in name_judge_ )
                                or ('广州恒大' in name_judge_ and real_time[0] == '11' and real_time[1] == '04')
                                or ('拜仁' in name_judge_ and real_time[0] == '12' and real_time[1] == '16')


                           ):
                                name_judge=1
                                break
                        if(name_judge==1):
                            continue
                        if (n1.find('p')):
                            n1_2 = n1.find('p')
                            if (n1_2.find('a')):
                                for n1_2_ in n1_2('a'):
                                   # print(10)
                                    #print(n1_2_.get_text())
                                    if (n1_2_.get_text() == "战报" or n1_2_.get_text() == '实录'):
                                        print(n1_2_.get_text())
                                        index = index + 1
                                        print(n1_2_['href'])
                                        url_set.append(n1_2_['href'])
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
        if (index != 2):
            #print(index)
            continue
        else:
            get_txt(url_set[0], name)
            if (page_return != 0):

                get_livetxt(url_set[1])


    # 方法体1：遍历网页依次找到链接地址
    # 方法体1结束
    # url = 'http://match.sports.sina.com.cn/livecast/1/iframe/live_log.html?168198'
    # url_new = 'http://sports.sina.com.cn/j/2012-08-17/21216193280.shtml'
    else:
        return
def get_txt(url, name):  # ,real_name)
                    print(2)
                    driver.get(url)
                    global page_return
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    strong_list = 0
                    txt_list = []
                    test_time_count=0
                    test_time=[]
                    if(soup.find('span',id='pub_date')):
                        mtime=soup.find('span',id='pub_date')
                        test_time.append(re.findall(r'[0-9]{2,2}\u6708',mtime.get_text())[0][0:2])    #月
                        test_time.append(re.findall(r'[0-9]{2,2}\u65e5',mtime.get_text())[0][0:2])    #日

                    if(len(test_time)==0):
                        if (soup.find('span', class_='article-a__time')):
                            mtime = soup.find('span',class_='article-a__time')
                            test_time.append(re.findall(r'[0-9]{2,2}\u6708', mtime.get_text())[0][0:2])
                            test_time.append(re.findall(r'[0-9]{2,2}\u65e5', mtime.get_text())[0][0:2])
                    print(test_time)
                    if(len(test_time)==2):
                      if(test_time[0]!=real_time[0]):
                         page_return=0
                         return
                      if(int(test_time[1])<int(real_time[1])-1 or int(test_time[1])>int(real_time[1])+1):
                          page_return=0
                          return
                    if (soup.find('div', class_='BSHARE_POP blkContainerSblkCon clearfix blkContainerSblkCon_14')):
                        intern_deal('BSHARE_POP blkContainerSblkCon clearfix blkContainerSblkCon_14', soup, txt_list,
                                    name, strong_list)
                    elif (soup.find('div', class_='blkContainerSblkCon')):
                        intern_deal('blkContainerSblkCon', soup, txt_list, name, strong_list)
                    elif (soup.find('div', class_='article-a__content')):
                        intern_deal('article-a__content', soup, txt_list, name, strong_list)
                    elif (soup.find('div',
                                    class_='layout-equal-height__item layout-fl layout-of-hidden layout-pt-c layout-wrap-b layout-pr-a layout-br-a')):
                        intern_deal(
                            'layout-equal-height__item layout-fl layout-of-hidden layout-pt-c layout-wrap-b layout-pr-a layout-br-a',
                            soup, txt_list, name, strong_list)
                    else:
                        page_return = 0
def intern_deal(class1,soup,txt_list,name,strong_list):
    print(3)
    global page_list
    tag=1#用来判断是否已经到达进球信息的标签
    global page_return
    start_list=0#定义有文字的ｐ的开始位置
    previous_list=0#定义一个计数器，算出第一个分钟起始位置
    txt1 = soup.find('div', class_=class1)

    # 如果有一个空P开头那么就计算一下，从后面第二个P开始

    if txt1.find('p').get_text().replace(' ','').strip()=="":
                start_list=1
    print(100)
    if (txt1.find('p')):
        list_number=0
        # print(len(txt1('p')))
        if (len(txt1('p')) <= 4+start_list):
            page_return=0
            return
        #用来判断是否是一篇合格的新闻即分钟要出现在前4个p中
        newstag=0
        for news_tag in txt1.find_all('p',recursive=False)[0:5]:
            if(re.match(r'.*\u5206\u949f.*', news_tag.get_text()) != None):
                newstag=1
        if(newstag==0):
            page_return=0
            return
        else:
            for i in txt1.find_all('p',recursive=False)[1+start_list:4+start_list]:
                #  print(3)
                if (i.find('strong')):
                    #print(i('strong')[0].get_text())
                    #print(len(i('strong')[0].get_text()))
                    #print(i.get_text().strip())
                    #print(i.get_text().strip()[0:len(i('strong')[0].get_text())])
                    #print(3)
                    if (i('strong')[0].get_text() ==i.get_text().strip()[0:len(i('strong')[0].get_text())] and not
                        re.match(r'.*\u5206\u949f.*',i('strong')[0].get_text())):
                        strong_list = strong_list + 1
                       # print(strong_list)
            if (strong_list >= 2):
                page_return=0
                return
            for i in txt1.find_all('p')[1+start_list:-1]:
               # print(10000)
                # i = i.get_text().replace(" ", "").strip()
                #                    print(i[0:2])
               # print(i.attrs)
                #print(i.get_text)
                if(i.attrs!={}):
                   # print(i.attrs)
                    #print(i.get_text)
                    continue
                #print()
                if (i.get_text().replace(" ", "").strip()[0:2] == "进球" or i.get_text().replace(" ", "").strip()[0:2] == '信息' ):
                    tag=0
                    continue
                if(len(i.get_text().replace(" ", "").strip())<=35 and tag==0):
                    continue
                if ((re.match(r'.*[0-9]-[\u4e00-\u9fa5].*', i.get_text()) != None      #一龥
                     or re.match(r'.*[0-9]\'',i.get_text())!=None)and list_number>=3):  # 如果匹配到了最后一个球员名单
                    name.append(i.get_text().replace(" ", "").strip()[0:2])  # 加入名字列表
                    break
                list_number=list_number+1  #分钟
                if ((re.match(r'.*\u5206\u949f.*', i.get_text()) == None and '开场'  not in i.get_text() and '开始' not in i.get_text()) and previous_list == 0):  # 如果不match分钟就跳过
                    continue
                else:
                    final_txt = i.get_text()
                    if (i.find('a')):
                        len1 = len(i.find_all('a'))
                        # print(len1)
                        final_txt = final_txt.replace('[点击观看视频]', '').replace('[点击观看进球视频]', '')
                        for m in range(len1):
                            a_txt = i('a')[m].get_text()
                            # print(a_txt)
                            final_txt = final_txt.replace(a_txt, '')
                    else:
                       print()


                    if (i.find('script')):
                          len1 = len(i.find_all('script'))
                          # print(len1)
                          for m in range(len1):
                             a_txt = i('script')[m].get_text()
                             # print(a_txt)
                             final_txt = final_txt.replace(a_txt, '')
                    else:
                        print()
                    if (i.find('style')):
                        len1 = len(i.find_all('style'))
                        # print(len1)
                        for m in range(len1):
                            a_txt = i('style')[m].get_text()
                            # print(a_txt)
                            final_txt = final_txt.replace(a_txt, '')
                        if (i.find('span')):
                            len1 = len(i.find_all('span'))
                            # print(len1)
                            for m in range(len1):
                                a_txt = i('span')[m].get_text()
                                # print(a_txt)
                                final_txt = final_txt.replace(a_txt, '')

                    else:
                        print()
                         # print(3）final_txt.replace(" ", "").replace('[','').replace(']','').replace(':','').replace('【','').replace('】','').strip()
                    final_txt = final_txt.replace(" ", "").replace('[', '').replace(']', '').replace(':', '').replace(
                        '【', '').replace('】', '').replace('(', '').replace(')', '').replace('（', '').replace('）',
                                                                                                             '').strip()

                    if (len(final_txt) >= 10):
                        txt_list.append(final_txt)  # 将链接内的字符删除
                    previous_list = previous_list + 1
                    # if (name[1] not in real_name):  # 判断名字是否在其中
               #如果一个网页最后一个P元素为空，那么就这么做..爬倒数第二个


        zuihounumber=-1
        maxxunhuan=10
        while(zuihounumber<0 and maxxunhuan>0):
            if (re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])', txt1('p')[zuihounumber].get_text().replace(" ", "").strip()) and not txt1('p')[zuihounumber].find('a')):
                txt_list.append( (re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])', txt1('p')[zuihounumber].get_text().replace(" ", "").strip()))[0])
                zuihounumber=1
            else:
                zuihounumber=zuihounumber-1
                maxxunhuan=maxxunhuan-1
                # if (
                # re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])', txt1('p')[-1].get_text().replace(" ", "").strip())):
                #     txt_list.append(
                #         (re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])',
                #                     txt1('p')[-1].get_text().replace(" ", "").strip()))[
                #             0])
                # elif (
                # re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])', txt1('p')[-2].get_text().replace(" ", "").strip())):
                #     txt_list.append(
                #         (re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])',
                #                     txt1('p')[-2].get_text().replace(" ", "").strip()))[
                #             0])
                # elif (
                # re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])', txt1('p')[-3].get_text().replace(" ", "").strip())):
                #     txt_list.append(
                #         (re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])',
                #                     txt1('p')[-3].get_text().replace(" ", "").strip()))[
                #             0])
                # elif (
                # re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])', txt1('p')[-4].get_text().replace(" ", "").strip())):
                #     txt_list.append(
                #         (re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])',
                #                     txt1('p')[-4].get_text().replace(" ", "").strip()))[
                #             0])
                # else:
                #     txt_list.append(
                #         (re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])',
                #                     txt1('p')[-5].get_text().replace(" ", "").strip()))[
                #             0])
       # print(real_name[0])
       # print(real_name[1])
        print(txt_list)
        #print(name[0],real_name)
        if(len(name)==0):
            page_return=0
            return
        if((name[0] not  in real_name[0] and name[0] not  in real_name[1])and name[0]!='女王' and name[0]!='托' and name[0]!='皇马' and name[0]!='巴萨'):
            page_return=0
        else:
          #  print(1000)
            write_path = '/Users/hejie/Desktop/课外学习/数据集/新浪直播数据/战报/'+str(page_list)+'.txt'
            #print(write_path)
         #   print(1000)
            fo = open(write_path, "w",encoding='utf-8')
          #  print(1000)
           # print(6)
           # print(txt)
            for i in txt_list:
               # print(1000)
                # print(type(i.strip()))
                print(i)
                fo.write(i.replace(' ', ''))
                fo.write('\n')
            fo.close()
           # print(txt_list)
 #浏览器配置
    else:
        page_return=0
        return
def get_livetxt(url):
 print(4)
 print(url)

 number = re.findall(r'\b[0-9][0-9]{4,7}\b',url)[0]
 #print(number)
 url_='http://api.sports.sina.com.cn/?p=live&s=livecast&a=livecastlog&id='+number+'&dpc=1'#真正的要访问的url
 print(url_)
 msg=[]
 total_time=[]
 score=[]
 driver.get(url_)
 soup = BeautifulSoup(driver.page_source, 'lxml')
 #如果得到的url是一个网站
 if (soup.find('pre')==None):
     print("选择1")
     msg,total_time,score=get_txt_direct(url)
 #如果得到的url是直接一个数据库文件
 else:
     print('选择2')
     msg,total_time,score=get_txt_indirect(url_)
 global page_list
 page_in_list = 0
 judge=0#定义的是上半场最终访问时间
 workbook=xlwt.Workbook()#excle打开
 sheet1=workbook.add_sheet('sheet1',cell_overwrite_ok=True)
 #txt=soup.find("tbody")
 #print(txt)
 list=0
 #a=['上' ,'下','完']
 print(1000)
 write_path = '/Users/hejie/Desktop/课外学习/数据集/新浪直播数据/实录/'+str(page_list)+'.xls'
 print(write_path)
 # for i in txt('tr'):
 #    if(i('td')[2]):
 #     if(i('td')[2].get_text()[0] not in a ):
 #        continue
 #     elif(i('td')[2].get_text()[0]=='完' and list<2):
 #         #print(i('td'))
 #         sheet1.write(page_in_list, 0, i('td')[1].get_text().strip())
 #         sheet1.write(page_in_list, 1, "完赛")
 #         sheet1.write(page_in_list, 2, i('td')[3].get_text().strip())
 #         page_in_list=page_in_list+1
 #         list=list+1
 #         #print(list)
 #     elif(i('td')[2].get_text()[0]=='上'):#记得将下半场的时间加上上半场的时间
 #         sheet1.write(page_in_list, 0, i('td')[1].get_text().strip())
 #         sheet1.write(page_in_list, 1, re.findall(r'[0-9]+',i('td')[2].get_text())[0])
 #         sheet1.write(page_in_list, 2, i('td')[3].get_text().strip())
 #         judge=re.findall(r'[0-9]+',i('td')[2].get_text())
 #         page_in_list = page_in_list + 1
 #     else:
 #         sheet1.write(page_in_list, 0, i('td')[1].get_text().strip())
 #         sheet1.write(page_in_list, 1, str(int(re.findall(r'[0-9]+', i('td')[2].get_text())[0])+judge))
 #         sheet1.write(page_in_list, 2, i('td')[3].get_text().strip())
 #         page_in_list = page_in_list + 1
 #         print(i('td'))
 #     print(3)
 for i in range(len(msg)):
    sheet1.write(page_in_list, 0, msg[i])
    sheet1.write(page_in_list, 1, total_time[i])
    sheet1.write(page_in_list, 2, score[i])
    page_in_list=page_in_list+1
 workbook.save(write_path)#存放excle表
 page_list=page_list+1#
 #全局变量在外面赋值
def get_txt_indirect(url):#有些网站分钟没有直接显示出来
    msg=[]
    total_time=[]
    score=[]
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # 定义一个文本，其是直播数据
    txt = soup.find('pre').get_text()

    txt = re.findall(r'\[.*\]', txt)
    txt = txt[0]
    print(txt)
    jo = json.loads(txt)

    shang_end=0 #end标志标志比赛的结束最多有两个
    # json_number=0
    for i in jo:
        if ('st' in  i and i['st']!=None ):
             if ('q' in i ):
                  if(i['q']==1):
                      if(':' in i['m']):
                          continue
                      msg.append(i['m'].replace('.',''))
                      total_time.append((i['st']//60)+1)
                      score.append(i['s']['s1']+'-'+i['s']['s2'])
                      # print(i['m'])
                      # #print('上半场')
                      # print((i['st']//60)+1)
                      # print(i['s']['s1']+'-'+i['s']['s2'])

                      shang_end=(i['st']//60)+1#标记上半场的结束时间
                  elif(i['q']==2):
                      if (':' in i['m']):
                          continue
                      msg.append(i['m'].replace('.',''))
                      total_time.append((i['st'] // 60) + 1+shang_end)
                      score.append(i['s']['s1'] + '-' + i['s']['s2'])
                      # print(i['m'])
                      # #print('下半场')
                      # print((i['st'] // 60) + 1+shang_end)
                      # print(i['s']['s1'] + '-' + i['s']['s2'])

                  elif(i['q']==5):
                      if (':' in i['m']):
                          continue
                      if (len(re.findall(r'[0-9]-[0-9]',i['m']))==1):
                          msg.append(i['m'].replace('.',''))
                          total_time.append('完赛')
                          score.append(i['s']['s1'] + '-' + i['s']['s2'])
                          # print(i['m'])
                          # print('完赛')
                          # print(i['s']['s1'] + '-' + i['s']['s2'])
                          # print(1000)
                          break
                      else:
                          continue
                      #print(re.findall(r'[0-9]-[0-9]',i['m']))

                  else:
                      continue
             else:
                 continue
        else:
            continue
    #print(1000)
    return msg,total_time,score
#有些网站分钟直接显示出来了
def get_txt_direct(url):
    msg = []
    total_time = []
    score = []
    global page_list
    page_in_list_=0
    driver.get(url)
    judge = 0
    # workbook = xlwt.Workbook()
    #        sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    txt = soup.find("tbody")
    # print(3)
    # print(txt)
    list = 0
    a = ['上', '下', '完']
    start_time=0#记录上半场时间
    #        write_path = "E:直播数据\新郎直播数据\实录\\" + str(page_list) + ".xls"

    # workbook.save(write_path)
#    page_list = page_list + 1  #
    for i in txt('tr')[::-1]:
        #print(i('th')[0])
        if (i.find('th')):
            #print(1000)
            #print(type(i('th')[0].get_text()))
            if (re.findall(r'[0-9]+',i('th')[0].get_text())):
                #print(1000)
                #print(page_in_list_, 0, i('td')[0].get_text().strip())
                if (':' in i('td')[0].get_text()):
                    continue
                msg.append(i('td')[0].get_text().replace('.','').strip())
                if(len(re.findall(r'[0-9]+',i('th')[0].get_text()))==1):#如果时间的长度为1，就调用一个就行 ，否则两者相加
                    total_time.append(re.findall(r'[0-9]+',i('th')[0].get_text())[0])
                   # print(page_in_list_, 1, re.findall(r'[0-9]+',i('th')[0].get_text())[0])
                    start_time=re.findall(r'[0-9]+',i('th')[0].get_text())[0]
                else:
                    time_=0
                    for  time_1 in re.findall(r'[0-9]+',i('th')[0].get_text()):
                       time_=time_+int(time_1)
                    total_time.append(time_)
                   # print(page_in_list_, 1, time_)
                    start_time = re.findall(r'[0-9]+', i('th')[0].get_text())[0]
                score.append(i('td')[1].get_text().strip())
                #print(page_in_list_, 2, i('td')[1].get_text().strip())
                page_in_list_ = page_in_list_ + 1
            elif (i('th')[0].get_text().replace(' ','').strip()=="" and int(start_time)>80):
                  if(re.findall(r'[0-9]-[0-9]',i('td')[0].get_text())):
                  # print(i('td'))
                    if (':' in i('td')[0].get_text()):
                      continue
                    msg.append(i('td')[0].get_text().replace('.','').strip())
                    total_time.append("完赛")
                    score.append(i('td')[1].get_text().strip())
                    # print(page_in_list_, 0, i('td')[0].get_text().strip())
                    # print(page_in_list_, 1, "完赛")
                    # print(page_in_list_, 2, i('td')[1].get_text().strip())
                    page_in_list_ = page_in_list_ + 1
                    list = list + 1
                    break
                  else:
                      continue
                # print(list)
            else:
              continue
        else:
            continue
        #print(3)
    return msg,total_time,score
service_args=[]
#设置驱动器的浏览器
driver=webdriver.Chrome( )
page_list=4564
page_return=1
real_name=[]
#获取网页地址
#方法体2：切换到新窗口中,点击新窗口中的按钮
#driver.switch_to.window(driver.window_handles[1])
'''
link=element.get_attribute('href')#获取到链接地址，然后进行跳转
driver.navigate().to(link)
driver.implicitly_wait(10)#等待10s，有可能链接还不能找到
element.click()模拟元素点击
'''
driver.implicitly_wait(2) #等待10s以便页面加载完全
#element=driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/a[2]")#找到直播数据按钮
#element.click()
#driver.implicitly_wait(2)#等待10s以便页面加载完全

#抓取直播里面的文字信息

#element=driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/a[6]")#找到战报元素
#print (5)#一个断点低级提示
#element.click() #点击战报元素
#mse=get_txt(url_new)

#a=['1','2','3','4']
#soup=BeautifulSoup(driver.page_source, 'lxml')
#txt1=soup.find('div',class_='article-a__content')
#for i in txt1('p')[:-1]:
    # if('strong' in i.prettify())
    #     #print(len(i('strong')[0].get_text()))
    #     print(i('strong')[0].get_:text()[-3])
    #     #print("dasdsadsa")
    #     if(i('strong')[0].get_text()[-3] in  a):
    #         #print(321321)
    #         continue
   # print(i.get_text().replace(" ","").strip())
    #print(i)
#fo.close()
years=['2012','2013','2014','2015','2016','2017']
mouth=['01','02','03','04','05','06','07','08','09','10','11','12']
days1=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
days2=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
days3=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']
days4=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29']
try:
 for i in years[0:]:
    if(i== '2012' ):
         for m in mouth[0:]:#每次出问题记得更改
               if(m in ['06']):
                   for n in days1[16:]:
                      print(i + '-' + m + '-' + n)
                      print(
                          'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                      search('http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate='+i+'-'+m+'-'+n)
               elif (m in [ '09']):
                   for n in days1[25:]:
                       print(i + '-' + m + '-' + n)
                       print(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                       search(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
               elif (m in [ '11']):
                   for n in days1[28:]:
                       print(i + '-' + m + '-' + n)
                       print(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                       search(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
               elif(m in ['07']):
                   for n in days2[22:]:
                       search(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                       print(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                       print(i + '-' + m + '-' + n)
               elif(m in ['08']):
                   for n in days2[21:]:
                       search(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                       print(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                       print(i + '-' + m + '-' + n)
               elif(m in ['10']):
                   for n in days2[30:]:
                       search(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                       print(
                           'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                       print(i + '-' + m + '-' + n)
               else:
                   for n in days2[30:]:
                      search(
                       'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                      print(
                       'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                      print(i + '-' + m + '-' + n)
    elif( i == '2016'):
        for m in mouth[11:]:
            if (m in [ '11']):
                for n in days1[23:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in ['09']):
                for n in days1[13:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in [ '06']):
                for n in days1[18:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in ['04']):
                for n in days1[8:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in ['02']):
                for n in days4[2:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif(m in ['05']):
                for n in days2[4:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif(m in ['07']):
                for n in days2[1:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif(m in ['12']):
                for n in days2[9:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            else:
                for n in days2:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
    elif(i=='2013'):
                    for m in mouth[9:]:
                        if (m in [  '11']):
                            for n in days1:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                                print(i + '-' + m + '-' + n)
                        elif (m in ['09']):
                            for n in days1[28:]:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                                print(i + '-' + m + '-' + n)
                        elif (m in ['04']):
                            for n in days1[26:]:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                                print(i + '-' + m + '-' + n)
                        elif (m in ['06']):
                            for n in days1[1:]:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                                print(i + '-' + m + '-' + n)
                        elif (m in ['02']):
                            for n in days3[15:]:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                                print(i + '-' + m + '-' + n)
                        elif(m in ['01']):
                            for n in days2:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                            print(i + '-' + m + '-' + n)
                        elif(m in ['03']):
                            for n in days2[30:]:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                            print(i + '-' + m + '-' + n)
                        elif (m in ['10']):
                            for n in days2[23:]:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                            print(i + '-' + m + '-' + n)
                        elif (m in ['07']):
                            for n in days2[2:]:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                            print(i + '-' + m + '-' + n)
                        else:
                            for n in days2:
                                search(
                                    'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                            print(i + '-' + m + '-' + n)
    elif(i=='2014'):
        for m in mouth[11:]:
            if (m in ['04',  '09']):
                for n in days1:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif(m in ['12']):
                for n in days2[13:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif (m in ['11']):
                for n in days1[26:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in [ '06']):
                for n in days1[28:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in ['02']):
                for n in days3[24:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif(m in ['07']):
                for n in days2[12:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif(m in ['08']):
                for n in days2[15:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif(m in ['10']):
                for n in days2[23:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            else:
                for n in days2:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
    elif(i=='2015'):
        for m in mouth[8:]:
            if (m in [ '06', '11']):
                for n in days1:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in ['09']):
                for n in days1[23:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in ['04']):
                for n in days1[14:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in ['02']):
                for n in days3:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif(m in ['01']):
                for n in days2[22:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif(m in ['03']):
                for n in days2[29:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif(m in ['05']):
                for n in days2[2:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif(m in ['07']):
                for n in days2[26:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            else:
                for n in days2:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
    else:
        for m in mouth[11:]:
            if (m in [ '06', '09']):
                for n in days1:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in [ '11']):
                for n in days1[29:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in ['04']):
                for n in days1[26:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif (m in ['02']):
                for n in days3[19:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                    print(i + '-' + m + '-' + n)
            elif(m in ['01']):
                for n in days2[11:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif(m in ['03']):
                for n in days2[23:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif(m in ['05']):
                for n in days2[13:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif (m in ['07']):
                for n in days2[18:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif(m in ['08']):
                for n in days2[27:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            elif(m in ['10']):
                for n in days2[27:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
            else:
                for n in days2[16:]:
                    search(
                        'http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=' + i + '-' + m + '-' + n)
                print(i + '-' + m + '-' + n)
 #search('http://match.sports.sina.com.cn/index.html#type=schedule&matchtype=all&filtertype=time&livetype=ed&scheduledate=2017')
 driver.quit()
except Exception as e:
  print(e)
else:
 print("error")


