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


@sopel.module.commands('wouldyourather', 'wyr', 'rather')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'wouldyourather')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    joke = getJoke()
    if joke:
        osd(bot, trigger.sender, 'say', joke)
    else:
        osd(bot, trigger.sender, 'say', 'I would rather not give you a response.')


def getJoke():
    url = 'http://www.rrrather.com/botapi?nsfw=true'
    try:
        page = requests.get(url)
        result = page.content
        jsonjoke = json.loads(result)
        joke = jsonjoke['title'] + " A: " + jsonjoke['choicea'] + " or B: " + jsonjoke['choiceb']
    except:
        joke = "I would rather not."
    return joke
