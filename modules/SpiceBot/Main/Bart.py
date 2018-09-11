#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib
from xml.dom.minidom import parseString
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

replies = ["Eat My Shorts!",
           "Don't Have a Cow, Man!",
           "¡Ay, caramba!",
           "Get Bent.",
           "I'm Bart Simpson, Who the Hell are You?",
           "Cowabunga!",
           "I Didn't Do It!",
           "Nobody saw me do it. You can't prove anything!",
           "Aw, Man!",
           "Aw, Geez!",
           "Whoa, mama!",
           "Eep!"]


@sopel.module.commands('bart')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'bart')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    answer = get_trigger_arg(bot, replies, 'random')
    osd(bot, trigger.sender, 'action', answer)
