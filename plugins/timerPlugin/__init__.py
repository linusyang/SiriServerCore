#!/usr/bin/python
# -*- coding: utf-8 -*-
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

import re

from fractions import Fraction

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject
from siriObjects.timerObjects import *


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
    error = 0  
    while count < len(a):
        tmpChr = a[count]
        tmpNum = dict.get(tmpChr, None)
        if tmpNum == None:
            error = 1
            break
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
    if error == 1:
        try:
            return int(a)
        except:
            return 0
    result = result + tmp
    result = result + Billion
    return result

def parse_number(s, language):
    # check for simple article usage (a, an, the)
    if re.match(timerPlugin.res['articles'][language], s, re.IGNORECASE):
        return 1
    f = 0
    for part in s.split(' '):
        f += float(Fraction(part))
    return f


def parse_timer_length(t, language):
    seconds = None
    for m in re.finditer(timerPlugin.res['timerLength'][language], t, re.IGNORECASE):
        print(m.groups())
        seconds = seconds or 0
        unit = m.group(2)[0]
        count = parse_number(m.group(1), language)
        if unit == 'h':
            seconds += count * 3600
        elif unit == 'm':
            seconds += count * 60
        elif unit == 's':
            seconds += count
        else:
            seconds += count * 60

    return seconds


class timerPlugin(Plugin):

    localizations = {
        'Timer': {
            'durationTooBig': {
               'en-US': 'Sorry, I can only set timers up to 24 hours.',
               'zh-CN': u'抱歉，我最多只能设置到24小时。',
               'fr-FR': u'Désolé, je peux uniquement régler le minuteur pour 24 heures.'
            }, "settingTimer": {
                "en-US": u"Setting the timer\u2026",
                "zh-CN": u"正在设置计时器…",
                "fr-FR": u"Démarrage du minuteur\u2026"
            }, 'showTheTimer': {
                'en-US': u'Here\u2019s the timer:',
                'zh-CN': u'这是您的计时器：',
                'fr-FR': u'Voici votre minuteur :'
            }, 'timerIsAlreadyPaused': {
                'en-US': u'It\u2019s already paused.',
                'zh-CN': u'您的计时器已暂停。',
                'fr-FR': u'Il est déjà en pause.'
            }, "timerIsAlreadyRunning": {
                "en-US": u"Your timer\u2019s already running:",
                'zh-CN': u'您的计时器已运行：',
                "fr-FR": u"Votre minuteur est déjà en marche :"
            }, 'timerIsAlreadyStopped': {
                'en-US': u'It\u2019s already stopped.',
                'zh-CN': u'您的计时器已停止。',
                'fr-FR': u'Votre minuteur est déjà arrêté.'
            }, 'timerWasPaused': {
                'en-US': u'It\u2019s paused.',
                'zh-CN': u'计时器暂停。',
                'fr-FR': u'Il est arrêté.'
            }, 'timerWasReset': {
                'en-US': u'I\u2019ve canceled the timer.',
                'zh-CN': u'我已经取消过了计时器。',
                'fr-FR': u'J\'ai remis à zéro le minuteur.'
            }, 'timerWasResumed': {
                'en-US': u'It\u2019s resumed.',
                'zh-CN': u'计时器继续。',
                'fr-FR': u'C\'est reparti.'
            }, "timerWasSet": {
                "en-US": "Your timer is set for {0}.",
                'zh-CN': u'您的计时器已设为{0}。',
                "fr-FR": "Votre minuteur est en marche pour {0}."
            }, "wontSetTimer": {
                "en-US": "OK.",
                'zh-CN': u'好的。',
                "fr-FR": "OK."
            }
        }
    }

    res = {
        'articles': {
            'en-US': 'a|an|the',
            'fr-FR': u'un|une|le',
        }, 'pauseTimer': {
            'en-US': '.*(pause|freeze|hold).*timer',
            'zh-CN': u'暂停.*计时.*',
            'fr-FR': u'.*(pause|pose|suspend|interromp).*minuteur'
        }, 'resetTimer': {
            'en-US': '.*(cancel|reset|stop).*timer',
            'zh-CN': u'(停止|取消).*计时.*',
            'fr-FR': u'.*(annule|reset|arret|arrêt|zero|zéro|stop).*minuteur'
        }, 'resumeTimer': {
            'en-US': '.*(resume|thaw|continue).*timer',
            'zh-CN': u'继续.*计时.*',
            'fr-FR': u'.*(reprend|continue|relance).*minuteur'
        }, 'setTimer': {
            #'fr-FR': u'.*minuteur.*\s+([0-9/ ]*|un|une|le|la|pour|sur)\s+(secs?|secondes?|mins?|minutes?|hrs?|heures?)'
            # 'en-US': '.*timer[^0-9]*(((([0-9/ ]*|a|an|the)\s+(seconds?|secs?|minutes?|mins?|hours?|hrs?))\s*(and)?)+)'
            'en-US': '.*timer[^0-9]*(?P<length>([0-9/ ]|seconds?|secs?|minutes?|mins?|hours?|hrs?|and|the|an|a){2,})',
            'zh-CN': u'(?u)^[^暂停止取消继续显示]*计时\s*((?P<h>[\w ]+)小时)?\s*((?P<m>[\w ]+)分)?钟?\s*((?P<s>[\w ]+)秒)?钟?',
            'fr-FR': '.*minuteur[^0-9]*(?P<length>([0-9/ ]|secondes?|secs?|minutes?|mins?|heures?|hrs?|et){2,})'
        }, 'showTimer': {
            'en-US': '.*(show|display|see).*timer',
            'zh-CN': u'显示.*计时.*',
            'fr-FR': u'.*(montre|affiche|voir).*minuteur'
        }, 'timerLength': {
            'en-US': '([0-9][0-9 /]*|an|a|the)\s+(seconds?|secs?|minutes?|mins?|hours?|hrs?)',
            'fr-FR': '([0-9][0-9 /]*|un|une|le|la|pour|sur)\s+(secs?|secondes?|mins?|minutes?|hrs?|heures?)',
        }
    }

    @register("en-US", res['setTimer']['en-US'])
    @register("zh-CN", res['setTimer']['zh-CN'])
    @register("fr-FR", res['setTimer']['fr-FR'])
    def setTimer(self, speech, language):
        m = re.match(timerPlugin.res['setTimer'][language], speech, re.IGNORECASE)
        timer_length = u""
        if language == 'zh-CN':
            ch_hour = toNum(m.group('h'))
            ch_min = toNum(m.group('m'))
            ch_sec = toNum(m.group('s'))
            if ch_hour != 0:
                timer_length += str(ch_hour) + u"小时"
            if ch_min != 0:
                timer_length += str(ch_min) + u"分钟"
            if ch_sec != 0:
                timer_length += str(ch_sec) + u"秒"
            duration = ch_hour * 3600 + ch_min * 60 + ch_sec
        else:
            timer_length = m.group('length')
            duration = parse_timer_length(timer_length, language)

        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [
            AssistantUtteranceView(
                speakableText=timerPlugin.localizations['Timer']['settingTimer'][language],
                dialogIdentifier="Timer#settingTimer")]
        self.sendRequestWithoutAnswer(view)

        # check the current state of the timer
        response = self.getResponseForRequest(TimerGet(self.refId))
        if response['class'] == 'CancelRequest':
            self.complete_request()
            return
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue=timer_properties['timerValue'],
                state=timer_properties['state'])

        if timer.state == "Running":
            # timer is already running!
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyRunning'][language], dialogIdentifier="Timer#timerIsAlreadyRunning")
            view2 = TimerSnippet(timers=[timer], confirm=True)
            view.views = [view1, view2]
            utterance = self.getResponseForRequest(view)
            #if response['class'] == 'StartRequest':
            view = AddViews(self.refId, dialogPhase="Reflection")
            view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['settingTimer'][language], dialogIdentifier="Timer#settingTimer")]
            self.sendRequestWithoutAnswer(view)

            if re.match('\^timerConfirmation\^=\^no\^', utterance):
                # user canceled
                view = AddViews(self.refId, dialogPhase="Completion")
                view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['wontSetTimer'][language], dialogIdentifier="Timer#wontSetTimer")]
                self.sendRequestWithoutAnswer(view)
                self.complete_request()
                return
            else:
                # user wants to set the timer still - continue on
                pass

        if duration > 24 * 60 * 60:
            view = AddViews(self.refId, dialogPhase='Clarification')
            view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['durationTooBig'][language], dialogIdentifier='Timer#durationTooBig')]
            self.sendRequestWithoutAnswer(view)
            self.complete_request()
            return

        # start a new timer
        timer = TimerObject(timerValue = duration, state = "Running")
        response = self.getResponseForRequest(TimerSet(self.refId, timer=timer))
        
        print(timerPlugin.localizations['Timer']['timerWasSet'][language].format(timer_length))
        view = AddViews(self.refId, dialogPhase="Completion")
        view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasSet'][language].format(timer_length), dialogIdentifier="Timer#timerWasSet")
        view2 = TimerSnippet(timers=[timer])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()

    @register("en-US", res['resetTimer']['en-US'])
    @register("zh-CN", res['resetTimer']['zh-CN'])
    @register("fr-FR", res['resetTimer']['fr-FR'])
    def resetTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        if timer.state == "Running" or timer.state == 'Paused':
            response = self.getResponseForRequest(TimerCancel(self.refId))
            if response['class'] == "CancelCompleted":
                view = AddViews(self.refId, dialogPhase="Completion")
                view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasReset'][language], dialogIdentifier="Timer#timerWasReset")]
                self.sendRequestWithoutAnswer(view)
            self.complete_request()
        else:
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()

    @register("en-US", res['resumeTimer']['en-US'])
    @register("zh-CN", res['resumeTimer']['zh-CN'])
    @register("fr-FR", res['resumeTimer']['fr-FR'])
    def resumeTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        if timer.state == "Paused":
            response = self.getResponseForRequest(TimerResume(self.refId))
            if response['class'] == "ResumeCompleted":
                view = AddViews(self.refId, dialogPhase="Completion")
                view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasResumed'][language], dialogIdentifier="Timer#timerWasResumed")
                view2 = TimerSnippet(timers=[timer])
                view.views = [view1, view2]
                self.sendRequestWithoutAnswer(view)
            self.complete_request()
        else:
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()

    @register("en-US", res['pauseTimer']['en-US'])
    @register("zh-CN", res['pauseTimer']['zh-CN'])
    @register("fr-FR", res['pauseTimer']['fr-FR'])
    def pauseTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        if timer.state == "Running":
            response = self.getResponseForRequest(TimerPause(self.refId))
            if response['class'] == "PauseCompleted":
                view = AddViews(self.refId, dialogPhase="Completion")
                view.views = [AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerWasPaused'][language], dialogIdentifier="Timer#timerWasPaused")]
                self.sendRequestWithoutAnswer(view)
            self.complete_request()
        elif timer.state == "Paused":
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyPaused'][language], dialogIdentifier="Timer#timerIsAlreadyPaused")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()
        else:
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['timerIsAlreadyStopped'][language], dialogIdentifier="Timer#timerIsAlreadyStopped")
            view2 = TimerSnippet(timers=[timer])
            view.views = [view1, view2]

            self.sendRequestWithoutAnswer(view)
            self.complete_request()

    @register("en-US", res['showTimer']['en-US'])
    @register("zh-CN", res['showTimer']['zh-CN'])
    @register("fr-FR", res['showTimer']['fr-FR'])
    def showTimer(self, speech, language):
        response = self.getResponseForRequest(TimerGet(self.refId))
        timer_properties = response['properties']['timer']['properties']
        timer = TimerObject(timerValue = timer_properties['timerValue'], state = timer_properties['state'])

        view = AddViews(self.refId, dialogPhase="Summary")
        view1 = AssistantUtteranceView(speakableText=timerPlugin.localizations['Timer']['showTheTimer'][language], dialogIdentifier="Timer#showTheTimer")
        view2 = TimerSnippet(timers=[timer])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()