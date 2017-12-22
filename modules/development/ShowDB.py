#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sopel
from sopel import module, tools
import random
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('dbshow')
def mainfunction(bot, trigger):
    triggerargsarray = spicebot_prerun(bot, trigger)
    execute_main(bot, triggerargsarray)
    
def execute_main(bot, triggerargsarray):
    nick = get_trigger_arg(triggerargsarray, 1)
    bot.say("nick: " + nick)
    dbkey = get_trigger_arg(triggerargsarray, 2)
    bot.say("dbkey: " + dbkey)
    dbresult = get_database_value(bot, 
    #get_database_value(bot, nick, databasekey):
