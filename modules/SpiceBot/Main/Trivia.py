#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import urllib2
import json

moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('trivia')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'triva')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    category, type, question, answer = getQuestion()
    osd(bot, trigger.sender, 'say', "Category: " + category + " Type: " + type + " Question: " + question)


def getQuestion():
    url = 'https://opentdb.com/api.php?amount=1'
    data = json.loads(urllib2.urlopen(url).read())
    results = str(data['results'])
    a = results.split(',')
    category = a[0]
    type = a[1]
    question = a[2]
    answer = a[4]
    return category, type, question, answer
