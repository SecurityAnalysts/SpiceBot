#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sopel
from sopel import module, tools
import random
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('webmd', 'webmdadd', 'webmddel')
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
    commandtrimmed = trigger.group(1)
    commandtrimmed = str(commandtrimmed.split("webmd", 1)[1])
    webmd = get_webmd(bot)
    if commandtrimmed == '':
        target = trigger.group(3) or trigger.nick
        responses = [
                    "has died from",
                    "is being treated for",
                    "is recovering from"]
        reply = random.randint(0, len(responses) - 1)
        condition = str(responses[reply])
        if webmd == []:
            result = "death"
        else:
            resultselected = random.randint(0, len(webmd) - 1)
            result = str(webmd[resultselected])
        conclusion = str(target + ' ' + condition + ' ' + result + '.')
        osd(bot, trigger.sender, 'say', conclusion)
    elif not trigger.group(2):
        osd(bot, trigger.sender, 'say', "What would you like to add/remove?")
    else:
        webmdchange = str(trigger.group(2))
        if commandtrimmed == 'add':
            if webmdchange in webmd:
                osd(bot, trigger.sender, 'say', webmdchange + " is already in the webmd locker.")
                rescan = 'False'
            else:
                webmd.append(webmdchange)
                update_webmd(bot, webmd)
                rescan = 'True'
        elif commandtrimmed == 'del':
            if webmdchange not in webmd:
                osd(bot, trigger.sender, 'say', webmdchange + " is not in the webmd locker.")
                rescan = 'False'
            else:
                webmd.remove(webmdchange)
                update_webmd(bot, webmd)
                rescan = 'True'
        if rescan == 'True':
            webmd = get_webmd(bot)
            if webmdchange in webmd:
                osd(bot, trigger.sender, 'say', webmdchange + " has been added to the webmd locker.")
            else:
                osd(bot, trigger.sender, 'say', webmdchange + ' has been removed from the webmd locker.')


def get_webmd(bot):
    for channel in bot.channels:
        webmd = bot.db.get_nick_value(channel, 'webmd_locker') or []
        return webmd


def update_webmd(bot, webmd):
    for channel in bot.channels:
        bot.db.set_nick_value(channel, 'webmd_locker', webmd)
