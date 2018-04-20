#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('gif','giphy')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(bot, triggerargsarray, 0)
    if target != "roulette":
        query = target.replace(' ', '%20')
        query = str(query)
        gif,randno = getGif(query)
        if gif:
            bot.say("Result number " + str(randno) + ": " + gif)
        else:
            bot.say("Hmm...Couldn't find a gif for that!")
    elif target == "roulette":
        gif = roulette()
        if gif:
            bot.say("Click at your own risk! " + gif)           
    else:
        bot.say("Tell me what you're looking for!")
            
def getGif(query):
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    limit = 50
    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(query)+'&api_key=' + str(api) + '&limit=' + str(limit) + '&rating=r'    
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(0,limit)
    try:
        id = data['data'][randno]['id']
        gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    except IndexError:
        gif = ""
    return gif,randno

def roulette():
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    randno = randint(0,9)
    if randno == 4:
        url = 'http://api.giphy.com/v1/gifs/random?api_key=' + str(api) + '&tag=nsfw&rating=r'
    else:
        url = 'http://api.giphy.com/v1/gifs/random?api_key=' + str(api) + '&tag=wholesome&rating=g'
    data = json.loads(urllib2.urlopen(url).read())
    try:
        id = data['data']['id']
        gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    except KeyError:
        gif = ""
    return gif
