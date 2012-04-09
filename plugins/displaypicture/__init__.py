# -*- coding: utf-8 -*-
#displaypicture.py

#Google Image Plugin v0.2
#by Ryan Davis (neoshroom)
#feel free to add to, mess with and use this plugin with original attribution
#additional Google Image functions to add can be found at:
#https://developers.google.com/image-search/v1/jsondevguide#request_format

#usage: say "display a picture of william shakespeare" 
#(or anything else you want a picture of)

# Must be before wwwsearch plugin
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

import re
import urllib2, urllib
import json

from plugin import *
from plugin import __criteria_key__

from siriObjects.uiObjects import AddViews
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine

class displaypic(Plugin):
    
    @register("de-DE", "(zeig mir|zeige|zeig).*(bild|zeichnung) (vo. ein..|vo.|aus)* ([\w ]+)")
    @register("en-US", "(display|show me|show).*(picture|image|drawing|illustration) (of|an|a)* ([\w ]+)")
    @register("zh-CN", u".*(找|显示|给我看)(关于|有关)?([\w ]+)(的图).*")
    @register("fr-FR", u"(montre|affiche|recherche|cherche|dessine)?.*(photos?|images?|dessins?|illustrations?) (une?|pour|de la|de l'|des|du|de|d'une?|d'|l')* ?([\w ]+)")
    def displaypicture(self, speech, language, regex):
        if language == "zh-CN":
            Title = regex.group(3).strip()
        else:
            Title = regex.group(regex.lastindex).strip()
        Query = urllib.quote_plus(Title.encode("utf-8"))
        SearchURL = u'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&imgsz=small|medium|large|xlarge&q=' + str(Query)
        try:
            if language == "zh-CN":
                self.say(u"这是有关{0}的图片：".format(Title))
            else:
                self.say("Here is the image for "+Title+"...")
            jsonResponse = urllib2.urlopen(SearchURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
            ImageURL = jsonDecoded['responseData']['results'][0]['unescapedUrl']
            view = AddViews(self.refId, dialogPhase="Completion")
            ImageAnswer = AnswerObject(title=Title,lines=[AnswerObjectLine(image=ImageURL)])
            view1 = AnswerSnippet(answers=[ImageAnswer])
            view.views = [view1]
            self.sendRequestWithoutAnswer(view)
            self.complete_request()
        except (urllib2.URLError):
            if language == "zh-CN":
                self.say(u"抱歉，我无法连接谷歌图片服务。")
            else:
                self.say("Sorry, a connection to Google Images could not be established.")
            self.complete_request()
