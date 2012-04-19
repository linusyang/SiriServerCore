#!/usr/bin/python
# -*- coding: utf-8 -*-
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

from plugin import *
from siriObjects.systemObjects import ResultCallback
import uuid

class examplePlugin(Plugin):
    
    @register("de-DE", ".*Sinn.*Leben.*")
    @register("en-US", ".*Meaning.*Life.*")
    @register("zh-CN", u".*生.*意义.*")
    def meaningOfLife(self, speech, language, matchedRegex):
        if language == 'de-DE':
            answer = self.ask(u"Willst du das wirklich wissen?")
            self.say(u"Du hast \"{0}\" gesagt!".format(answer))
        elif language == 'zh-CN':
            self.say(u"这很难说，或许哪位哲学家会知道吧。")
        else:
            self.say("That's easy...It's a philosophical question concerning the purpose and significance of life or existence.")
        self.complete_request()
    
    @register("de-DE", ".*standort.*test.*")
    @register("en-US", ".*location.*test.*")
    @register("zh-CN", u".*位置.*测试.*")
    @register("nl-NL", ".*locatie.*test.*")
    def locationTest(self, speech, language):
        location = self.getCurrentLocation(force_reload=True)
        if language == 'zh-CN':
            self.say(u"纬度: {0}, 经度: {1}".format(location.latitude, location.longitude))
        else:
            self.say(u"lat: {0}, long: {1}".format(location.latitude, location.longitude))
        self.complete_request()
          
