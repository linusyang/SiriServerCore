#!/usr/bin/python                                                                                                                                                                   
# -*- coding: utf-8 -*-                                                                                                                                                             
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

from plugin import *
from siriObjects.websearchObjects import WebSearch

class wwwSearch(Plugin):
    @register("de-DE", "(websuche.*)|(web suche.*)|(internetsuche.*)|(internet suche.*)|(web.*)|(internet.*)")
    @register("en-US", "(web search.*)|(web.*)|(internet.*)|(internet search.*)|(google.*)")
    @register("zh-CN", u".*(搜索|google|谷歌)([\w ]+)")
    @register("fr-FR", u".*(recherche web de|rechercher? sur internet|chercher? sur internet|recherche de|rechercher?|chercher?|google|trouver?)(.*)(?!wiki(pedia)?)$")
    def webSearch(self, speech, language, regex):
        if (language == "en-US"):
            if (speech.find('Web search') == 0):
                speech = speech.replace('Web search', ' ',1)
            elif (speech.find('Web') == 0):
                speech = speech.replace('Web',' ',1)
            elif (speech.find('Internet search') == 0):
                speech = speech.replace('Internet search',' ',1)
            elif (speech.find('Internet') == 0):
                speech = speech.replace('Internet',' ',1)
            speech = speech.strip()
            if speech == "":
                speech = self.ask("What is your query?")
        elif(language == 'zh-CN'):
            speech = regex.group(regex.lastindex).strip()
            if(speech == ""):
                speech = self.ask(u"您想让我搜索什么？")
        elif(language == 'fr-FR'):
            speech = regex.group(regex.lastindex).strip()
            if(speech == ""):
                speech = self.ask(u"Que voulez-vous rechercher ?")
        elif (language == "de-DE"):
            if (speech.find('Websuche') == 0):
                speech = speech.replace('Websuche',' ',1)
            elif (speech.find('Web suche') == 0):
                speech = speech.replace('Web suche',' ',1)
            elif (speech.find('Internetsuche') == 0):
                speech = speech.replace('Internetsuche',' ',1)
            elif (speech.find('Internet suche') == 0):
                speech = speech.replace('Internet suche',' ',1)
            elif (speech.find('Web') == 0):
                speech = speech.replace('Web',' ',1)
            elif (speech.find('Internet') == 0):
                speech = speech.replace('Internet',' ',1)
            speech = speech.strip()
            if speech == "":
                speech = self.ask("Nach was soll ich suchen?")

        search = WebSearch(refId=self.refId, query=speech)
        self.sendRequestWithoutAnswer(search)
        self.complete_request()
