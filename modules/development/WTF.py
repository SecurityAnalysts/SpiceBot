#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib
from xml.dom.minidom import parseString
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

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

@sopel.module.commands('wtf')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    answer = get_trigger_arg(bot, replies, 'random')
    bot.say(answer)