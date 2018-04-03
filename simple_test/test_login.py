#coding=utf-8
import urllib2
import cookielib

COOKIES_DOMAIN = '172.16.39.197'
HOST = '172.16.39.197:8080'
REFERER = 'http://172.16.39.197:8080/webscan/login'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
HTTP_HEADERS = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch',
    'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection' : 'keep-alive',
    'DNT' : '1',
    'Host' : HOST,
    'Referer' : REFERER,
    'User-Agent' : USER_AGENT,
}

cookiesJar = cookielib.CookieJar()
cookieProcessor = urllib2.HTTPCookieProcessor(cookiesJar)
cookieOpener = urllib2.build_opener(cookieProcessor, urllib2.HTTPHandler)
for item in HTTP_HEADERS:
    cookieOpener.addheaders.append ((item ,HTTP_HEADERS[item]))
urllib2.install_opener(cookieOpener)


req = urllib2.Request(url = "http://172.16.39.197:8080/webscan/login", data = 'username=admin&password=365sec')
resp = urllib2.urlopen(req)

cookiesDict = {}
for c in cookiesJar:
    print c.domain
    if COOKIES_DOMAIN in c.domain:
        cookiesDict[c.name] = c.value
print cookiesDict

req2 = urllib2.Request(url = "http://172.16.39.197:8080/webscan/")
resp = urllib2.urlopen(req2)
#print resp.read()


