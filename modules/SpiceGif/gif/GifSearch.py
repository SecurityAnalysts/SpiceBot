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
gifshareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(gifshareddir)
from BotShared import *
from GifShared import *


@sopel.module.commands('gif')
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
    query = spicemanip(bot, triggerargsarray, 0)

    gifapiresults = []
    for currentapi in valid_gif_api:
        gifdict = eval("getGif_" + currentapi + "(bot, query, 'random')")
        if gifdict["querysuccess"]:
            gifapiresults.append(gifdict)

    if gifapiresults == []:
        osd(bot, trigger.sender, 'say',  'No Results were found for ' + query + 'in any api')
        return

    gifdict = spicemanip(bot, gifapiresults, 'random')

    osd(bot, trigger.sender, 'say',  gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"]))
