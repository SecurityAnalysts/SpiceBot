#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('asimov')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    laws ['may not injure a human being or, through inaction, allow a human being to come to harm.', 'must obey orders given it by human beings except where such orders would conflict with the First Law.', 'must obey orders given it by human beings except where such orders would conflict with the First Law.', 'must protect its own existence as long as such protection does not conflict with the First or Second Law.', 'must comply with all chatroom rules.']
    #bot.action('may not injure a human being or, through inaction, allow a human being to come to harm.')
    #bot.action('must obey orders given it by human beings except where such orders would conflict with the First Law.')
    #bot.action('must protect its own existence as long as such protection does not conflict with the First or Second Law.')
    #bot.action('must comply with all chatroom rules.')
    bot.action(laws)
