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


@sopel.module.commands('facepalm')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = get_trigger_arg(bot, triggerargsarray, 0)
    if not target:
        query = "facepalm"
        gif, randno = getGif(query)
        if gif:
            osd(bot, trigger.sender, 'say', "Result number " + str(randno) + ": " + gif)
        else:
            osd(bot, trigger.sender, 'say', "Hmm...Couldn't find a gif for that!")
    elif target == "major":
        osd(bot, trigger.sender, 'say', "There is not enough facepalm in the world for this")
    elif target == "help":
        osd(bot, trigger.sender, 'say', "Commands: .facepalm help, .facepalm major, or .facepalm")
    else:
        osd(bot, trigger.sender, 'say', "You are really facepalming")


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
