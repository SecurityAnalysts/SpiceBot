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

import textwrap
import collections
import json

import requests

from sopel.logger import get_logger
from sopel.module import commands, rule, example, priority


@sopel.module.commands('dbbtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "This is deathbybandaid's test module")

    command = get_trigger_arg(bot, triggerargsarray, 1) or 'get'
    if command in triggerargsarray:
        triggerargsarray.remove(command)

    whatisleft = get_trigger_arg(bot, triggerargsarray, 0)

    # RPG dynamic Class
    rpg = class_create('rpg')
    rpg.default = 'rpg'

    if command == 'get':
        coin = get_user_dict(bot, rpg, bot.nick, 'coin')
        bot.say(str(coin))
    elif command == 'set':
        set_user_dict(bot, rpg, bot.nick, 'coin', 20)
    elif command == 'reset':
        reset_user_dict(bot, rpg, bot.nick, 'coin')
    elif command == 'adjustup':
        adjust_user_dict(bot, rpg, bot.nick, 'coin', 20)
    elif command == 'adjustdown':
        adjust_user_dict(bot, rpg, bot.nick, 'coin', -20)
    elif command == 'viewarray':
        weapons = get_user_dict(bot, rpg, bot.nick, 'weapons')
        bot.say(str(weapons))
    elif command == 'addarray':
        adjust_user_dict_array(bot, rpg, bot.nick, 'weapons', [whatisleft], 'add')
    elif command == 'delarray':
        adjust_user_dict_array(bot, rpg, bot.nick, 'weapons', [whatisleft], 'del')
    else:
        bot.say("invalid command")
        return

    """
    End of all of the rpg stuff after error handling
    """

    save_user_dicts(bot, rpg)
    if command != 'get':
        bot.say("done")


# Database Users
def get_user_dict(bot, dclass, nick, dictkey):

    # check that db list is there
    if not hasattr(dclass, 'userdb'):
        dclass.userdb = class_create('userdblist')
    if not hasattr(dclass.userdb, 'list'):
        dclass.userdb.list = []

    returnvalue = 0

    # check if nick has been pulled from db already
    if nick not in dclass.userdb.list:
        dclass.userdb.list.append(nick)
        nickdict = get_database_value(bot, nick, dclass.default) or dict()
        createuserdict = str("dclass.userdb." + nick + " = nickdict")
        exec(createuserdict)
    else:
        if not hasattr(dclass.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('dclass.userdb.' + nick)

    if dictkey in nickdict.keys():
        returnvalue = nickdict[dictkey]
    else:
        nickdict[dictkey] = 0
        returnvalue = 0

    return returnvalue


# set a value
def set_user_dict(bot, dclass, nick, dictkey, value):
    currentvalue = get_user_dict(bot, dclass, nick, dictkey)
    nickdict = eval('dclass.userdb.' + nick)
    nickdict[dictkey] = value


# reset a value
def reset_user_dict(bot, dclass, nick, dictkey):
    currentvalue = get_user_dict(bot, dclass, nick, dictkey)
    nickdict = eval('dclass.userdb.' + nick)
    if dictkey in nickdict:
        del nickdict[dictkey]


# add or subtract from current value
def adjust_user_dict(bot, dclass, nick, dictkey, value):
    oldvalue = get_user_dict(bot, dclass, nick, dictkey)
    if not str(oldvalue).isdigit():
        oldvalue = 0
    nickdict = eval('dclass.userdb.' + nick)
    nickdict[dictkey] = float(oldvalue) + float(value)


# Save all database users in list
def save_user_dicts(bot, dclass):

    # check that db list is there
    if not hasattr(dclass, 'userdb'):
        dclass.userdb = class_create('userdblist')
    if not hasattr(dclass.userdb, 'list'):
        dclass.userdb.list = []

    for nick in dclass.userdb.list:
        if not hasattr(dclass.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('dclass.userdb.' + nick)
        set_database_value(bot, nick, dclass.default, nickdict)


def adjust_user_dict_array(bot, dclass, nick, dictkey, entries, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    oldvalue = get_user_dict(bot, dclass, nick, dictkey)
    nickdict = eval('dclass.userdb.' + nick)
    if not isinstance(oldvalue, list):
        oldvalue = []
    for x in entries:
        if adjustmentdirection == 'add':
            if x not in oldvalue:
                oldvalue.append(x)
        elif adjustmentdirection == 'del':
            if x in oldvalue:
                oldvalue.remove(x)
    nickdict[dictkey] = oldvalue
