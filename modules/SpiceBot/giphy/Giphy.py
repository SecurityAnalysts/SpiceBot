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
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('gif', 'giphy')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 0)
    if target != "roulette":
        query = target.replace(' ', '%20')
        query = str(query)
        i = 0
        while i < 3:
            gif, randno = getGif(query)
            if gif:
                osd(bot, trigger.sender, 'say', "Result number " + str(randno) + ": " + gif)
                i = 5
            else:
                i = i + 1
        if i == 3:
            osd(bot, trigger.sender, 'say', "Hmm...Couldn't find a gif for that!")
    elif target == "roulette":
        gif = roulette()
        if gif:
            osd(bot, trigger.sender, 'say', "Click at your own risk! " + gif)
    else:
        osd(bot, trigger.sender, 'say', "Tell me what you're looking for!")


def getGif(query):
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    limit = 50
    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(query)+'&api_key=' + str(api) + '&limit=' + str(limit) + '&rating=r'
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(0, limit)
    try:
        id = data['data'][randno]['id']
        gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    except IndexError:
        gif = ""
    return gif, randno


def roulette():
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    # randno = randint(0,9)
    # if randno == 4:
    url = 'http://api.giphy.com/v1/gifs/random?api_key=' + str(api) + '&rating=nsfw'
    # else:
    #    url = 'http://api.giphy.com/v1/gifs/random?api_key=' + str(api) + '&rating=g'
    data = json.loads(urllib2.urlopen(url).read())
    try:
        id = data['data']['id']
        gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    except KeyError:
        gif = ""
    return gif
