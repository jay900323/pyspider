#coding=utf-8
import re
import urllib2
import urllib
import cut
import os  

send_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Encoding': 'identity',
                'Connection': 'keep-alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9, */*;q=0.8',
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'}

def getContent(url):
    opener = urllib2.build_opener()
    req = urllib2.Request(url, headers=send_headers)
    data = ''
    try:
        res = urllib2.urlopen(req)
        data = res.read()
    except urllib2.URLError, e:
        data = e.read()
    return data

#'http://223.112.4.118:8001/web/image/login/vCode.aspx?11:59:17'
def loadImage(url):
    for i in range(0, 100):
        data = getContent(url)
        file = open('image\\' + str(i)+'.jpg', 'wb')
        file.write(data)
        file.close()
        

if __name__ == '__main__':
    loadImage('http://lljiuzhu.mca.gov.cn:8090/insiis6/verifyCode')
