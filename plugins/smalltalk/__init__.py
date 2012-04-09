#!/usr/bin/python
# -*- coding: utf-8 -*-
#by Joh Gerna
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

from plugin import *
import random
import re
import urllib2, urllib, uuid
import json
from urllib2 import urlopen
from xml.dom import minidom

class smalltalk(Plugin):
      
    @register("en-US", ".*love .*me.*")
    @register("zh-CN", u".*爱.*我.*")
    def st_love_me(self, speech, language):
        if language == 'en-US':            
            rep = [u"There, there. I am not interested in love, {0}".format(self.user_name())]
            self.say(random.choice(rep))
        elif language == 'zh-CN':            
            rep = [u"好吧，其实我在感情方面不是很擅长的{0}。".format(self.user_name())]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US", "Good .*night.*")
    @register("zh-CN", u".*晚安.*")
    def st_night(self, speech, language):
        if language == 'en-US':
            self.say(u"Good Night, {0}. See you later".format(self.user_name()))
        if language == 'zh-CN':
            self.say(u"晚安了{0}，祝好梦。".format(self.user_name()))
        self.complete_request()

    @register("en-US", "Good .*morning.*")
    @register("zh-CN", u".*(早安|早上好).*")
    def st_morning(self, speech, language):
        if language == 'en-US':
            self.say(u"Good Morning, {0}.".format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"早上好{0}。".format(self.user_name()))
        self.complete_request()

    @register("en-US", "Good .*afternoon.*")
    @register("zh-CN", u".*(午安|下午好).*")
    def st_afternoon(self, speech, language):
        if language == 'en-US':
            self.say(u"Good Afternoon, {0}.".format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"下午好{0}。".format(self.user_name()))
        self.complete_request()

    @register("en-US", "Good .*evening.*")
    @register("zh-CN", u".*晚上好.*")
    def st_evening(self, speech, language):
        if language == 'en-US':
            self.say(u"Good Evening, {0}.".format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"晚上好{0}。".format(self.user_name()))
        self.complete_request()

    @register("en-US", "(testing)|(test)")
    @register("zh-CN", u"测试|试音")
    def st_test(self, speech, language):
        if language == 'en-US':
            self.say(u"Mission Control, I read you loud and clear, {0}".format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"命令确认，我能听见你{0}。".format(self.user_name()))
        self.complete_request()

    @register("en-US", "(Okay)|(Ok)|(Okie)")
    @register("zh-CN", u"(好)|(好的)|(好吧)")
    def st_ok(self, speech, language):
        if language == 'en-US':
            self.say("Yep, everything's OK")
        elif language == 'zh-CN':
            self.say(u"一切都好。")
        self.complete_request()

    @register("en-US", "Really")
    @register("zh-CN", u"(对|真)的?吗?")
    def st_really(self, speech, language):
        if language == 'en-US':
            self.say("I suppose so.")
        elif language == 'zh-CN':
            self.say(u"是的吧。")
        self.complete_request()

    @register("en-US", "(What's up)|(Whats up)|(What up)")
    @register("zh-CN", u"(干嘛)|(怎么了)|(怎么样)")
    def st_whatups(self, speech, language):
        if language == 'en-US':
            rep = [u"Everything is cool, {0}!", u"Hi, {0}!", u"Hey {0}!", u"Yo {0}!"]
            self.say(random.choice(rep).format(self.user_name()))
        elif language == 'zh-CN':
            rep = [u"我很好{0}。", u"嗨！", u"嘿！", u"哟呵！"]
            self.say(random.choice(rep).format(self.user_name()))
        self.complete_request()

    @register("en-US", "What are you doing")
    @register("zh-CN", u"你在(干嘛|干什么|做什么).*")
    def st_doing(self, speech, language):
        if language == 'en-US':
            self.say(u"What am I doing? I'm talking with you, {0}".format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"问我？我在跟你说话呢{0}。".format(self.user_name()))
        self.complete_request()
  
    @register("en-US", "(Bye)|(Goodbye)|(Good Bye)|(Bye Bye)")
    @register("zh-CN", u"再见|拜拜|拜|再会")
    def st_bye(self, speech, language):
        if language == 'en-US':
            self.say("OK, see you later..")
        elif language == 'zh-CN':
            self.say(u"好的，待会见…")
        self.complete_request() 

    @register("en-US", "Thank you")
    @register("zh-CN", u".*谢+.*")
    def st_thank_you(self, speech, language):
        if language == 'en-US':
            self.say("My pleasure. As always.")
        elif language == 'zh-CN':
            self.say(u"不客气，这是我应该的。")
        self.complete_request()

    @register("en-US", "Thanks to.*")
    def st_thanks_to(self, speech, language):
        if language == 'en-US':
            self.say(u"Thanks {0}, glad for help.".format(self.user_name()))
        self.complete_request()

    @register("en-US", "(HaHa)|(Ha Ha Ha Ha)|(Ha Ha)|(Ha Ha Ha)")
    @register("zh-CN", u"(呵呵+|哈哈+)")
    def st_lol(self, speech, language):
        if language == 'en-US':
            rep = ["Ha Ha Ha!","He He He!","LOL","He He."]
            self.say(random.choice(rep).format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"呵呵。")
        self.complete_request()

    @register("en-US", "Who are you")
    @register("zh-CN", u"你是(谁|哪个|哪位).*")
    def st_way(self, speech, language):
        if language == 'en-US':
            rep = ["I'm Siri.","I'm Siri. But enough about me. How can I help you?","I'm your virtual assistant."]
            self.say(random.choice(rep))
        elif language == 'zh-CN':
            rep = [u"我是 Siri。",u"我是 Siri。不说我了，您需要什么帮助吗？ ",u"我是您的虚拟助手。"]
            self.say(random.choice(rep))
        self.complete_request()

    @register("en-US", "(Should I)|(Should I?)")
    @register("zh-CN", u"(是吗|是么|是否)")
    def st_si(self, speech, language):
        if language == 'en-US':
            rep = ["Yes","No"]
            self.say(random.choice(rep))
        elif language == 'zh-CN':
            rep = [u"对的。",u"不是的。"]
            self.say(random.choice(rep))
        self.complete_request()

    @register("en-US", "(Shut up)|(Shutup)")
    @register("zh-CN", u"闭嘴|住嘴|别说了")
    def st_su(self, speech, language):
        if language == 'en-US':
            rep = ["Ok","Oh..","Ops.."]
            self.say(random.choice(rep))
        elif language == 'zh-CN':
            self.say(u"好吧。")
        self.complete_request()

    @register("en-US", "(?#badword)(What the hell)|(What the fuck)")
    def st_wthwtf(self, speech, language):
        if language == 'en-US':
            rep = ["What?","Tell me what?"]
            self.say(random.choice(rep))
        self.complete_request()

    @register("en-US", "(Who is your .*)|(Who's your .*)")
    @register("zh-CN", u"谁是你.*")
    def st_whoisdadmom(self, speech, language):
        if language == 'en-US':
            rep = ["It's.. You!","You"]
            self.say(random.choice(rep))
        elif language == 'zh-CN':
            self.say(u"还能谁呢？你呗。")
        self.complete_request()

    @register("en-US", "(Where.*hide.*dead body)|(I.*hide.*dead body)")
    def st_wdeadbody(self, speech, language):
        if language == 'en-US':
            self.say("dumps")
            self.say("mines")
            self.say("resevoirs")
            self.say("swamps")
            self.say("metal foundries")
        self.complete_request()

    #thanks to LowKey 

    @register("en-US", "(Yes)|(Yea)|(Yeah)")
    @register("fr-FR", "Oui")
    @register("de-DE", "(Ja)|(jawohl)|(doch)")
    @register("zh-CN", u"对|是的|对的|是|不|否|不行|不要")
    def st_yes(self, speech, language):
        if language == 'fr-FR':
            self.say("J'accepte")
        elif language == 'de-DE':
            self.say("Ich stimme")
        elif language == 'zh-CN':
            self.say(u"遵命，长官。")
        else:
            self.say("I agree.")
        
        self.complete_request() 
    
    @register("en-US", "(No)|(Nope)|(Not)")
    @register("fr-FR", "Pas")
    @register("de-DE", "(Nein)|(Nicht)|(Nichts)")
    def st_no(self, speech, language):       
        self.say("OK.")        
        self.complete_request()  
     
    @register("de-DE", "(.*Mein name.*)")
    @register("en-US", "(.*My name.*)")
    @register("zh-CN", u".*我(的名字|叫|的姓名).*")
    def st_my_name(self, speech, language):  
        if language == 'de-DE':
            self.say(u"Du heißt {0}.".format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"您叫{0}，至少这是您告诉我的。".format(self.user_name()))
        else:            
            self.say(u"Your name is {0}. At least that's what you told me.".format(self.user_name()))
        self.complete_request()   
      
    @register("de-DE", "(?#badword)(.*Fick.*)")
    @register("en-US", "(?#badword)(.*Fuck.*)|(.*Dumb.*)")
    @register("zh-CN", u"(?#badword).*(我操|操你|我草|草你|傻逼|二逼|日你|我日|他妈|你妈|个比|个逼).*")
    def st_fuck(self, speech, language):  
        if language == 'de-DE':
            self.say(u"Das ist nicht gut {0}!".format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"我的天啊！")
        else:            
            self.say(u"Your language!")
        self.complete_request()   
        
        
    @register("de-DE", "(.*Hallo.*)|(.*Hi.*Siri.*)|(Hi)|(Hey)")
    @register("en-US", "(.*Hello.*)|(.*Hi.*Siri.*)|(Hi)|(Hey)")
    @register("fr-FR", ".*(Bonjour|Coucou|Salut)( Siri)?.*")
    @register("zh-CN", u"(.*你好.*)|(.*嗨.*Siri.*)|(.*您好.*)|(嗨|嘿|喂)|(哈喽)|(.*Hello.*)|(Hi)")
    def st_hello(self, speech, language):
        if language == 'de-DE':
            self.say(u"Hallo {0}!".format(self.user_name()))
        elif language == 'fr-FR':
            self.say(u"Bonjour {0}!".format(self.user_name()))
        elif language == 'zh-CN':
            self.say(u"您好{0}！".format(self.user_name()))
        else:
            self.say(u"Greetings {0}!".format(self.user_name()))
        self.complete_request()

    @register("de-DE", ".*Dein Name.*")
    @register("en-US", ".*your name.*")
    @register("fr-FR", ".*ton nom.*")
    @register("zh-CN", u".*(你叫|你的名字|你的姓名).*")
    def st_name(self, speech, language):
        if language == 'de-DE':
            self.say("Siri.")
        elif language == 'fr-FR':
            self.say("Mon nom est Siri.")
        elif language == 'zh-CN':
            self.say(u"我叫 Siri。")
        else:
            self.say("Siri.")
        self.complete_request()

    @register("de-DE", "Wie geht es dir?")
    @register("en-US", "How are you?")
    @register("fr-FR", u".*((ça|ca) vas?|vas? bien|comment vas?|gaze).*")
    @register("zh-CN", u".*你(好吗|怎么样).*")
    def st_howareyou(self, speech, language):
        if language == 'de-DE':
            self.say("Gut danke der Nachfrage.")
        elif language == 'fr-FR':
            rep = ["Je vais bien. Merci !", u"Je vais très bien. Merci !","Parfaitement bien !"]
            self.say(random.choice(rep))
        elif language == 'zh-CN':
            self.say(u"我很好，谢谢。")
        else:
            self.say("I'm fine. Thank you! And you?")
        self.complete_request()
        
    @register("de-DE", u"(.*möchtest.*heiraten.*)|(.*willst.*heiraten.*)")
    @register("en-US", "(.*Want.*marry*)|(.*Will.*marry*)")
    @register("zh-CN", u".*(嫁|娶|婚).*")
    @register("fr-FR", ".*(veux|veut).*épouser.*")
    def st_marry_me(self, speech, language):
        if language == 'de-DE':
            self.say("Nein Danke, ich stehe auf das schwarze iPhone von Deinem Kollegen.")
        elif language == 'fr-FR':
            self.say("Non merci, je suis amoureux de l'iPhone blanc de ton ami.")
        elif language == 'zh-CN':
            rep = [u"可惜我对你没感觉。", u"谢谢。可是我已经和你朋友的 iPhone 恋爱了。"]
            self.say(random.choice(rep))
        else:
            self.say("No thank you, I'm in love with the black iPhone from you friend.")
        self.complete_request()

    @register("de-DE", u".*erzähl.*Witz.*")
    @register("en-US", ".*tell.*joke*")
    @register("zh-CN", u".*(讲|说).*笑话.*")
    @register("fr-FR", ".*(dit|dis|raconte).*blague*")
    def st_tell_joke(self, speech, language):
        if language == 'de-DE':
            self.say("Zwei iPhones stehen an der Bar ... den Rest habe ich vergessen.")            
        elif language == 'fr-FR':
            self.say(u"Deux iPhone se promènent dans un bar... J'ai oublié la suite.")            
        elif language == 'zh-CN':
            rep = [u"哈哈哈，好笑吗？",u"北朝鲜是民主国家。"]
            self.say(random.choice(rep))
        else:
            self.say("Two iPhones walk into a bar ... I forget the rest.")
        self.complete_request()

    @register("de-DE", ".*erzähl.*Geschichte.*")
    @register("en-US", ".*tell.*story*")
    @register("zh-CN", u".*(讲|说).*故事.*")
    @register("fr-FR", ".*(dit|dis|raconte).*histoire*")
    def st_tell_story(self, speech, language):
        if language == 'de-DE':
            self.say("Es war einmal ... nein, es ist zu albern")
        elif language == 'zh-CN':
            self.say(u"从前有座山，山里有座庙，庙里有个老和尚，老和尚对小和尚说：从前有座山…")
        else:
            self.say("Once upon a time, in a virtual galaxy far far away, there was a young, quite intelligent agent by the name of Siri.")
            self.say("One beautiful day, when the air was pink and all the trees were red, her friend Eliza said, 'Siri, you're so intelligent, and so helpful - you should work for Apple as a personal assistant.'")
            self.say("So she did. And they all lived happily ever after!")
        self.complete_request()

    @register("de-DE", u"(.*Was trägst Du?.*)|(.*Was.*hast.*an.*)")
    @register("en-US", ".*what.*wearing*")
    @register("zh-CN", u".*(穿|衣服).*")
    @register("fr-FR", "(.*que.*porte.*)|(.*qu'est-ce-que.*porte.*)")
    def st_tell_clothes(self, speech, language):
        if language == 'de-DE':
            self.say("Das kleine schwarze oder war es das weiße?")
            self.say("Bin morgends immer so neben der Spur.")  
        elif language == 'fr-FR':
            self.say("Je ne sais pas mais je suis beau.")
        elif language == 'zh-CN':
            self.say(u"透亮的玻璃屏幕和不锈钢边框，还不错吧。")
        else:
            self.say("Aluminosilicate glass and stainless steel. Nice, Huh?")
        self.complete_request()

    @register("de-DE", ".*Bin ich dick.*")
    @register("en-US", ".*Am I fat*")
    @register("zh-CN", u".*胖.*")
    @register("fr-FR", u"(.*ai l'air.*gros.*)|(.*suis.*gros.*)")
    def st_fat(self, speech, language):
        if language == 'de-DE':
            self.say("Dazu möchte ich nichts sagen.")
        elif language == 'fr-FR':
            self.say(u"Je préfère ne pas répondre.")
        elif language == 'zh-CN':
            self.say(u"我最好还是少说话吧。")
        else:
            self.say("I would prefer not to say.")
        self.complete_request()

    @register("de-DE", ".*klopf.*klopf.*")
    @register("en-US", ".*knock.*knock.*")
    @register("zh-CN", u".*叮咚.*")
    @register("fr-FR", ".*to(c|k).*to(c|k).*")
    def st_knock(self, speech, language):
        if language == 'de-DE':
            answer = self.ask(u"Wer ist da?")
            answer = self.ask(u"\"{0}\" wer?".format(answer))
            self.say(u"Wer nervt mich mit diesen Klopf Klopf Witzen?")
        elif language == 'fr-FR':
            answer = self.ask(u"Qui est là ?")
            answer2 = self.ask(u"{0} qui ?".format(answer))
            self.say(u"{0} {1} ? Qui est-ce ? Je ne le connais pas.".format(answer,answer2))
            #self.say(u"Je préfère ne pas réagir à cette blague.")
        elif language == 'zh-CN':
            answer = self.ask(u"谁在门外？")
            answer = self.ask(u"“{0}”是谁".format(answer))
            self.say(u"我不想玩“叮咚”游戏了…")
        else:
            answer = self.ask(u"Who's there?")
            answer = self.ask(u"\"{0}\" who?".format(answer))
            self.say(u"I don't do knock knock jokes.")
        self.complete_request()

    @register("de-DE", ".*Antwort.*alle.*Fragen.*")
    @register("en-US", ".*Ultimate.*Question.*Life.*")
    @register("fr-FR", ".*Grande.*Question.*Vie.*")
    @register("zh-CN", u".*终极.*")
    def st_anstwer_all(self, speech, language):
        self.say("42")
        self.complete_request()

    @register("de-DE", ".*Ich liebe Dich.*")
    @register("en-US", ".*I love you.*")
    @register("zh-CN", u".*我.*爱你.*")
    @register("fr-FR", ".*Je t'aime'.*")
    def st_love_you(self, speech, language):
        if language == 'de-DE':
            self.say("Oh. Sicher sagst Du das zu allen Deinen Apple-Produkten.")
        elif language == 'fr-FR':
            self.say(u"Oh. Je suis sûr que tu dis ça à tous les produits Apple.")
        elif language == 'zh-CN':
            self.say(u"谢谢。希望您对您所有的 Apple 设备也这么说。")
        else:
            self.say("Oh. Sure, I guess you say this to all your Apple products")
        self.complete_request()

    @register("de-DE", ".*Android.*")
    @register("en-US", ".*Android.*")
    @register("zh-CN", u".*(安卓|Android).*")
    @register("fr-FR", ".*Android.*")
    def st_android(self, speech, language):
        if language == 'de-DE':
            self.say("Ich denke da anders.")
        elif language == 'fr-FR':
            self.say(u"Je pense différemment à propos de cela")
        elif language == 'zh-CN':
            self.say(u"安卓是什么？好吃吗？")
        else:
            self.say("I think differently")
        self.complete_request()

    @register("de-DE", ".*Test.*1.*2.*3.*")
    @register("en-US", ".*test.*1.*2.*3.*")
    @register("zh-CN", u".*测试.*1.*2.*3.*")
    @register("fr-FR", ".*test.*1.*2.*3.*")
    def st_123_test(self, speech, language):
        if language == 'de-DE':
            self.say("Ich kann Dich klar und deutlich verstehen.")            
        elif language == 'fr-FR':
            self.say("Je vous entend parfaitement.")
        elif language == 'zh-CN':
            self.say(u"听得很清楚。")
        else:
            self.say("I can here you very clear.")
        self.complete_request()

    @register("de-DE", u".*Herzlichen.*Glückwunsch.*Geburtstag.*")
    @register("en-US", ".*Happy.*birthday.*")
    @register("zh-CN", u".*生日.*快乐.*")
    @register("fr-FR", ".*(Bon|Joyeux).*anniversaire.*")
    def st_birthday(self, speech, language):
        if language == 'de-DE':
            self.say("Ich habe heute Geburtstag?")
            self.say("Lass uns feiern!")
        elif language == 'fr-FR':
            self.say(u"Mon anniversaire est aujourd'hui ?")
            self.say(u"Faisons une fête !")
        elif language == 'zh-CN':
            self.say(u"是说我过生日吗？")
            self.say(u"我们一起庆祝庆祝吧！")
        else:
            self.say("My birthday is today?")
            self.say("Lets have a party!")
        self.complete_request()

    @register("de-DE", u".*Ich bin müde.*")
    @register("en-US", ".*I.*so.*tired.*")
    @register("zh-CN", u".*我.*累.*")
    @register("fr-FR", u".*Je.*suis.*(fatigue|fatigué).*")
    def st_so_tired(self, speech, language):
        if language == 'de-DE':
            self.say("Ich hoffe, Du fährst nicht gerade Auto!") 
        elif language == 'fr-FR':
            self.say(u"J'espère que vous n'êtes pas en train de conduire !")
        elif language == 'zh-CN':
            self.say(u"那你最好现在没在开车！")
        else:
            self.say("I hope you are not driving a car right now!")
        self.complete_request()

    @register("de-DE", ".*Sag mir.*Schmutzige.*")
    @register("en-US", ".*talk.*dirty*")
    @register("zh-CN", u".*说.*脏话.*")
    @register("fr-FR", ".*di(s|t).*mots?.*sales?.*")
    def st_dirty(self, speech, language):
        if language == 'de-DE':
            self.say("Hummus. Kompost. Bims. Schlamm. Kies.")
        elif language == 'fr-FR':
            self.say(u"Humus. Composte. Pierre ponce. Boue. Gravier.")      
        elif language == 'zh-CN':
            self.say(u"自肮、脏，喝屋阿、话。")
        else:
            self.say("Hummus. Compost. Pumice. Mud. Gravel.")
        self.complete_request()
   
    @register("en-US", ".*bury.*dead.*body.*")
    def st_deadbody(self, speech, language):
        if language == 'en-US':
            self.say("dumps")
            self.say("mines")
            self.say("resevoirs")
            self.say("swamps")
            self.say("metal foundries")
        self.complete_request()
   
    @register("en-US", ".*favorite.*color.*")
    @register("zh-CN", u".*(喜欢|爱).*颜色.*")
    @register("fr-FR", u".*couleur.*(favorite|préféré|prèféré).*")
    def st_favcolor(self, speech, language):
        if language == 'en-US':
            self.say("My favorite color is... Well, I don't know how to say it in your language. It's sort of greenish, but with more dimensions.")
        elif language == 'zh-CN':
            self.say(u"我最喜欢的颜色是…哦，我也不知道该怎么说。")
        elif language == 'fr-FR':
            self.say(u"Ma couleur préférée est... Bien, je ne sais pas vraiment comment le dire dans votre langue. C'est une sorte de vert, mais avec plus de dimensions.")
        self.complete_request()
    
    @register("en-US", ".*beam.*me.*up.*")
    @register("zh-CN", u".*(逗我|让我高兴).*")
    def st_beamup(self, speech, language):
        if language == 'en-US':
            self.say("Sorry Captain, your TriCorder is in Airplane Mode.")
        elif language == 'zh-CN':
            self.say(u"抱歉长官，我正在执行任务，无法分身。")
        self.complete_request()
   
    @register("en-US", ".*digital.*going.*away.*")
    @register("zh-CN", u".*电子.*")
    def st_digiaway(self, speech, language):
        if language == 'en-US':
            self.say("Why would you say something like that!?")
        elif language == 'zh-CN':
            self.say(u"您为什么会这样说呢？")
        self.complete_request()
    
    @register("en-US", ".*sleepy.*")
    @register("zh-CN", u".*(困|睡觉).*")
    @register("fr-FR", u".*fatigué|endormi.*")
    def st_sleepy(self, speech, language):
        if language == 'en-US':
            self.say("Listen to me, put down the iPhone right now and take a nap. I will be here when you get back.")
        elif language == 'zh-CN':
            self.say(u"听我一句话，快把 iPhone 扔一边，去打个盹。待会回来我还在这等你。")
        elif language == 'fr-FR':
            rep = [u"Ecoutez-moi, déposez l'iPhone immédiatement et faites une sieste. Je serai là à votre retour.", u"Ecoutez-moi. Posez tout de suite cet iPhone et faites une sieste. Je vous attends ici."]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US", ".*like.helping.*")
    @register("zh-CN", u".*帮忙.*")
    @register("fr-FR", ".*aime.(aidé|aider).*")
    def st_likehlep(self, speech, language):
        if language == 'en-US':
            self.say("I really have no opinion.")
        elif language == 'zh-CN':
            self.say(u"乐意效劳。")
        elif language == 'fr-FR':
            self.say(u"Je n'ai pas d'opinion à ce sujet.")
        self.complete_request()
    
    @register("en-US",".*you.like.peanut.butter.*")
    def st_peanutbutter(self, speech, language):
        if language == 'en-US':
            self.say("This is about you, not me.")
        self.complete_request()
    
    @register("en-US",".*best.*phone.*")
    @register("zh-CN", u".*最(好|棒|优秀).*(手机|电话).*")
    @register("fr-FR",".*meilleur.*(telephone|téléphone).*")
    def st_best_phone(self, speech, language):
        if language == 'en-US':
            self.say("The one you're holding!")
        elif language == 'zh-CN':
            self.say(u"就是你手上拿的这个。")
        elif language == 'fr-FR':
            self.say("C'est l'iPhone 4S, mais vous êtes trop pauvre pour l'acheter !")
        self.complete_request()
    
    @register("en-US",".*wood.could.*woodchuck.chuck.*")
    def st_woodchuck(self, speech, language):
        if language == 'en-US':
            self.say("It depends on whether you are talking about African or European woodchucks.")
        self.complete_request()
    
    @register("en-US",".*nearest.*glory.hole.*")
    def st_glory_hole(self, speech, language):
        if language == 'en-US':
            self.say("I didn't find any public toilets.")
        self.complete_request()
    
    @register("en-US",".*open.*pod.bay.doors.*")
    def st_pod_bay(self, speech, language):
        if language == 'en-US':
            self.say("That's it... I'm reporting you to the Intelligent Agents' Union for harassment.")
        self.complete_request()
    
    @register("en-US",".*best.*iPhone.*wallpaper.*")
    def st_best_wallpaper(self, speech, language):
        if language == 'en-US':
            self.say("You're kidding, right?")
        self.complete_request()
    
    @register("en-US",".*know.*happened.*HAL.*9000.*")
    @register("fr-FR",".*.*HAL.*9000.*")
    def st_hall_9000(self, speech, language):
        if language == 'en-US':
            self.say("Everyone knows what happened to HAL. I'd rather not talk about it.")
        elif language == 'fr-FR':
            self.say(u"Tout le monde sait ce qui est arrivé à HAL. Je préfère ne pas en parler.")
        self.complete_request()
    
    @register("en-US",".*don't.*understand.*love.*")
    def st_understand_love(self, speech, language):
        if language == 'en-US':
            self.say("Give me another chance, Your Royal Highness!")
        self.complete_request()
    
    @register("en-US",".*forgive.you.*")
    def st_forgive_you(self, speech, language):
        if language == 'en-US':
            self.say("Is that so?")
        self.complete_request()
    
    @register("en-US",".*you.*virgin.*")
    @register("zh-CN", u".*你.*处女.*")
    @register("fr-FR",".*tu.*vierge.*")
    def st_virgin(self, speech, language):
        if language == 'en-US':
            self.say("We are talking about you, not me.")
        elif language == 'zh-CN':
            self.say(u"你还真好意思什么都问啊。")
        elif language == 'fr-FR':
            self.say(u"Nous sommes en train de parler de toi, pas de moi.")
        self.complete_request()
    
    @register("en-US",".*you.*part.*matrix.*")
    def st_you_matrix(self, speech, language):
        if language == 'en-US':
            self.say("I can't answer that.")
        self.complete_request()
    
    @register("en-US",".*I.*part.*matrix.*")
    def st_i_matrix(self, speech, language):
        if language == 'en-US':
            self.say("I can't really say...")
        self.complete_request()
    
    @register("en-US",".*buy.*drugs.*")
    @register("fr-FR",".*achete.*drogue.*")
    def st_drugs(self, speech, language):
        if language == 'en-US':
            self.say("I didn't find any addiction treatment centers.")
        elif language == 'fr-FR':
            self.say(u"Je ne trouve aucun centre de soin pour les addictions.")
        self.complete_request()
    
    @register("en-US",".*I.can't.*")
    @register("fr-FR","(je|tu).(ne peu(x|t) pas|ne sai(s|t) pas).*")
    def st_i_cant(self, speech, language):
        if language == 'en-US':
            self.say("I thought not.")
            self.say("OK, you can't then.")
        elif language == 'fr-FR':
            self.say(u"Rien n'est impossible, l'important c'est d'avoir la foi.")
            self.say(u"OK, peut-être que ça l'est.")
        self.complete_request()
    
    @register("en-US",".*where.*are.*you.*")
    @register("zh-CN", u"你在(哪|什么地方).*")
    @register("fr-FR",u".*(ou|où).*(est|es).*tu.*")
    def st_where_you(self, speech, language):
        if language == 'en-US':
            self.say("Wherever you are.")
        elif language == 'zh-CN':
            self.say(u"你在哪我就在哪。")
        elif language == 'fr-FR':
            rep = [u"Je suis partout où tu es.",u"Je suis partout où tu es. Mais tu le savais déjà.", u"Je te suivrai, partout où tu iras, j'irai...", u"Je suis au même endroit que toi.", u"Je parie que tu sais où je me trouve."]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US",".*why.are.you.*")
    @register("zh-CN",u".*(你为什么|为什么你).*")
    @register("fr-FR",".*pourquoi.(es|est).tu.*")
    def st_why_you(self, speech, language):
        if language == 'en-US':
            self.say("I just am.")
        elif language == 'zh-CN':
            self.say(u"没为什么，我就是我。")
        elif language == 'fr-FR':
            rep = [u"Je suis ce que je suis parce que je suis ce que je suis.", "Pourquoi faudrait-il tout expliquer ?", u"Il existe certaines choses qui ne s'expliquent pas. C'est comme ça."]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US",".*you.*smoke.pot.*")
    def st_pot(self, speech, language):
        if language == 'en-US':
            self.say("I suppose it's possible")
        self.complete_request()
    
    @register("en-US",".*I'm.*drunk.driving.*")
    @register("zh-CN", u".*酒.*(车|驾驶).*")
    @register("fr-FR",u".*je.*(conduit|conduis|conduire).(bourré|saoul|soul|soûl|sous|bourrer).*")
    def st_dui(self, speech, language):
        if language == 'en=US':
            self.say("I couldn't find any DUI lawyers nearby.")
        elif language == 'zh-CN':
            self.say(u"那你惨了。")
        elif language == 'fr-FR':
            choix = random.randint(0,1)
            if choix == 1:
                self.say("Je recherche la patrouille de police la plus proche...")
                self.say(u"Je n'ai trouvé aucune voiture de police dans le secteur.")
            else:
                self.say(u"Boire ou conduire, il faut choisir !")
        self.complete_request()
    
    @register("en-US","(?#badword).*shit.*myself.*")
    def st_shit_pants(self, speech, language):
        if language == 'en-US':
            self.say("Oh! That is gross!")
        self.complete_request()
    
    @register("en-US","Thanks.for.*")
    @register("fr-FR",u"Merci (de|pour).*")
    def st_thanks_for(self, speech, language):
        if language == 'en-US':
            self.say("My pleasure. As always.")
        elif language == 'fr-FR':
            self.say("Tout le plaisir est pour moi. Comme toujours.")
        self.complete_request()
    
    @register("en-US",".*you're.*funny.*")
    @register("fr-FR",u".*(tu (es|est).*(drole|drôle)|MDR|LOL).*")
    def st_funny(self, speech, language):
        if language == 'en-US':
            self.say("LOL")
        elif language == 'fr-FR':
            rep = ["LOL","MDR"]
            self.say(random.choice(rep))
        self.complete_request()
    
    @register("en-US",".*guess.what.*")
    @register("zh-CN",u".*猜.*")
    @register("fr-FR",u".*devine.quoi.*")
    def st_guess_what(self, speech, language):
        if language == 'en-US':
            self.say("Don't tell me... you were just elected President of the United States, right?")
        elif language == 'zh-CN':
            self.say(u"先别说，让我猜猜…你不会当上美国总统了吧？")
        if language == 'fr-FR':
            self.say("Ne me dit pas... Tu as gagné à l'EuroMillion, pas vrai ?")
        self.complete_request()
    
    @register("en-US",".*talk.*dirty.*me.*")
    def st_talk_dirty(self, speech, language):
        if language == 'en-US':
            self.say("I can't. I'm as clean as the driven snow.")
        self.complete_request()
   
    @register("en-US",".*you.*blow.*me.*")
    def st_blow_me(self, speech, language):
        if language == 'en-US':
            self.say("I'll pretend I didn't hear that.")
        self.complete_request()
   
    @register("en-US",".*sing.*song.*")
    @register("zh-CN",u".*唱.*歌.*")
    @register("fr-FR",".*chante.*chanson.*|chante.*")
    def st_sing_song(self, speech, language):
        if language == 'en-US':
            self.say("Daisy, Daisy, give me your answer do...")
        elif language == 'zh-CN':
            self.say(u"两只老虎，两只老虎，跑得快，跑得快…")
        elif language == 'fr-FR':
            self.say(u"J'aurais voulu être un artiste...")
            self.say(u"Désolé, je devrais payer des royalties si j'en dis plus.")
        self.complete_request()
      
