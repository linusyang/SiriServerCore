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
            u'bulgarian': 'bg',
            u'catalan': 'ca',
            u'chinese': 'zh-CHS',
            u'simplified chinese': 'zh-CHS',
            u'traditional chinese': 'zh-CHT',
            u'czech': 'cs',
            u'danish': 'da',
            u'dutch': 'nl',
            u'english': 'en',
            u'estonian': 'et',
            u'finnish': 'fi',
            u'french': 'fr',
            u'german': 'de',
            u'greek': 'el',
            u'haitian creole': 'ht',
            u'hebrew': 'he',
            u'hindi': 'hi',
            u'hungarian': 'hu',
            u'indonesian': 'id',
            u'italian': 'it',
            u'japanese': 'ja',
            u'korean': 'ko',
            u'latvian': 'lv',
            u'lithuanian': 'lt',
            u'norwegian': 'no',
            u'polish': 'pl',
            u'portuguese': 'pt',
            u'romanian': 'ro',
            u'russian': 'ru',
            u'slovak': 'sk',
            u'slovenian': 'sl',
            u'spanish': 'es',
            u'swedish': 'sv',
            u'thai': 'th',
            u'turkish': 'tr',
            u'ukrainian': 'uk',
            u'vietnamese': 'vi'
        },
        'zh-CN': {
            u'阿拉伯': 'ar',
            u'保加利亚': 'bg',
            u'加泰隆': 'ca',
            u'中': 'zh-CHS',
            u'汉': 'zh-CHS',
            u'简体中': 'zh-CHS',
            u'繁体中': 'zh-CHT',
            u'捷克': 'cs',
            u'丹麦': 'da',
            u'荷兰': 'nl',
            u'英': 'en',
            u'爱沙尼亚': 'et',
            u'芬兰': 'fi',
            u'法': 'fr',
            u'德': 'de',
            u'希腊': 'el',
            u'海地克里奥尔': 'ht',
            u'希伯来': 'he',
            u'印地': 'hi',
            u'匈牙利': 'hu',
            u'印度尼西亚': 'id',
            u'印尼': 'id',
            u'意大利': 'it',
            u'日本': 'ja',
            u'日': 'ja',
            u'朝鲜': 'ko',
            u'韩': 'ko',
            u'拉脱维亚': 'lv',
            u'立陶宛': 'lt',
            u'挪威': 'no',
            u'波兰': 'pl',
            u'葡萄牙': 'pt',
            u'罗马尼亚': 'ro',
            u'俄': 'ru',
            u'斯洛伐克': 'sk',
            u'斯洛文尼亚': 'sl',
            u'西班牙': 'es',
            u'瑞典': 'sv',
            u'泰': 'th',
            u'土耳其': 'tr',
            u'乌克兰': 'uk',
            u'越南': 'vi'
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
