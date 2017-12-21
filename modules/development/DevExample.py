#!/usr/bin/env python
# coding=utf-8
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('devexample')
def mainfunction(bot, trigger):
    execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    bot.notice("This is to help the dev team understand values.", trigger.nick)
    bot.notice("Trigger.nick: " + trigger.nick, trigger.nick)
    args = ''
    for arg in trigger.args:
        args = str(args) + ', '
    args[:-2]
    bot.notice("Trigger.args: [" + args + ']', trigger.nick)
    
