#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
from SpicebotShared import *
import sopel.module
import sys
import os
import urllib2
import json
import random

moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)

@sopel.module.commands('trivia')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    if len(triggerargsarray) > 0:
        if (triggerargsarray[0] == 'answer':
            answer(bot,trigger,triggerargsarray)
    else:
        lastquestionanswered = get_database_value(bot,'triviauser','triviaanswered')
        if lastquestionanswered == 'f':
            getQuestionFromDb(bot)
        else:
            askQuestion(bot)
        

    
def askQuestion(bot):
    type,question,arrAnswers,answer = getQuestion()
    set_database_value(bot,'triviauser','triviaq',question)    
    set_database_value(bot,'triviauser','triviaa',answer)
    set_database_value(bot,'triviauser','triviachoices',arrAnswers)
    set_database_value(bot,'triviauser','triviaanswered','f')
    
    if type == "boolean":
        question = "True or False: " + question
        bot.say("Question: " + question)
    else:
        bot.say("Question: " + question)
        bot.say("Choices:" + arrAnswers[0] + " " + arrAnswers[1] + " " + arrAnswers[2] + " " + arrAnswers[3])
        
def getQuestionFromDb(bot):
    question = get_database_value(bot,'triviauser','triviaq')
    arrAnswers = get_database_value(bot,'triviauser','triviachoices')
    bot.say("Still waiting for someone to answer this one: " + question)
    #if len(str(arrAnswers) > 2):
    try:
        bot.say("Choices:" + arrAnswers[0] + " " + arrAnswers[1] + " " + arrAnswers[2] + " " + arrAnswers[3])
    except IndexError:
        bot.say("Choices:" + arrAnswers[0] + ", " + arrAnswers[1])
    #else:
    #bot.say("Choices:" + arrAnswers[0] + " " + arrAnswers[1])
    
def getQuestion():
    url = 'https://opentdb.com/api.php?amount=1'
    data = json.loads(urllib2.urlopen(url).read())
           
    results = str(data['results'])
    a = results.split("',") 
    type = splitEntry(a[1])
    if type != "boolean":
        wrongAnswers = data['results'][0]
        wrongAnswers = wrongAnswers['incorrect_answers']
        arrWrong = str(wrongAnswers).split("',")
        choiceOne = arrWrong[0].replace("u'","",1).strip()
        choiceTwo = arrWrong[1].replace("u'","",1).strip()
        choiceThree = arrWrong[2].replace("u'","",1).strip()
        choiceOne = sanitizeString(choiceOne)
        choiceTwo = sanitizeString(choiceTwo)
        choiceThree = sanitizeString(choiceThree)
        answer = splitEntry(a[4])
        answer = sanitizeString(answer)
        arrAnswers = [choiceOne,choiceTwo,choiceThree,answer]
        random.shuffle(arrAnswers)
        arrAnswers[0] = "A) "+arrAnswers[0]
        arrAnswers[1] = "B) "+arrAnswers[1]
        arrAnswers[2] = "C) "+arrAnswers[2]
        arrAnswers[3] = "D) "+arrAnswers[3]
        question  = splitEntry(a[2])        
    else:
        question  = splitEntry(a[2])
        answer = splitEntry(a[4])
        arrAnswers=['True','False']
                
    return type,question,arrAnswers,answer

def answer(bot,trigger,triggerargsarray):
    if triggerargsarray[0] == "answer":
        guesser = trigger.nick
        useranswer = triggerargsarray[1]
        correctanswer = get_database_value(bot,'triviauser','triviaa')
        useranswer = useranswer.lower()
        correctanswer = correctanswer.lower()
        if useranswer == correctanswer:
            set_database_value(bot,'triviauser','triviaanswered','t')
            bot.say(guesser + " has answered correctly!")
        else:
            bot.say("Sorry, " + guesser + ", that is incorrect.")                    
                                  
                                 
        
def splitEntry(entry):
    splitChar = ':'
    a = entry.split(splitChar)
    result = a[1]
    result = result.replace("u'","",1).strip()
    result = sanitizeString(result)
    return result

def sanitizeString(entry):
    result = entry.replace('[','')
    result = result.replace(']','')
    result = result.replace("&quot;",'"')
    result = result.replace("&#039;","'")
    result = result.replace("'","",len(result))
    return result

# Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str('trivia_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

# Set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('trivia_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
# get current value and update it adding newvalue
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey)
    databasecolumn = str('trivia_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))

    
    
