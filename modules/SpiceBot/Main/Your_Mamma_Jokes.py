#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
import json
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('urmom')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    joke = getJoke()
    target = spicemanip(bot, triggerargsarray, 1)
    for c in bot.channels:
        channel = c
    if joke:
        if not target:
            osd(bot, trigger.sender, 'say', joke)
        else:
            if not target.lower() not in bot.privileges[channel.lower()]:
                if target == bot.nick:
                    osd(bot, trigger.sender, 'say', 'I have no mother')
                else:
                    osd(bot, trigger.sender, 'say', 'Hey, ' + target + '! ' + joke)
            else:
                osd(bot, trigger.sender, 'say', target + ' is not here but ' + trigger.nick + ' ' + joke)
    else:
        osd(bot, trigger.sender, 'say', 'Please leave the mothers out of it.')


def getJoke():
    url = 'http://api.yomomma.info'
    try:
        page = requests.get(url)
        result = page.content
        jsonjoke = json.loads(result)
        joke = jsonjoke['joke']
    except:
        joke = "yo momma broke the interwebs."
    return joke
