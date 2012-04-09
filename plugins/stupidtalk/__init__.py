#!/usr/bin/python
# -*- coding: utf-8 -*-
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

from plugin import *
import random
import re
import urllib2, urllib, uuid
import json
from urllib2 import urlopen
from xml.dom import minidom

class smalltalk(Plugin):

    @register("en-US", "(testing)|(test)")
    @register("zh-CN", u".*(测试|试试).*")
    def st_test(self, speech, language):
        if language == 'en-US':
            self.say(u"Mission Control, I read you loud and clear, {0}".format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"命令确认，我能听见你{0}。".format(self.user_name()))
        self.complete_request()
        
    @register("en-US","I.just.*")
    @register("zh-CN", u".*(你|我|他|是|很|好|来|去|只|不|要|想|对).*")
    @register("fr-FR",u"je.viens.*")
    def st_i_just(self, speech, language):
        if language == 'en-US':
            self.say("Really!?")
        elif language == 'zh-CN':
            rep = [u"是吗？", u"哇塞。", u"好吧。", u"遵命。", u"都听你的。", u"嗨！", u"嘿！", u"哟呵！"]
            self.say(random.choice(rep))
        elif language == 'fr-FR':
            rep = [u"Vraiment !?", u"Cool !", u"Bravo !", u"Pas mal !", u"Super !"]
            self.say(random.choice(rep))
        self.complete_request()
        
    @register("de-DE", ".*Warum.*bin ich.*Welt.*")
    @register("en-US", ".*Why.*I.*World.*")
    @register("zh-CN", u".*(什|怎)么.*")
    @register("fr-FR", ".*Pourquoi.*je.*monde.*")
    def st_why_on_world(self, speech, language):
        if language == 'de-DE':
            self.say("Das weiß ich nicht.")
            self.say("Ehrlich gesagt, frage ich mich das schon lange!")
        elif language == 'fr-FR':
            self.say("Je ne sais pas.")
            self.say(u"Je me le demande moi-même depuis longtemps")
        elif language == 'zh-CN':
            rep = [u"我也不懂。", u"无可奉告。", u"不知道呀。", u"你猜呢？", u"就不告诉你。", u"我搞不定。"]
            self.say(random.choice(rep))
        else:
            self.say("I don't know")
            self.say("I have asked my self this for a long time!")
        self.complete_request()
