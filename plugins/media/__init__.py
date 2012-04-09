#!/usr/bin/python
# -*- coding: utf-8 -*-
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

from plugin import *
from siriObjects.baseObjects import ObjectIsCommand, RequestCompleted
from siriObjects.uiObjects import UIAddViews, UIAssistantUtteranceView
from siriObjects.systemObjects import ResultCallback
from siriObjects.mediaObjects import *
import re


res = {
        'pause':
            {'de-DE': u"Paused",
             'en-US': u"Paused.",
             'zh-CN': u"已暂停"
             },
        'stop':
            {'de-DE': u"Stopping.",
             'en-US': u"Stopping",
             'zh-CN': u"正在停止"
             },
        'resume':
            {'de-DE': u"Ok...",
             'en-US': u"Ok...",
             'zh-CN': u"好的…"
             },
        'forward':
            {'de-DE': u"Weiter zum nächsten Lied...",
             'en-US': u"forwarding to next song...",
             'zh-CN': u"切到下首歌"
             },
        'back':
            {'de-DE': u"Weiter zum letzten Lied...",
             'en-US': u"forwarding to last song...",
             'zh-CN': u"切到最后一首歌"
             },
        'beginning':
            {'de-DE': u"Zum anfang der Wiedergabe Liste...",
             'en-US': u"going to the beginning of the playlist...",
             'zh-CN': u"从列表的第一首歌开始播放…"
             },
        'play':
            {'de-DE': u'Ok, ich spiele Musik ab.',
             'en-US': u'Ok, Starting your song now!.',
             'zh-CN': u"好的，开始播放。"
             },
        'error':
            {'de-DE': u"Kein Titel gefunden.",
             'en-US': u"No title found in your iPod",
             'zh-CN': u"抱歉，未找到。"
             }
    }

class iPod(Plugin):
    
    def searchMusic(self,music):
        constraints = MPSearchConstraint()
        constraints.query = music
        constraints.searchProperties = ["Album", "Artist", "Composer", "Genre", "Title"]
        search = MPSearch(self.refId)
        search.constraints = [constraints]
        search.maxResults = 10
        search.searchProperties = ["Album", "Artist", "Composer", "Genre", "Title"]
        search.searchTypes =  ["Playlist", "Podcast", "Song"]
        search.searchValue = music
        answerObj = self.getResponseForRequest(search)
        if ObjectIsCommand(answerObj, MPSearchCompleted):
            answer = MPSearchCompleted(answerObj)
            return answer.results if answer.results != None else []
        else:
            raise StopPluginExecution("Unknown response: {0}".format(answerObj))
            return []
            
    def play(self, results, language):
        collection = MPTitleCollection()
        collection.items = []
        for result in results:
            if not hasattr(result, 'genre'):
                result.genre = ""
            if not hasattr(result, 'trackNumber'):
                result.trackNumber = ""
            if not hasattr(result, 'artist'):
                result.artist = ""
            if not hasattr(result, 'title'):
                result.title = ""
            if not hasattr(result, 'sortTitle'):
                result.sortTitle = ""
            if not hasattr(result, 'playCount'):
                result.playCount = ""
            if not hasattr(result, 'rating'):
                result.rating = ""
            if not hasattr(result, 'album'):
                result.album = ""
            if not hasattr(result, 'identifier'):
                result.identifier = ""
            song = MPSong()
            song.album = result.album
            song.artist = result.artist
            song.genre = result.genre
            song.playCount = result.playCount
            song.rating = result.rating
            song.sortTitle = result.sortTitle
            song.title = result.title
            song.trackNumber = result.trackNumber
            song.identifier = result.identifier
            collection.items.append(song)
            collection.sortTitle = result.title
            collection.title = result.sortTitle
        collection.identifier = result.identifier
        complete = MPSetQueue(self.refId)
        complete.mediaItems = collection
        self.getResponseForRequest(complete)
        commands = MPSetState(self.refId)
        commands.state = "Playing"
        commands2 = MPEnableShuffle(self.refId)
        commands2.enable = False
        code = 0
        root = UIAddViews(self.refId)
        root.dialogPhase = "Summary"
        assistant = UIAssistantUtteranceView()
        assistant.dialogIdentifier = "PlayMedia#nowPlayingMediaItemByTitle"
        assistant.speakableText = assistant.text = res["play"][language]
        root.views = [(assistant)]
        root.callbacks = [ResultCallback([commands, commands2], code)]
        callback = [ResultCallback([root], code)]
        self.send_object(RequestCompleted(self.refId, callback))
        self.complete_request()
    
    def pause(self, language):
        commands = MPSetState(self.refId)
        commands.state = "Paused"
        code = 0
        root = UIAddViews(self.refId)
        root.dialogPhase = "Summary"
        assistant = UIAssistantUtteranceView()
        assistant.dialogIdentifier = "PlayMedia#Paused"
        assistant.speakableText = assistant.text = res["pause"][language]
        root.views = [(assistant)]
        root.callbacks = [ResultCallback([commands], code)]
        callback = [ResultCallback([root], code)]
        self.send_object(RequestCompleted(self.refId, callback))
        self.complete_request()
        
    def stop(self, language):
        commands = MPSetState(self.refId)
        commands.state = "Stopped"
        code = 0
        root = UIAddViews(self.refId)
        root.dialogPhase = "Summary"
        assistant = UIAssistantUtteranceView()
        assistant.dialogIdentifier = "PlayMedia#Stopped"
        assistant.speakableText = assistant.text = res["stop"][language]
        root.views = [(assistant)]
        root.callbacks = [ResultCallback([commands], code)]
        callback = [ResultCallback([root], code)]
        self.send_object(RequestCompleted(self.refId, callback))
        self.complete_request()
        
    def resume(self, language):
        commands = MPSetState(self.refId)
        commands.state = "Playing"
        code = 0
        root = UIAddViews(self.refId)
        root.dialogPhase = "Summary"
        assistant = UIAssistantUtteranceView()
        assistant.dialogIdentifier = "PlayMedia#SkipToNext"
        assistant.speakableText = assistant.text = res["resume"][language]
        root.views = [(assistant)]
        root.callbacks = [ResultCallback([commands], code)]
        callback = [ResultCallback([root], code)]
        self.send_object(RequestCompleted(self.refId, callback))
        self.complete_request()
        
    def forward(self, language):
        commands = MPSetState(self.refId)
        commands.state = "Playing"
        commands2 = MPSetPlaybackPosition(self.refId)
        commands2.position = "NextItem"
        code = 0
        root = UIAddViews(self.refId)
        root.dialogPhase = "Summary"
        assistant = UIAssistantUtteranceView()
        assistant.dialogIdentifier = "PlayMedia#SkipToNext"
        assistant.speakableText = assistant.text = res["forward"][language]
        root.views = [(assistant)]
        root.callbacks = [ResultCallback([commands, commands2], code)]
        callback = [ResultCallback([root], code)]
        self.send_object(RequestCompleted(self.refId, callback))
        self.complete_request()
        
    def back(self, language):
        commands = MPSetState(self.refId)
        commands.state = "Playing"
        commands2 = MPSetPlaybackPosition(self.refId)
        commands2.position = "PreviousItem"
        code = 0
        root = UIAddViews(self.refId)
        root.dialogPhase = "Summary"
        assistant = UIAssistantUtteranceView()
        assistant.dialogIdentifier = "PlayMedia#Previous"
        assistant.speakableText = assistant.text = res["back"][language]
        root.views = [(assistant)]
        root.callbacks = [ResultCallback([commands, commands2], code)]
        callback = [ResultCallback([root], code)]
        self.send_object(RequestCompleted(self.refId, callback))
        self.complete_request()
        
    def beginning(self, language):
        commands = MPSetState(self.refId)
        commands.state = "Playing"
        commands2 = MPSetPlaybackPosition(self.refId)
        commands2.position = "Beginning"
        code = 0
        root = UIAddViews(self.refId)
        root.dialogPhase = "Summary"
        assistant = UIAssistantUtteranceView()
        assistant.dialogIdentifier = "PlayMedia#SkipToBeginning"
        assistant.speakableText = assistant.text = res["beginning"][language]
        root.views = [(assistant)]
        root.callbacks = [ResultCallback([commands, commands2], code)]
        callback = [ResultCallback([root], code)]
        self.send_object(RequestCompleted(self.refId, callback))
        self.complete_request()
            
    @register("de-DE", "spiele (?P<music>[\w ]+)")
    @register("en-US", "Play (?P<music>[\w ]+)")
    @register("zh-CN", u".*(播放)\s?(?P<music>[\w ]+)")
    def playMusic(self, speech, language, regex):
        music = regex.group('music')
        results = self.searchMusic(music)
        library = None
        if len(results) == 0:
            self.say(res["error"][language])
        else:
            library = results
        if library != None:
            self.play(library, language)
            return
        self.complete_request()
        
    @register("de-DE", "pause")
    @register("en-US", "pause")
    @register("zh-CN", u"暂停(音乐|播放)?")
    def pauseMusic(self, speech, language, regex):
        self.pause(language)
        self.complete_request()
        
    @register("de-DE", u"überspringen")
    @register("en-US", "forward")
    @register("zh-CN", u"(前进|下一首|下一曲|切歌).*")
    def forwardMusic(self, speech, language, regex):
        self.forward(language)
        self.complete_request()
        
    @register("de-DE", u"anfang")
    @register("en-US", "beginning")
    @register("zh-CN", u"(从头播放|重新播放|从头开始).*")
    def backMusic(self, speech, language, regex):
        self.beginning(language)
        self.complete_request()
        
    @register("de-DE", u"zurück")
    @register("en-US", "back")
    @register("zh-CN", u"(后退|前一首|上一首).*")
    def backMusic(self, speech, language, regex):
        self.back(language)
        self.complete_request()
        
    @register("de-DE", u"abspielen")
    @register("en-US", u"resume")
    @register("zh-CN", u"继续(音乐|播放)?")
    def resumeMusic(self, speech, language, regex):
        self.resume(language)
        self.complete_request()
    
    @register("de-DE", "stop")
    @register("en-US", "stop")
    @register("zh-CN", u"停止(音乐|播放)?")
    def stopMusic(self, speech, language, regex):
        self.stop(language)
        self.complete_request()