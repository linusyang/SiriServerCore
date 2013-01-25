#!/usr/bin/python
# -*- coding: utf-8 -*-
# Written by Linus Yang <laokongzi@gmail.com>

from plugin import *
import json
import urllib2
import cookielib
import re

class SimiWorker:

    def __init__(self):
        self.cjar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cjar))
        self.opener.addheaders = [('Referer','http://www.simsimi.com/talk.htm')]
        try:
            self.opener.open('http://www.simsimi.com/talk.htm')
        except:
            pass
        self.url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'

    def chat(self, message=''):
        message = message.encode('utf-8').strip()
        if message != '':
            try:
                r = self.opener.open(self.url % message.strip()).read()
                return json.loads(r)['response']
            except:
                return u'让我再想想。'
        else:
            return u'我没听清，可以再说一遍吗？'
                              
class SimiTalk(Plugin):

    @register("zh-CN", u".*")
    def Simi_Message(self, speech, language):
        simiWorker = SimiWorker()
        if language == 'zh-CN':
            self.say(simiWorker.chat(speech))
	    self.complete_request()
