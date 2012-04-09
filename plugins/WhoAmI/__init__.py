#!/usr/bin/python
# -*- coding: utf-8 -*-
# Code by Javik
# Update by @FreeManRepo
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

import re
import uuid

from plugin import *

from siriObjects.baseObjects import *
from siriObjects.uiObjects import *
from siriObjects.systemObjects import *
from siriObjects.contactObjects import *

class meCard(Plugin):
	
	@register("en-US", "(Who am I.*)|(What's my name.*)")
	@register("zh-CN", u".*我(的名字|叫|的姓名|是谁|是哪).*")
	def mePerson(self, speech, language):
		
		if language == 'zh-CN':
			self.say(u"您叫{0}，至少这是您告诉我的。".format(self.user_name()))
		else:
			self.say("You're {0}, that's what you told me. anyway.".format(self.user_name()))		
		
		person_search = PersonSearch(self.refId)
		person_search.scope = PersonSearch.ScopeLocalValue
		person_search.me = "true"        
		person_return = self.getResponseForRequest(person_search)
		person_ = person_return["properties"]["results"]
		mecard = PersonSnippet(persons=person_)
		view = AddViews(self.refId, dialogPhase="Completion")		
		view.views = [mecard]
		self.sendRequestWithoutAnswer(view)
		self.complete_request()