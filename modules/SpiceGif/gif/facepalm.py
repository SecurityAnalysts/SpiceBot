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
gifshareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(gifshareddir)
from GifShared import *


@sopel.module.commands('facepalm')
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
    target = spicemanip(bot, triggerargsarray, 0)
    if not target:
        query = "facepalm"
        gif = getGif_all(bot, query, 'random')
        if gif["querysuccess"]:
            osd(bot, trigger.sender, 'say', "%s Result (#%s): %s" % (gif['gifapi'].title(), gif['returnnum'], gif['returnurl']))
        else:
            osd(bot, trigger.sender, 'say', "Hmm...Couldn't find a gif for that!")
    elif target == "major":
        osd(bot, trigger.sender, 'say', "There is not enough facepalm in the world for this")
    elif target == "help":
        osd(bot, trigger.sender, 'say', "Commands: .facepalm help, .facepalm major, or .facepalm")
    else:
        osd(bot, trigger.sender, 'say', "You are really facepalming")
