#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-3-10 16:38:17
import urllib
import urllib2
import urlparse
import cookielib
import gzip
import StringIO
import logging
import time

logger = logging.getLogger('login')

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'

class Login(object):

    def __init__(self):
        self.cookiesJar = cookielib.CookieJar()
        self.cookieProcessor = urllib2.HTTPCookieProcessor(self.cookiesJar)
        self.cookieOpener = urllib2.build_opener(self.cookieProcessor, urllib2.HTTPHandler)
        urllib2.install_opener(self.cookieOpener)
        urllib2.socket.setdefaulttimeout(10)
        self.cookie_updatetime = {}
        self.update_interval = 3*60
        
    #说明： 获取验证码
    def getContent(self, url):
        scheme, netloc, path, params, qs, fragment = urlparse.urlparse(url)

        if scheme == netloc == '' and path:
            # By default we set the protocol to "http"
            scheme = 'http'
            netloc = path
            path = ''
                
        HTTP_HEADERS = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection' : 'keep-alive',
            'Host' : netloc,
            'User-Agent' : USER_AGENT,
        }
        domain = netloc.split(':')[0]
        data = ''
        try:
            url = url.replace(' ', '%20')
            req = urllib2.Request(url = url, headers = HTTP_HEADERS)
            res = urllib2.urlopen(req)
            
            isGzip = res.headers.get('Content-Encoding')
            if isGzip == 'gzip':
                compresseddata = res.read()
                compressedstream = StringIO.StringIO(compresseddata)
                gzipper = gzip.GzipFile(fileobj=compressedstream)
                data = gzipper.read()
            else:
                data = res.read()
        except urllib2.URLError, e:
            data = e.read()
        return data
     
    #说明: urllib2会自动处理重定向的请求
    def getCookie(self, login_url, headers, data):
        
        scheme, netloc, path, params, qs, fragment = urlparse.urlparse(login_url)
        #
        # This is the case when someone creates a url_object like
        # this: url_object('www.w3af.com')
        #
        if scheme == netloc == '' and path:
            # By default we set the protocol to "http"
            scheme = 'http'
            netloc = path
            path = ''
                
        domain = netloc.split(':')[0]
        try:
            req = urllib2.Request(url = login_url, headers = headers, data = data)
            resp = urllib2.urlopen(req)
            cookiesDict = self.getDomainCookie(domain)
            return (resp, cookiesDict)
        except Exception, e:
            #在登录的时候如果带Cookie去登录但是始终无法登录成功的情况下可能cookie失效禁止登录了
            #此时需要重新去获取cookie 尝试重新登录
            logger.info('login error. url: {0} error: {1}'.format(login_url, str(e)))

            if self.getDomainCookie(domain):
                self.cookiesJar.clear(domain = domain)
                req = urllib2.Request(url = login_url, headers = headers, data = data)
                resp = urllib2.urlopen(req)
                cookiesDict = self.getDomainCookie(domain)
                return cookiesDict
            else:
                raise e
            
    #说明：在用户首次需要登录的时候使用getCookie 非首次登录的话 
    #返回值： 新Cookie
    def relogin(self, login_url, headers, data):
        scheme, netloc, path, params, qs, fragment = urlparse.urlparse(login_url)
        if scheme == netloc == '' and path:
            netloc = path
        domain = netloc.split(':')[0]
        cookie_update_time = self.cookie_updatetime.get(domain, None)
        if not cookie_update_time:
            #没有cookie更新记录
            self.getCookie(login_url, headers, data)
        else:
            if time.time() > self.update_interval + cookie_update_time:
                self.getCookie(login_url, headers, data)
        
        cookiesDict = self.getDomainCookie(domain)
        return cookiesDict
                
    def getDomainCookie(self, domain):
        cookiesDict = {}
        for c in self.cookiesJar:
            if domain in c.domain:
                cookiesDict[c.name] = c.value
        return cookiesDict
    
    def GetHtml(self, res):
        isGzip = res.headers.get('Content-Encoding')
        if isGzip == 'gzip':
            compresseddata = res.read()
            compressedstream = StringIO.StringIO(compresseddata)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()
        else:
            data = res.read()
        return data
    
    #说明：登录成功后记得调用此函数 记录上次登录成功的时间
    #        下次登录的时候直接从cookiejar中获取 
    #为什么要设置此函数  是时候因为登录成功只有脚本编写者知道 如果登录失败也记录cookie 那么下次可能会获取到无效的cookie
    def set_login_sucessful(self, domain):
        self.cookie_updatetime[domain] = time.time()
        
login = Login()
