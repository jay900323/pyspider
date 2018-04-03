#coding=utf-8
import urllib2
import cookielib
COOKIES_DOMAIN = "baidu.com"
#声明一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler=urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib2.build_opener(handler)
#此处的open方法同urllib2的urlopen方法，也可以传入request
response = opener.open('http://www.baidu.com')

cookiesDict = {}
for c in cookie:
    if COOKIES_DOMAIN in c.domain:
        cookiesDict[c.name] = c.value
print cookiesDict

