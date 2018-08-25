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


def execute_main(bot, trigger):
    osd(bot, trigger.sender, 'say', "This is deathbybandaid's test module")

    command = get_trigger_arg(bot, triggerargsarray, 1)

    # RPG dynamic Class
    rpg = class_create('rpg')
    rpg.default = 'rpg'

    if not command or command == 'get':
        coin = get_rpg_user_dict(bot, rpg, bot.nick, 'coin')
        bot.say(str(coin))
    elif command == 'set':
        set_rpg_user_dict(bot, rpg, bot.nick, 'coin', 20)
    elif command == 'reset':
        reset_rpg_user_dict(bot, rpg, bot.nick, 'coin')
    elif command == 'adjustup':
        adjust_rpg_user_dict(bot, rpg, bot.nick, 'coin', 20)
    elif command == 'adjustdown':
        adjust_rpg_user_dict(bot, rpg, bot.nick, 'coin', -20)

    """
    End of all of the rpg stuff after error handling
    """

    save_rpg_user_dict(bot, rpg)


# Database Users
def get_rpg_user_dict(bot, dclass, nick, dictkey):

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
def set_rpg_user_dict(bot, dclass, nick, dictkey, value):
    currentvalue = get_rpg_user_dict(bot, dclass, nick, dictkey)
    nickdict = eval('dclass.userdb.' + nick)
    nickdict[dictkey] = value


# reset a value
def reset_rpg_user_dict(bot, dclass, nick, dictkey):
    currentvalue = get_rpg_user_dict(bot, dclass, nick, dictkey)
    nickdict = eval('dclass.userdb.' + nick)
    if dictkey in nickdict:
        del nickdict[dictkey]


# add or subtract from current value
def adjust_rpg_user_dict(bot, dclass, nick, dictkey, value):
    oldvalue = get_rpg_user_dict(bot, dclass, nick, dictkey)
    nickdict = eval('dclass.userdb.' + nick)
    nickdict[dictkey] = float(oldvalue) + float(value)


# Save all database users in list
def save_rpg_user_dict(bot, dclass):

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
