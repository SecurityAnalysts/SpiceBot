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

validpicarray = ['dog', 'cat', 'bird', 'fox']
dog_url = 'https://random.dog/woof.json'
dog_json = 'url'
cat_url = 'http://aws.random.cat/meow'
cat_json = 'file'
bird_url = 'http://shibe.online/api/birds?count=[1-100]&urls=[true/false]&httpsUrls=[true/false]'
bird_json = ''
fox_url = 'https://randomfox.ca/floof/'
fox_json = 'image'


@sopel.module.commands('random')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    pictype = spicemanip(bot, triggerargsarray, 1)
    outputtext = ''
    if not pictype:
        pictype = spicemanip(bot, validpicarray, 'random')
    if pictype not in validpicarray:
        outputtext = str("I don't currently have an api for " + str(pictype))
    else:
        outputtext = getoutputtext(bot, pictype)
    if not outputtext:
        outputtext = "An error has occured."
    osd(bot, trigger.sender, 'say', outputtext)


def getoutputtext(bot, pictype):
    url = eval(pictype+"_url")
    jsontype = eval(pictype+"_json")
    try:
        page = requests.get(url)
        result = page.content
        jsonpoop = json.loads(result)
        outputtext = jsonpoop[jsontype]
    except:
        outputtext = ""
    return outputtext
