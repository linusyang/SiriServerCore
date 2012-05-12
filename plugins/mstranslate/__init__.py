#!/usr/bin/python
# -*- coding: utf-8 -*-
#Microsoft Translator Plugin
#Author: Linus Yang <laokongzi@gmail.com>

from plugin import *
import urllib, codecs, json
import xml.etree.ElementTree as etree

clientid = APIKeyForAPI("bing_clientid")
clientsec = APIKeyForAPI("bing_clientsecret")

res = {
    'command': {
        'en-US': u'Translate (?P<transword1>[^^]+) from (?P<fromlang1>[\w ]+) to (?P<tolang1>[\w ]+)|Translate (?P<transword2>[^^]+) to (?P<tolang2>[\w ]+)',
        'zh-CN': u'请?翻译(?P<fromlang1>[^语文]+)(语|文)的?(?P<transword1>[^^]+)(成|为|到)(?P<tolang1>[^语文]+)(语|文)|请?(把|将)?(?P<fromlang2>[^语文]+)(语|文)的?(?P<transword2>[^^]+)翻译(成|为|到)(?P<tolang2>[^语文]+)(语|文)|请?(把|将)?(?P<transword3>[^^]+)翻译(成|为|到)(?P<tolang3>[^语文]+)(语|文)',
        'de-DE': u'(Übersetze|Übersetzer|Übersetzen|Translate) (?P<transword>[^^]+) von (?P<fromlang>[\w]+) (nach|in|zu) (?P<tolang>[\w]+)'
    },
    'answer': {
        'en-US': u'Here is your {0} translation for {1}:\n',
        'zh-CN': u'“{1}”的{0}文\n',
        'de-DE': u'Hier ist deine {0} Übersetzung für {1}:\n'
    },
    'languageCodes': {
        'en-US': {
            u'arabic': 'ar',
        },
        'zh-CN': {
            u'阿拉伯': 'ar',
        },
        'de-DE': {
            u'englisch': 'en',
            u'spanisch': 'sp',
            u'französisch': 'fr',
            u'italienisch': 'it',
            u'finnisch': 'fi',
            u'griechisch': 'el',
            u'arabisch': 'ar',
            u'tschechisch': 'cs',
            u'holländisch': 'nl',
            u'hebräisch': 'he',
            u'russisch': 'ru',
            u'polnisch': 'pl',
            u'portugisisch': 'pt',
            u'rumänisch': 'ro',
            u'schwedisch': 'sv',
            u'türkisch': 'tr',
            u'indonesisch': 'id',
            u'ungarisch': 'id',
            u'deutsch': 'de'
        }
    },
    'errors': {
        'en-US': u'I\'m sorry, {0} is not a known language',
        'zh-CN': u'抱歉，暂不支持{0}文。',
        'de-DE': u'Tut mir leid, {0} ist keine Unterstütze Sprache'
    },
    'connerrors': {
        'en-US': u'Sorry. I can\'t connect to Microsoft Translator.',
        'zh-CN': u'抱歉，我无法连接到微软翻译服务。',
        'de-DE': u'Error.'
    }
}

def _unicode_urlencode(params):
    if isinstance(params, dict):
        params = params.items()
    return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])    

def translate(text, source, target, html=False):
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': clientid,
        'client_secret': clientsec,
        'scope': 'http://api.microsofttranslator.com'
    }
    get_token = urllib.urlopen(
        url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13',
        data = urllib.urlencode(token_data)
        ).read()
    token = None
    if get_token is not None:
        try:
            token = json.loads(get_token)['access_token']
        except:
            pass
    if token is None:
        return None
    query_args = {
        'appId': 'Bearer ' + token,
        'text': text,
        'to': target,
        'contentType': 'text/plain' if not html else 'text/html',
        'category': 'general'
    }
    if source is not None:
        query_args['from'] = source
    result = urllib.urlopen('http://api.microsofttranslator.com/V2/Http.svc/Translate?' + _unicode_urlencode(query_args)).read()
    if result.startswith(codecs.BOM_UTF8):
        result = result.lstrip(codecs.BOM_UTF8).decode('utf-8')
    elif result.startswith(codecs.BOM_UTF16_LE):
        result = result.lstrip(codecs.BOM_UTF16_LE).decode('utf-16-le')
    elif result.startswith(codecs.BOM_UTF16_BE):
        result = result.lstrip(codecs.BOM_UTF16_BE).decode('utf-16-be')
    answer = etree.fromstring(result)
    if answer is not None:
        return answer.text
    return None

class ms_translate(Plugin):
    @register("en-US", res['command']['en-US'])
    @register("de-DE", res['command']['de-DE'])
    @register("zh-CN", res['command']['zh-CN'])
    def snx_translate(self, speech, language, matchedRegex):
        if language == 'en-US':
            text = matchedRegex.group('transword1')
            if text != None:
                longlang1 = matchedRegex.group('fromlang1').lower()
                longlang2 = matchedRegex.group('tolang1').lower()
            else:
                text = matchedRegex.group('transword2')
                longlang1 = None
                longlang2 = matchedRegex.group('tolang2').lower()
        elif language == 'zh-CN':
            text = matchedRegex.group('transword1')
            if text != None:
                longlang1 = matchedRegex.group('fromlang1')
                longlang2 = matchedRegex.group('tolang1')
            else:
                text = matchedRegex.group('transword2')
                if text != None:
                    longlang1 = matchedRegex.group('fromlang2')
                    longlang2 = matchedRegex.group('tolang2')
                else:
                    text = matchedRegex.group('transword3')
                    longlang1 = None
                    longlang2 = matchedRegex.group('tolang3')
        else:
            text = matchedRegex.group('transword')
            longlang1 = matchedRegex.group('fromlang').lower()
            longlang2 = matchedRegex.group('tolang').lower()
        if longlang1 != None:
            try:
                lang1 = res['languageCodes'][language][longlang1]
            except:
                pass
        else:
            lang1 = None
        lang2 = None
        try:
            lang2 = res['languageCodes'][language][longlang2]
        except:
            self.say(res['errors'][language].format(longlang2))
        if lang2 != None:
            translation = translate(text, lang1, lang2)
            if translation is None:
                self.say(res['connerrors'][language])
            else:
                if longlang2 is not None:
                    self.say(res['answer'][language].format(longlang2, text))
                self.say(translation)
        self.complete_request()