#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('usage','moduleusage','totalusage')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    # # Initial ARGS
    # triggerargsarray = create_args_array(trigger.group(3))
    triggerargsarray = get_trigger_arg(bot, trigger.group(3), 'create')
    # commandused = get_trigger_arg(bot, triggerargsarray, 0)
    commandused = trigger.group(1)
    target = get_trigger_arg(bot, triggerargsarray, 1)
    instigator = trigger.nick
    GITWIKIURL = 'https://github.com/SpiceBot/sopel-modules/wiki/Usage'
    # # Variable ARGS
    moduletocheck = get_trigger_arg(bot, triggerargsarray, 1) or instigator
    checktarget = get_trigger_arg(bot, triggerargsarray, 2)
    usagefor = ''
    querytype = 'specific'
    counter = 1

    if moduletocheck == 'channel':
        querytype = 'invalidmodule'
        counter = 0
    if moduletocheck == 'help':
        querytype = 'help'
        counter = 0

    if counter == 1:
        if moduletocheck.lower() in [u.lower() for u in bot.users]:
            querytype = 'user'
            usagefor = str(moduletocheck)
            if not checktarget:
                checktarget = 'total'
        elif moduletocheck.lower() not in [u.lower() for u in bot.users]:
            if checktarget:
                if checktarget == 'channel':
                    usagefor = trigger.sender
                else:
                    usagefor = checktarget
            elif not checktarget:
                usagefor = str(trigger.nick)

        count = get_database_value(bot, usagefor, moduletocheck+"usage")

        if querytype == 'user':
            if count == 0:
                message = str('It appears that ' + usagefor + ' has not run any commands at all.')
            elif count == 1:
                message = str(usagefor + ' has run a total of ' + str(count) + ' commands.')
            else:
                message = str(usagefor + ' has run a total of ' + str(count) + ' commands.')
        else:
            if count == 0:
                message = str('It appears that ' + usagefor + ' has not run ' + moduletocheck + ' at all.')
            elif count == 1:
                message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' time.')
            else:
                message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' times.')
    elif counter == 0:
        if querytype == 'invalidmodule':
            message = str("I'm sorry, but that's not a valid module to check.")
        if querytype == 'help':
            message = str('A wiki page for this is in progress.')
        else:
            message = str('An error occurred. Please try again later.')
    osd(bot, trigger.sender, 'say', message)
