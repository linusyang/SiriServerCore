#!/usr/bin/python
# -*- coding: utf-8 -*-

#author: AlphaBetaPhi <beta@alphabeta.ca>
#todo: check for existing alarms, delete alarms, update alarms, add original commands aka wake me up/tomorrow morning/midnight/etc.
#project: SiriServer
#commands: set an alarm for HH:MM AM/PM
#          set an alarm for HH AM/PM
#          set an alarm for HH AM/PM <called/labeled/named> <[word 1] [word 2] [word 3]>
#comments: feel free to email any comments/bug/updates
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

import re
from fractions import Fraction
from plugin import *
from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject
from siriObjects.alarmObjects import *

dict = {u'零':0, u'一':1, u'二':2, u'三':3, u'四':4, u'五':5, u'六':6, u'七':7, u'八':8, u'九':9, u'十':10, u'百':100, u'千':1000, u'万':10000,
   u'０':0, u'１':1, u'２':2, u'３':3, u'４':4, u'５':5, u'６':6, u'７':7, u'８':8, u'９':9,
            u'壹':1, u'贰':2, u'叁':3, u'肆':4, u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9, u'拾':10, u'佰':100, u'仟':1000, u'萬':10000, u'亿':100000000}
   
def toNum(a, encoding="utf-8"):
    if isinstance(a, str):
        a = a.decode(encoding)
    if a == None:
        return 0
    else:
        a, tmp = re.subn("[a-zA-Z ]", "", a)
    count = 0 
    result = 0
    tmp = 0
    Billion = 0
    chs = 0
    digit = 0
    while count < len(a):
        tmpChr = a[count]
        tmpNum = dict.get(tmpChr, None)
        if tmpNum == None:
            count += 1
            continue
        else:
            chs = 1
        if tmpNum == 100000000:
            result = result + tmp
            result = result * tmpNum
            Billion = Billion * 100000000 + result 
            result = 0
            tmp = 0
        elif tmpNum == 10000:
            result = result + tmp
            result = result * tmpNum
            tmp = 0
        elif tmpNum >= 10:
            if tmp == 0:
                tmp = 1
            result = result + tmpNum * tmp
            tmp = 0
        elif tmpNum is not None:
            tmp = tmp * 10 + tmpNum
        count += 1
    result += tmp + Billion
    if (chs == 0) and (result == 0):
        p = re.compile("[^0-9]*([0-9]+)[^0-9]*").match(a)
        if p:
            result = int(p.group(1))
            digit = 1
    if ((chs == 1) or (digit == 1)) and (result <= 12) and (a.count(u"晚上") > 0 or a.count(u"夜里") > 0 or a.count(u"下午") > 0):
        result = (result + 12) % 24
    return result

class alarmPlugin(Plugin):
    localizations = {
        'Alarm': {
            "settingAlarm": {
                "en-US": u"Setting the Alarm\u2026",
                "zh-CN": u"设置闹钟\u2026",
                "fr-FR": u"Réglage de l'alarme\u2026"
            }, "alarmWasSet": {
                "en-US": "Your alarm is set for {0}:{1} {2}.",
                "zh-CN": u"您的闹钟已设在{0}点{1}分 {2}。",
                "fr-FR": u"Votre alarme est programmée pour {0}:{1} {2}"
            }, "alarmSetWithLabel": {
                "en-US": "Your alarm {0} {1} is set for {2}:{3} {4}.",
                "zh-CN": u"您的闹钟“{0}”已设在{2}点{3}分 {4}。",
                "fr-FR": u"Votre alarme {0} {1} est programmée pour {2}:{3} {4}"
            }
        }
    }

    res = {
        'setAlarm': {
            'en-US': '.*set.* alarm for.* (0?[1-9]|1[012])([0-5]\d)?\s?([APap][mM])\s?(\bcalled|named|labeled\b)?\s?(([a-z0-9]{1,7}\s)?([a-z0-9]{1,7})\s?([a-z0-9]{1,7}))?',
            'zh-CN': u'(?u).*闹钟(.*在|.*为|设.|定.|订.)?\s*([\w ]+)\s*(点整|点钟|点半|点|小时)+\s*(([\w ]+)分)?钟?\s*(叫做([\w ]+))?',
            'fr-FR': u'.*(programme|regle|règle|met|mai).*(alarme|reveil|réveil)([^0-9]+)([0-2]?[0-9])([^0-9]+)?([0-5]?[0-9])?\s?(\appelée|appel|nommée|nommee|labellé|labelle\b)?\s?(([a-z0-9]{1,7}\s)?([a-z0-9]{1,7})\s?([a-z0-9]{1,7}))?'
        }
    }

    @register("en-US", res['setAlarm']['en-US'])
    @register("zh-CN", res['setAlarm']['zh-CN'])
    @register("fr-FR", res['setAlarm']['fr-FR'])
    def setAlarm(self, speech, language):
        
        alarmString = re.match(alarmPlugin.res['setAlarm'][language], speech, re.IGNORECASE)

        if language == 'fr-FR':
            labelGroupId = 8
            alarmHour = int(alarmString.group(4))
            alarm24Hour = alarmHour
            alarmMinutes = alarmString.group(6)
            alarmAMPM = ""
            alarmLabelExists = alarmString.group(labelGroupId)
        elif language == 'zh-CN':
            labelGroupId = 7
            alarmHour = toNum(alarmString.group(2))
            alarm24Hour = alarmHour
            if alarmString.group(3) == u'点半':
                alarmMinutes = str(30)
            else:
                alarmMinutes = str(toNum(alarmString.group(5)))
            alarmAMPM = ""
            alarmLabelExists = alarmString.group(labelGroupId)
        else:
            labelGroupId = 4
            alarmHour = int(alarmString.group(1))
            alarm24Hour = alarmHour
            alarmMinutes = alarmString.group(2)
            alarmAMPM = alarmString.group(3)
            alarmLabelExists = alarmString.group(labelGroupId)

        #check if we are naming the alarm
        if alarmLabelExists == None:
            alarmLabel = None
        else:
            alarmLabel = alarmString.group(labelGroupId)

        #the siri alarm object requires 24 hour clock
        if (alarmAMPM == "pm" and alarmHour != 12):
            alarm24Hour += 12
        if alarmMinutes == None:
            alarmMinutes = "00"
        else:
            alarmMinutes = int(alarmMinutes.strip())
        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [
            AssistantUtteranceView(
                speakableText=alarmPlugin.localizations['Alarm']['settingAlarm'][language],
                dialogIdentifier="Alarm#settingAlarm")]
        self.sendRequestWithoutAnswer(view)

        #create the alarm
        alarm = AlarmObject(alarmLabel, int(alarmMinutes), alarm24Hour, None, 1)
        response = self.getResponseForRequest(AlarmCreate(self.refId, alarm))
        #print(alarmPlugin.localizations['Alarm']['alarmWasSet'][language].format(alarmHour, alarmMinutes, alarmAMPM))
        view = AddViews(self.refId, dialogPhase="Completion")
        if alarmLabel == None:
            view1 = AssistantUtteranceView(speakableText=alarmPlugin.localizations['Alarm']['alarmWasSet'][language].format(alarmHour, alarmMinutes, alarmAMPM), dialogIdentifier="Alarm#alarmWasSet")
        else:
            view1 = AssistantUtteranceView(speakableText=alarmPlugin.localizations['Alarm']['alarmSetWithLabel'][language].format(alarmLabelExists, alarmLabel, alarmHour, alarmMinutes, alarmAMPM), dialogIdentifier="Alarm#alarmSetWithLabel")
        view2 = AlarmSnippet(alarms=[alarm])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()