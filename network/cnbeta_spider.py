#!/usr/bin/python
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
#from __future__ import unicode_literals

import urllib2
import urllib
import gzip, json, base64, re
from StringIO import StringIO

class CNbeta_spider:
    def __init__(self):
        self.url = 'http://www.cnbeta.com'
        
    def setHeader(self, referer):
        self.headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip,deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'25',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.cnbeta.com',
            'Origin':'http://www.cnbeta.com',
            'Referer':referer,
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
         }
    
    def parseMainUrl(self):
        header = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
            'Referer':'http://www.cnbeta.com'
        }
        req = urllib2.Request(url = self.url, headers = header)
        response_obj = urllib2.urlopen(req)
        response = response_obj.read()
        print(response)

    def run(self):
        self.parseMainUrl()

spider = CNbeta_spider()
spider.run()
        
'''
website = 'http://www.cnbeta.com/cmt'
article_num = 326973

postdata = urllib.urlencode({
     'op':'MSwzMjgwNDUsZTE0Mjc='
})
#    'POST_URL':"/comment",
#    'POST_VIEW_URL':"/cmt",
#    'EMOTION_URL':"/comment?op=emotion",

headers = {
    'Referer':'http://www.cnbeta.com/articles',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip,deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Length':'25',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Host':'www.cnbeta.com',
    'Origin':'http://www.cnbeta.com',
    'Referer':'http://www.cnbeta.com/articles/328045.htm',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}


#articleurl = website + '/' + str(article_num)
articleurl = website

req = urllib2.Request(url = articleurl, headers = headers, data = postdata)

try:
    response = urllib2.urlopen(req)
    html = response.read()
    #print(html)
    info = response.info()

    #file = open('content')
    #all_text = file.read()
    buf = StringIO(html)
    zip_obj = gzip.GzipFile(fileobj=buf)
    dictinfo = json.loads(zip_obj.read())
    response_data_encode = dictinfo['result']
    print(response_data_encode)
    print('--------------decode----------------')
    response_data_decode = base64.b64decode(response_data_encode);
    print(response_data_decode)
    #print('info:', info)
except urllib2.URLError as e:
    print(e.reason)
'''

