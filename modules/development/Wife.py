#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

replies = ["No.","Buy me jewellery!","You haven't done enough around the house lately.","Are you even listening to me?",
"My mother is coming to stay. You're okay with that, right?","Maybe you should ask your whore, Linda.",
"Would you like a blowjob? Oh, sure, you heard that one fine. Just making sure you're actually listening.",
"Hi honey. How was your day?","Can I help with the bills this month?","Do what you want to.",
"No really, it's fine, go fishing with the guys."]

@sopel.module.commands('wife')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    answer = get_trigger_arg(replies, 'random')
    bot.say(answer)
