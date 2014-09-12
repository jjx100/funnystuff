#!/usr/bin/python
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
#from __future__ import unicode_literals

import urllib2
import urllib

website = 'http://www.cnbeta.com/comment'
article_num = 326973

postdata = urllib.urlencode({
    'SID':"326973",
    'SN':"22074"
})
#    'POST_URL':"/comment",
#    'POST_VIEW_URL':"/cmt",
#    'EMOTION_URL':"/comment?op=emotion",

headers = {
    'Referer':'http://www.cnbeta.com/articles'
}

#articleurl = website + '/' + str(article_num)
articleurl = website

req = urllib2.Request(url = articleurl, headers = headers, data = postdata)

try:
    response = urllib2.urlopen(req)
    html = response.read()
    print('content:', html)
    info = response.info()
    print('info:', info)
except urllib2.URLError as e:
    print(e.reason)


