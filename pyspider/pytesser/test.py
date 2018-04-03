from pytesser import *
from PIL import Image,ImageEnhance  
from PIL import *  
import urllib2
import urllib
import os
import cookielib

send_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Encoding': 'identity',
                'Connection': 'keep-alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9, */*;q=0.8',
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'}
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

def getContent(url, headers = {}, data = None):
    print headers
    req = urllib2.Request(url, headers=headers, data = data)
    
    data = ''
    try:
        res = opener.open(req)

        data = res.read()
        print res.info()
    except urllib2.URLError, e:
        data = e.read()
    return data

headers1 = {'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Encoding': 'identity',
                'Connection': 'keep-alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9, */*;q=0.8',
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Cookie': 'JSESSIONID=TjWHZL5LK2qJwrkBfY1WrjytPPSphcpFlF1FbNLZrvgPqPnCy07G!2024697742'}

request = urllib2.Request('https://58.213.72.30/ITManager/main.do', headers = headers1)
response = urllib2.urlopen(request)
print response.read()

import StringIO
data = getContent('https://58.213.72.30/ITManager/image.jsp', headers = send_headers)
file = open('a.jpg', 'wb')
file.write(data)
file.close()
im = Image.open(StringIO.StringIO(data))


#im = im.resize((400, 160), Image.NEAREST)
#im = im.convert('RGB')
#im = im.point(table, '1')
#im = im.convert('L')
text = image_to_string(im)
print text

send_data = 'loginId=dxyt&loginPwd=123456&vcode='+text
print send_data.strip()

headers = {
'Host': '58.213.72.30',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Content-Length': '39',
'Connection': 'close'
 }
for c in cookie:
    print c
    
print getContent('https://58.213.72.30/ITManager/toLogin.do', headers=headers, data = send_data.strip())

for c in cookie:
    print c

getContent('https://58.213.72.30/ITManager/main.do', headers = send_headers)
