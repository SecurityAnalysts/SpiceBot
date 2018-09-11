#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sopel
import random
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

eightarray = [
                "Only on Tuesdays",
                "42",
                "Not so sure",
                "Negative",
                "Could be",
                "Unclear, ask again",
                "Yes",
                "No",
                "Possible, but not probable",
                "Most likely",
                "Absolutely not",
                "I see good things happening",
                "Never",
                "Outlook is good",
                "It is certain",
                "It is decidedly so",
                "Without a doubt",
                "Yes definitely",
                "You may rely on it",
                "As I see it yes",
                "Most likely",
                "Outlook good",
                "Yes",
                "Signs point to yes",
                "Reply hazy try again",
                "Ask again later",
                "Better not tell you now",
                "Cannot predict now",
                "Concentrate and ask again",
                "Don't count on it",
                "My reply is no",
                "God says no",
                "Very doubtful",
                "Outlook not so good"]


@sopel.module.commands('8ball')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "Let me dig deep into the waters of life, and find your answer")
    reply = get_trigger_arg(bot, eightarray, 'random')
    osd(bot, trigger.sender, 'say', reply)
