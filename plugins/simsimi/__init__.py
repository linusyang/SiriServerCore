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

def respond(self, simiWorker, inputString):
    if re.match(u'.*(结束|停止|闭嘴).*', inputString) != None:
        self.say(u"那么不说了，拜拜，{0}。".format(self.user_name()))
        self.complete_request()
    else:
        answer = self.ask(simiWorker.chat(inputString))
        respond(self, simiWorker, answer)
    self.complete_request()
                              
class SimSimi(Plugin):

    @register("zh-CN", u".*(黄鸡|聊天|聊聊|说话|谈谈|谈话).*")
    def Simi_Message(self, speech, language):
        simiWorker = SimiWorker()
        if language == 'zh-CN':
            answer = self.ask(u"我们开始聊吧，如果不想聊了，说“结束聊天”或“停止聊天”就行了。")
            respond(self, simiWorker, answer)
	    self.complete_request()
