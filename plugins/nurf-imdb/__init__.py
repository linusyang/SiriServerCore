#!/usr/bin/python
# -*- coding: utf-8 -*-
#nurf-imdb.py

#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

#IMDb Plugin for SiriServer
#by Casey (Nurfballs) Mullineaux 

# Download: 
#   - https://github.com/Nurfballs/SiriServer-IMDb

# Pre-requisites:
#   - Requires IMDbPy. 
#       Install IMDbPY (sudo apt-get install python-imdbpy) or download it from http://imdbpy.sourceforge.net

#Version 0.1 
#   - Initial release

# === Usage ===  
# -- Get information about a movie --
# (movie lookup)* ([\w ]+)
# Example: say "Movie lookup The Matrix"

# -- Get director for a movie --
# (who directed)* ([\w ]+)
# Example: say "Who directed The Matrix" 

#-- Get the name of the actor who played a character in a movie or TV show--
# (who played|who plays|who was)* ([\w ]+) *in* ([\w ]+)
# Example: say "Who played Morpheus in The Matrix"

# See README at https://github.com/Nurfballs/SiriServer-IMDb for full set of instructions.


import re
import sys
import urllib2, urllib
import json
from plugin import *

from siriObjects.uiObjects import AddViews
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine


try:
   from imdb import IMDb
   import imdb.helpers
except ImportError:
   raise NecessaryModuleNotFound("Oops! Unable to locate the IMDb library. Please install IMDbPy. e.g. (sudo easy_install IMDbPy) or (sudo apt-get install python-imdbpy)")

class nurf_imdb(Plugin):

    @register("en-US", "(who directed)* ([\w ]+)")
    @register("zh-CN", u"谁导演(?:了|的)?([\w ]+)")
    def who_director(self, speech, language,  regex):
        MovieTitle = regex.group(regex.lastindex).strip()
        ia = IMDb()
        search_result = ia.search_movie(MovieTitle)
        if not search_result:
            if language == "zh-CN":
                self.say(u"抱歉，我没找到“" + str(MovieTitle.encode("utf-8")) + u"”的信息。")
            else:
                self.say("Sorry, I could not find any information for " + MovieTitle)
            self.complete_request()
        else:
            movie_info = search_result[0]
            ia.update(movie_info)
            
            strFullTitle = movie_info['title']
            strDirector = movie_info['director'][0]['name']
            
            if language == "zh-CN":
                self.say(str(strDirector.encode("utf-8")) + u" 导演了 "+ str(strFullTitle.encode("utf-8")))
            else:
                self.say(strDirector + " directed "+ strFullTitle)
            self.complete_request()
    
    @register("en-US",  "(who played|who plays|who was)* ([\w ]+) *in* ([\w ]+)")
    def get_actorbycharacter(self,  speech,  language,  regex):
        if language == "en-US":
            
            # get the name of the character to look up
            character = regex.group(2)
            character = character.title().strip()
            
            # get the name of the movie to look up
            movie = regex.group(3)
            movie = movie.title()
            
            ia = IMDb()
            search_result = ia.search_movie(movie)
            
            if not search_result:
                self.say("No matches found for that title")
                self.complete_request()
            else:
                movietitle = search_result[0]['title']
                moviedetails = search_result[0]
                ia.update(moviedetails)

                cast = moviedetails['cast']
                
                try:
                    for actor in cast:                 
                        if character in actor.currentRole['name']:
                            self.say(actor['name'])
                            
                            #Get Image
                            Query = urllib.quote_plus(actor['name'].encode("utf-8"))
                            SearchURL = u'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&imgsz=small|medium|large|xlarge&q=' + str(Query)
                            try:
                                jsonResponse = urllib2.urlopen(SearchURL).read()
                                jsonDecoded = json.JSONDecoder().decode(jsonResponse)
                                ImageURL = jsonDecoded['responseData']['results'][0]['unescapedUrl']
                                view = AddViews(self.refId, dialogPhase="Completion")
                                ImageAnswer = AnswerObject(title=str(actor['name']),lines=[AnswerObjectLine(image=ImageURL)])
                                view1 = AnswerSnippet(answers=[ImageAnswer])
                                view.views = [view1]
                                self.sendRequestWithoutAnswer(view)
                                self.complete_request()
                            except (urllib2.URLError):
                                    self.say("Sorry, a connection to Google Images could not be established.")
                                    self.complete_request()

                            
                            self.complete_request()
                                        
                    self.complete_request()
                except:
                    self.say("Sorry, I couldnt find any characters by that name in " + movietitle)
                    self.complete_request()

    @register("en-US",  "(find|show).*movie ([\w ]+)")
    @register("zh-CN",  u"找?电影([\w ]+)")
    def move_lookup(self,  speech,  language,  regex):
       
        MovieTitle = regex.group(regex.lastindex).strip()
        ia = IMDb()
        search_result = ia.search_movie(MovieTitle)
        if not search_result:
            if language == "zh-CN":
                self.say(u"抱歉，我没找到“" + str(MovieTitle.encode("utf-8")) + u"”的信息。")
            else:
                self.say("Sorry, I could not find any information for " + MovieTitle)
            self.complete_request()
        
        else:
            
            if language == "zh-CN":
                self.say(u"好的，我来为您查找。")
            else:
                self.say("Let me look that up for you.")
            view = AddViews(self.refId, dialogPhase="Completion")
            
            # -- Get Movie Info --
            movie_info = search_result[0]
            MovieTitle = movie_info['long imdb canonical title']
            ia.update(movie_info)
        
            # -- Get the URL for poster --
            AnswerStringPosterURL = movie_info['cover url']
            # Output to the AnswerObject
            NurfIMDBAnswerPosterURL = AnswerObject(title=MovieTitle,lines=[AnswerObjectLine(image=AnswerStringPosterURL)])
        
            #-- Get Rating --
            AnswerStringRating = str(movie_info['rating']) + "/10 (" + str(movie_info['votes']) + " votes)"
            # Output to the AnswerObject
            NurfIMDBAnswerRating = AnswerObject(title='Rating:',lines=[AnswerObjectLine(text=AnswerStringRating)]) 
                    
            #-- Get Plot --
            plot = movie_info['plot'][0].split('::')
            AnswerStringPlot = plot[0]
            # Output to the AnswerObject
            NurfIMDBAnswerPlot = AnswerObject(title='Plot:',lines=[AnswerObjectLine(text=AnswerStringPlot)]) 

            #-- Get Directors --
            AnswerStringDirectors = ''
            for director in movie_info['director']:
                AnswerStringDirectors = AnswerStringDirectors + director['name'] + ", "
            AnswerStringDirectors = AnswerStringDirectors.rstrip(',') #Remove the last comma from the answerstring
            # Output to the AnswerObject
            NurfIMDBAnswerDirectors = AnswerObject(title='Directors:',lines=[AnswerObjectLine(text=AnswerStringDirectors)]) 
                    
            #-- Get Writers --
            AnswerStringWriters = ''
            for writer in movie_info['writer']:
                AnswerStringWriters = AnswerStringWriters + writer['name'] + ", "
            AnswerStringWriters = AnswerStringWriters.rstrip(',') #Remove the last comma from the answerstring
            # Output to the AnswerObject
            NurfIMDBAnswerWriters = AnswerObject(title='Writers:',lines=[AnswerObjectLine(text=AnswerStringWriters)]) 
        
            # -- Get Cast --
            AnswerStringCast = ''
            for actor in movie_info['cast']:
                try:
                    AnswerStringCast = AnswerStringCast + actor['name'] + " (" + str(actor.currentRole['name']) + "), "
                except:
                    AnswerStringCast = AnswerStringCast + actor['name'] + ", "
            AnswerStringCast = AnswerStringCast.rstrip(',') #Remove the last comma from the answerstring
            # Output to the AnswerObject
            NurfIMDBAnswerCast = AnswerObject(title='Cast:',lines=[AnswerObjectLine(text=AnswerStringCast)]) 
        
            # -- Results --
            #Display the results
            view1 = AnswerSnippet(answers=[NurfIMDBAnswerPosterURL, NurfIMDBAnswerRating, NurfIMDBAnswerPlot, NurfIMDBAnswerDirectors,  NurfIMDBAnswerWriters,  NurfIMDBAnswerCast])
            view.views = [view1]
            self.sendRequestWithoutAnswer(view)
            self.complete_request()
    
    @register("en-US", "(should i see|should i watch)* ([\w ]+)")
    @register("zh-CN", u"([\w ]+)值得.*") 
    def get_director(self, speech, language,  regex):
        MovieTitle = regex.group(regex.lastindex).strip()
        ia = IMDb()
        search_result = ia.search_movie(MovieTitle)
        if not search_result:
            if language == "zh-CN":
                self.say(u"抱歉，我没找到“" + str(MovieTitle.encode("utf-8")) + u"”的信息。")
            else:
                self.say("Sorry, I could not find any information for " + MovieTitle)
            self.complete_request()
            
        else:
            movie_info = search_result[0]
            ia.update(movie_info)    
            MovieRating = movie_info['rating']
            
            if (MovieRating < 6):
                if language == "zh-CN":
                    self.say(u"评级：" + str(MovieRating) + u"。不值一看。")
                else:
                    self.say("Rating: " + str(MovieRating) + " out of 10. You probably should not see this movie.")
            elif (MovieRating < 8):
                if language == "zh-CN":
                    self.say(u"评级：" + str(MovieRating) + u"。还可以，推荐一看。")
                else:
                    self.say("Rating: " + str(MovieRating) + " out of 10. I recommend you see this movie.")
            elif (MovieRating >= 8):
                if language == "zh-CN":
                    self.say(u"评级：" + str(MovieRating) + u"。必看好片！")
                else:
                    self.say("Rating: " + str(MovieRating) + " out of 10. This movie is a must-see!")
            self.complete_request()
    
