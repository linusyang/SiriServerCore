#!/usr/bin/python
# -*- coding: utf-8 -*-

#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

import os, sys
from datetime import date
import locale 
from plugin import *

class talkToMe(Plugin):   
        
    @register("de-DE", ".*status.*")
    @register("en-US", ".*status.*")
    @register("zh-CN", u".*状态.*")
    def ttm_uptime_status(self, speech, language):
        uptime = None
        servertype = ' '.join(os.uname())
        freemem = None
        if os.name == "posix":
            try:
                uptime = os.popen("uptime").read()
            except:
                pass
        if sys.platform.startswith('linux'):
            freemem = os.popen("grep MemFree /proc/meminfo").read()
        if (uptime == None) and (freemem == None) and (servertype == None):
            if language == 'zh-CN':
                self.say(u'您的服务器系统不支持状态查询。')
            else:
                self.say(u"Sorry, I can't get status from you server")
        elif language == 'de-DE':
            self.say('Hier ist der Status:')
            if servertype != None:
                self.say(servertype, ' ')
            if uptime != None:
                self.say(uptime, ' ')
            if freemem != None:
                self.say(freemem, ' ')
        elif language == 'zh-CN':
            self.say(u'服务器状态')
            if servertype != None:
                self.say(servertype, u'这是服务器类型。')
            if uptime != None:
                self.say(uptime, u'这是运行时间。')
            if freemem != None:
                self.say(freemem, u'这是剩余内存。')
        else:
            self.say('Here is the status:')
            if servertype != None:
                self.say(servertype, 'This is the server system.')
            if uptime != None:
                self.say(uptime, 'This is running time.')
            if freemem != None:
                self.say(freemem, 'And size of free memory.')
        self.complete_request()     
    
    
    @register("de-DE", "(Welcher Tag.*)|(Welches Datum.*)")
    @register("en-US", "(What Day.*)|(What.*Date.*)")
    @register("zh-CN", u"(.*几号.*)|(.*日期.*)")
    
    def ttm_say_date(self, speech, language):
        now = date.today()
        if language == 'de-DE':
            try:
                locale.setlocale(locale.LC_ALL, 'de_DE')
            except:
                pass
            result=now.strftime("Heute ist %A, der %d.%m.%Y (Kalenderwoche: %W)")
            self.say(result)
        elif language == 'zh-CN':
            try:
                locale.setlocale(locale.LC_ALL, 'zh-CN')
            except:
                pass
            result = u"今天是"
            result += now.strftime("%Y年%m月%d日，第%W周，%A。").decode("utf-8")
            self.say(result)
        else:
            try:
                locale.setlocale(locale.LC_ALL, 'en_US')
            except:
                pass
            result=now.strftime("Today is %A the %d.%m.%Y (Week: %W)")
            self.say(result)
        self.complete_request()
