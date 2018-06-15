# -*- coding:utf-8
# -*- learn webspider



#import jieba

if __name__=='__main__':
    '''#print "HelloWorld!"
    #values = {'username':'mawenqi0729', 'password':'mwq0729'}
    values = {'stuid':'201500301324',
			'pwd':'mwq980729'}
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'       #请求的身份（chrome浏览器）
    data = urllib.urlencode(values)
    headers = {'User-agent':user_agent,
               'Referer':'https://my.csdn.net/my/mycsdn',
               'content-type':'application/x-javascript',
               'accept - language': 'zh - CN, zh;q = 0.9' }

    loginurl = 'http://bkjws.sdu.edu.cn/'
    gradeUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjcx.curscopre'

    # 请求访问成绩查询网址
    url = 'http://www.baidu.com'
    #url = 'https://passport.csdn.net/account/login'
    #url = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    #cookie.load('cookie.txt',ignore_discard=True, ignore_expires=True)
    cookieHandler = urllib2.HTTPCookieProcessor(cookie)
    request = urllib2.Request(loginurl,data,headers)
    httpHandler = urllib2.HTTPHandler(debuglevel=1)
    httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
    opener = urllib2.build_opener(httpHandler, httpsHandler,cookieHandler)
    #urllib2.install_opener(opener)
    try:
        response = opener.open(loginurl,data)
    except urllib2.HTTPError,e:
        print 'Error!!!!'
        print e.code
        print e.reason
    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value
    cookie.save(ignore_discard=True, ignore_expires=True)


    #print response.read()

    text = open('test.txt','r', encoding='utf-8').read()
    result = jieba.cut(text)
    for i in result:
        print(i)'''

    str='word'
    print (str.encode('utf-8').decode('utf-8'))
    #print unicode(str)







