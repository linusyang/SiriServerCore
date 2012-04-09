#!/usr/bin/python
# -*- coding: utf-8 -*-
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

from plugin import *
from siriObjects.baseObjects import ObjectIsCommand
from siriObjects.contactObjects import PersonSearch, PersonSearchCompleted
from siriObjects.phoneObjects import PhoneCall
from siriObjects.systemObjects import SendCommands, StartRequest, ResultCallback, \
    Person, PersonAttribute
from siriObjects.uiObjects import AddViews, DisambiguationList, ListItem, \
    AssistantUtteranceView

responses = {
'notFound': 
    {'de-DE': u"Entschuldigung, ich konnte niemanden in deinem Telefonbuch finden der so heißt",
     'zh-CN': u"抱歉，我在通讯录里找不到匹配。",
     'en-US': u"Sorry, I did not find a match in your phone book"
    },
'devel':
    {'de-DE': u"Entschuldigung, aber diese Funktion befindet sich noch in der Entwicklungsphase",
     'zh-CN': u"抱歉，此功能正在开发中。",
     'en-US': u"Sorry this feature is still under development"
    },
 'select':
    {'de-DE': u"Wen genau?",
     'zh-CN': u"哪一个？", 
     'en-US': u"Which one?"
    },
'selectNumber':
    {'de-DE': u"Welche Telefonnummer für {0}",
     'zh-CN': u"{0} 的哪个号码",
     'en-US': u"Which phone one for {0}"
    },
'callPersonSpeak':
    {'de-DE': u"Rufe {0}, {1} an.",
     'zh-CN': u"正在呼叫 {0}，{1}。",
     'en-US': u"Calling {0}, {1}."
    },
'callPerson': 
    {'de-DE': u"Rufe {0}, {1} an: {2}",
     'zh-CN': u"正在呼叫 {0}，{1}：{2}",
     'en-US': u"Calling {0}, {1}: {2}"
    }
}

numberTypesLocalized= {
'_$!<Mobile>!$_': {'en-US': u"mobile", 'de-DE': u"Handynummer", 'fr-FR': u"mobile", 'zh-CN': u"移动电话"},
'iPhone': {'en-US': u"iPhone", 'de-DE': u"iPhone-Nummer", 'fr-FR': u"iPhone", 'zh-CN': u"iPhone"},
'_$!<Home>!$_': {'en-US': u"home", 'de-DE': u"Privatnummer", 'fr-FR': u"domicile", 'zh-CN': u"住宅"},
'_$!<Work>!$_': {'en-US': u"work", 'de-DE': u"Geschäftsnummer", 'fr-FR': u"bureau", 'zh-CN': u"工作"},
'_$!<Main>!$_': {'en-US': u"main", 'de-DE': u"Hauptnummer",'fr-FR': u"principal",'zh-CN': u"主要"},
'_$!<HomeFAX>!$_': {'en-US': u"home fax", 'de-DE': u'private Faxnummer', 'fr-FR': u'fax domicile', 'zh-CN': u'住宅传真'},
'_$!<WorkFAX>!$_': {'en-US': u"work fax", 'de-DE': u"geschäftliche Faxnummer", 'fr-FR': u"fax bureau", 'zh-CN': u'工作传真'},
'_$!<OtherFAX>!$_': {'en-US': u"_$!<OtherFAX>!$_", 'de-DE': u"_$!<OtherFAX>!$_", 'fr-FR': u"_$!<OtherFAX>!$_", 'zh-CN': u"其他传真"},
'_$!<Pager>!$_': {'en-US': u"pager", 'de-DE': u"Pagernummer", 'fr-FR': u"biper", 'zh-CN': u"传呼"},
'_$!<Other>!$_':{'en-US': u"other phone", 'de-DE': u"anderes Telefon", 'fr-FR': u"autre", 'zh-CN': u"其他"}
}

namesToNumberTypes = {
'de-DE': {'mobile': "_$!<Mobile>!$_", 'handy': "_$!<Mobile>!$_", 'zuhause': "_$!<Home>!$_", 'privat': "_$!<Home>!$_", 'arbeit': "_$!<Work>!$_"},
'en-US': {'work': "_$!<Work>!$_",'home': "_$!<Home>!$_", 'mobile': "_$!<Mobile>!$_"}, 
'zh-CN': {u'工作': "_$!<Work>!$_", u'家庭': "_$!<Home>!$_", u'住宅': "_$!<Home>!$_", u'移动': "_$!<Mobile>!$_", u'手机': "_$!<Mobile>!$_", u'移动电话': "_$!<Mobile>!$_", u'主要': "_$!<Main>!$_", u'其他': "_$!<Other>!$_", u'住宅传真': "_$!<HomeFAX>!$_", u'工作传真': "_$!<WorkFAX>!$_", u'其他传真': "_$!<OtherFAX>!$_", u'传呼': "_$!<Pager>!$_"}
}

speakableDemitter={
'en-US': u", or ",
'zh-CN': u", 或 ",
'de-DE': u', oder '}

errorNumberTypes= {
'de-DE': u"Ich habe dich nicht verstanden, versuch es bitte noch einmal.",
'zh-CN': u"我没听懂，呼叫取消。",
'en-US': u"Sorry, I did not understand. Cancelled."
}

errorNumberNotPresent= {
'de-DE': u"Ich habe diese {0} von {1} nicht, aber eine andere.",
'zh-CN': u"抱歉，我找不到 {1} 类型为 {0} 的号码，但找到了其他类型的号码。",
'en-US': u"Sorry, I don't have a {0} number from {1}, but another."
}

errorOnCallResponse={'en-US':
                     [{'dialogIdentifier':u"PhoneCall#airplaneMode",
                       'text': u"Your phone is in airplane mode.",
                       'code': 1201},
                      {'dialogIdentifier': u"PhoneCall#networkUnavailable",
                       'text': u"Uh, I can't seem to find a good connection. Please try your phone call again when you have cellular access.",
                       'code': 1202},
                      {'dialogIdentifier': u"PhoneCall#invalidNumber",
                       'text': u"Sorry, I can't call this number.",
                       'code': 1203},
                      {'dialogIdentifier': u"PhoneCall#fatalResponse",
                       'text': u"Oh oh, I can't make your phone call.",
                       'code': -1}],
                     'zh-CN':
                     [{'dialogIdentifier':u"PhoneCall#airplaneMode",
                       'text': u"您的电话处于飞行模式。",
                       'code': 1201},
                      {'dialogIdentifier': u"PhoneCall#networkUnavailable",
                       'text': u"信号有点差。请在信号好的地方重试。",
                       'code': 1202},
                      {'dialogIdentifier': u"PhoneCall#invalidNumber",
                       'text': u"抱歉，我无法拨打这个号码。",
                       'code': 1203},
                      {'dialogIdentifier': u"PhoneCall#fatalResponse",
                       'text': u"哦，我无法拨号。",
                       'code': -1}],
                     'de-DE':
                     [{'dialogIdentifier':u"PhoneCall#airplaneMode",
                       'text': u"Dein Telefon ist im Flugmodus.",
                       'code': 1201},
                      {'dialogIdentifier': u"PhoneCall#networkUnavailable",
                       'text': u"Oh je! Ich kann im Moment keine gute Verbindung bekommen. Versuch es noch einmal, wenn du wieder Funkempfang hast.",
                       'code': 1202},
                      {'dialogIdentifier': u"PhoneCall#invalidNumber",
                       'text': u"Ich kann diese Nummer leider nicht anrufen.",
                       'code': 1203},
                      {'dialogIdentifier': u"PhoneCall#fatalResponse",
                       'text': u"Tut mir leid, Ich, ich kann momentan keine Anrufe t�tigen.",
                       'code': -1}]
}

class phonecallPlugin(Plugin):

    def searchUserByName(self, personToLookup):
        namelen = len(personToLookup)
        while namelen > 0:
            search = PersonSearch(self.refId)
            search.scope = PersonSearch.ScopeLocalValue
            search.name = personToLookup[0:namelen]
            answerObj = self.getResponseForRequest(search)
            if ObjectIsCommand(answerObj, PersonSearchCompleted):
                answer = PersonSearchCompleted(answerObj)
            else:
                raise StopPluginExecution("Unknown response: {0}".format(answerObj))
            if answer.results != None:
                break
            namelen = namelen - 1
        return answer.results if answer.results != None else []
           
    def getNumberTypeForName(self, name, language):
        # q&d
        if name != None:
            if name.lower() in namesToNumberTypes[language]:
                return namesToNumberTypes[language][name.lower()]
            else:
                for key in numberTypesLocalized.keys():
                    if numberTypesLocalized[key][language].lower() == name.lower():
                        return numberTypesLocalized[key][language]
        return name
    
    def findPhoneForNumberType(self, person, numberType, language):         
        # first check if a specific number was already requested
        phoneToCall = None
        if numberType != None:
            # try to find the phone that fits the numberType
            listToCall = filter(lambda x: x.label == numberType, person.phones)
            if len(listToCall) == 1:
                phoneToCall = listToCall[0]
        else:
            favPhones = filter(lambda y: y.favoriteVoice if hasattr(y, "favoriteVoice") else False, person.phones)
            if len(favPhones) == 1:
                phoneToCall = favPhones[0]
        if phoneToCall == None:
            # lets check if there is more than one number
            if len(person.phones) == 1:
                if numberType != None:
                    self.say(errorNumberNotPresent[language].format(numberTypesLocalized[numberType][language], person.fullName))
                phoneToCall = person.phones[0]
            else:
                # damn we need to ask the user which one he wants...
                if phoneToCall == None:
                    rootView = AddViews(self.refId, temporary=False, dialogPhase="Clarification", scrollToTop=False, views=[])
                    sayit = responses['selectNumber'][language].format(person.fullName)
                    rootView.views.append(AssistantUtteranceView(text=sayit, speakableText=sayit, listenAfterSpeaking=True,dialogIdentifier="ContactDataResolutionDucs#foundAmbiguousPhoneNumberForContact"))
                    lst = DisambiguationList(items=[], speakableSelectionResponse="", listenAfterSpeaking=True, speakableText="", speakableFinalDemitter=speakableDemitter[language], speakableDemitter=", ",selectionResponse="")
                    rootView.views.append(lst)
                    for phone in person.phones:
                        numberType = numberTypesLocalized[phone.label][language] if phone.label in numberTypesLocalized else phone.label
                        item = ListItem()
                        item.title = ""
                        item.text = u"{0}: {1}".format(numberType, phone.number)
                        item.selectionText = item.text
                        item.speakableText = u"{0}, ".format(numberType)
                        item.object = phone
                        item.commands.append(SendCommands(commands=[StartRequest(handsFree=False, utterance=numberType)]))
                        lst.items.append(item)
                    answer = self.getResponseForRequest(rootView)
                    numberType = self.getNumberTypeForName(answer, language)
                    if numberType != None:
                        matches = filter(lambda x: x.label == numberType, person.phones)
                        if len(matches) == 1:
                            phoneToCall = matches[0]
                        else:
                            self.say(errorNumberTypes[language])
                    else:
                        self.say(errorNumberTypes[language])
        return phoneToCall
             
    
    def call(self, phone, person, language):
        root = ResultCallback(commands=[])
        rootView = AddViews("", temporary=False, dialogPhase="Completion", views=[])
        root.commands.append(rootView)
        if phone.label != None:
            numberType = numberTypesLocalized[phone.label][language] if phone.label in numberTypesLocalized else phone.label
        else:
            numberType = ""
        rootView.views.append(AssistantUtteranceView(text=responses['callPerson'][language].format(person.fullName, numberType, phone.number), speakableText=responses['callPersonSpeak'][language].format(person.fullName, numberType), dialogIdentifier="PhoneCall#initiatePhoneCall", listenAfterSpeaking=False))
        rootView.callbacks = []
        
        # create some infos of the target
        personAttribute=PersonAttribute(data=phone.number, displayText=person.fullName, obj=Person())
        personAttribute.object.identifer = person.identifier
        call = PhoneCall("", recipient=phone.number, faceTime=False, callRecipient=personAttribute)
        
        rootView.callbacks.append(ResultCallback(commands=[call]))
        
        call.callbacks = []
        # now fill in error messages (airplanemode, no service, invalidNumber, fatal)
        for i in range(4):
            errorRoot = AddViews(None, temporary=False, dialogPhase="Completion", scrollToTop=False, views=[])
            errorRoot.views.append(AssistantUtteranceView(text=errorOnCallResponse[language][i]['text'], speakableText=errorOnCallResponse[language][i]['text'], dialogIdentifier=errorOnCallResponse[language][i]['dialogIdentifier'], listenAfterSpeaking=False))
            call.callbacks.append(ResultCallback(commands=[errorRoot], code=errorOnCallResponse[language][i]['code']))
            
        self.complete_request([root])

    def presentPossibleUsers(self, persons, language):
        root = AddViews(self.refId, False, False, "Clarification", [], [])
        root.views.append(AssistantUtteranceView(responses['select'][language], responses['select'][language], "ContactDataResolutionDucs#disambiguateContact", True))
        lst = DisambiguationList([], "", True, "", speakableDemitter[language], ", ", "")
        root.views.append(lst)
        for person in persons:
            item = ListItem(person.fullName, person.fullName, [], u"{0}, ".format(person.fullName), person)
            item.commands.append(SendCommands([StartRequest(False, "^phoneCallContactId^=^urn:ace:{0}".format(person.identifier))]))
            lst.items.append(item)
        return root
    
    @register("de-DE", "ruf. (?P<name>[\w ]+?)( (?P<type>arbeit|zuhause|privat|mobil|handy.*|iPhone.*|pager))? an$")
    @register("en-US", "(make a )?call (to )?(?P<name>[\w ]+?)( (?P<type>work|home|mobile|main|iPhone|pager))?$")
    @register("zh-CN", u".*(呼叫|电话|拨号|打)给?(((?P<name>[\w ]+)类型为?(?P<type>工作|家庭|住宅|移动|手机)?)|(?P<name2>[\w ]+))")
    def makeCall(self, speech, language, regex):
        personToCall = regex.group('name')
        if (language == "zh-CN") and (personToCall == None):
            personToCall = regex.group('name2')
        numberType = str.lower(regex.group('type')) if type in regex.groupdict() else None
        numberType = self.getNumberTypeForName(numberType, language)
        persons = self.searchUserByName(personToCall)
        personToCall = None
        if len(persons) > 0:
            if len(persons) == 1:
                personToCall = persons[0]
            else:
                identifierRegex = re.compile("\^phoneCallContactId\^=\^urn:ace:(?P<identifier>.*)")
                #  multiple users, ask user to select
                if personToCall == None:
                    strUserToCall = self.getResponseForRequest(self.presentPossibleUsers(persons, language))
                    self.logger.debug(strUserToCall)
                    # maybe the user clicked...
                    identifier = identifierRegex.match(strUserToCall)
                    if identifier:
                        strUserToCall = identifier.group('identifier')
                        self.logger.debug(strUserToCall)
                    for person in persons:
                        if person.fullName == strUserToCall or person.identifier == strUserToCall:
                            personToCall = person
                    if personToCall == None:
                        # we obviously did not understand him.. but probably he refined his request... call again...
                        self.say(errorNumberTypes[language])
                    
            if personToCall != None:
                numberType = self.findPhoneForNumberType(personToCall, numberType, language)
                if numberType != None:
                    self.call(numberType, personToCall, language)
                    return # complete_request is done there
        self.say(responses['notFound'][language])                         
        self.complete_request()
    