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


@sopel.module.commands('quote')
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
    quote = getQuote()
    if quote:
        osd(bot, trigger.sender, 'say', quote)
    else:
        osd(bot, trigger.sender, 'say', 'There is nothing to quote - Abraham Lincoln')


def getQuote():
    url = 'https://talaikis.com/api/quotes/random/'
    try:
        page = requests.get(url)
        result = page.content
        jsonquote = json.loads(result)
        # quote = '"' + jsonquote['content'] + '" - ' + jsonquote['title']
        quote = '"' + jsonquote['quote'] + '" - ' + jsonquote['author']
    except:
        quote = "No quote for you."
    return quote
