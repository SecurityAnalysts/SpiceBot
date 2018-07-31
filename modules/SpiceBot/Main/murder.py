#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

databasekey = 'murder'

# author jimender2


@sopel.module.commands('murder', 'moida')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'murder')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender

    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    if command == "add":
        if inputstring not in existingarray:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            message = "Added to database."
            osd(bot, trigger.sender, 'say', message)
        else:
            message = "That response is already in the database."
            osd(bot, trigger.sender, 'say', message)
    elif command == "remove":
        if inputstring not in existingarray:
            message = "That response was not found in the database."
            osd(bot, trigger.sender, 'say', message)
        else:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'del')
            message = "Removed from database."
            osd(bot, trigger.sender, 'say', message)
    elif command == "count":
        messagecount = len(existingarray)
        message = "There are currently " + str(messagecount) + " responses for that in the database."
        osd(bot, trigger.sender, 'say', message)
    elif command == "last":
        message = get_trigger_arg(bot, existingarray, "last")
        osd(bot, trigger.sender, 'say', message)
    elif command in ["crows", 'crow']:
        rand = random.randint(1, 5)
        if rand == 1:
            allUsers = [u.lower() for u in bot.users]
            user = get_trigger_arg(bot, allUsers, "random") or 'spicebot'
            osd(bot, trigger.sender, 'say', "A murder of Crows swarms the room and carries " + user + " off.")
        elif rand == 2:
            allUsers = [u.lower() for u in bot.users]
            user = get_trigger_arg(bot, allUsers, "random") or 'spicebot'
            osd(bot, trigger.sender, 'say', "A Crow flys down and pecks " + user + "s eyeballs out of their sockets.")
        else:
            osd(bot, trigger.sender, 'say', "A Murder of Crows swarms the room looking for dead bodies.")
        return

    # if all is fine
    else:
        weapontype = get_trigger_arg(bot, existingarray, "random") or ''
        if weapontype == '':
            weapontype = "gun"
        target = get_trigger_arg(bot, triggerargsarray, 1)
        reason = get_trigger_arg(bot, triggerargsarray, '2+')
        msg = "a " + weapontype

        # No target specified
        if not target:
            osd(bot, trigger.sender, 'say', "Who/what would you like to murder?")

        # Cannot kill spicebot
        elif target == bot.nick:
            osd(bot, trigger.sender, 'say', "You cannot kill a nonliving entity")

        # Cannot kill self
        elif target == instigator:
            message = "Killing yourself would be suicide, " + instigator + ", not murder. Idiot."
            osd(bot, trigger.sender, 'say', message)

        # Target is fine
        else:
            if not reason:
                message = instigator + " murders " + target + " with " + msg + "."
                osd(bot, trigger.sender, 'say', message)
            else:
                message = instigator + " murders " + target + " with " + msg + " for " + reason + "."
                osd(bot, trigger.sender, 'say', message)


def get_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value
