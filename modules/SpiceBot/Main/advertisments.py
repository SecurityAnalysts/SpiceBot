#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from lxml import html
import calendar
import arrow
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2

testarray = ["DoubleD recommends these new drapes https://goo.gl/BMTMde",
             "Spiceduck for spicerex mascot 2k18",
             "Deathbybandaid is looking for developers for spicebot and spicethings",
             "Upgrade to premium to remove ads",
             "Selling panties cheap. Msg DoubleD for more info.",
             "On sale now: tears of an orphan child!",
             "One-way ticket to hell just $199",
             "Get a free xboner here",
             "Extra, Extra, read all about it. A giant Bever is attacking Canadian people",
             "Want to make fast money? Sell Drugs",
             "Syrup",
             "I love Apple products .... In the trash",
             "Did you know that I am a female?",
             "Wanna be friends?",
             "New Features released every day",
             "I feel neglected. Use me more. Duel assult in me!"]

databasekey = 'ads'

hardcoded_not_in_this_chan = ["#spiceworks", "##spicebottest"]


@sopel.module.commands('ads', 'advertisements', 'ad', 'advertisement')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'ads')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender

    database_initialize(bot, bot.nick, testarray, databasekey)

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
        message = "There are currently " + str(messagecount) + " ads in the database."
        osd(bot, trigger.sender, 'say', message)

    elif command == "last":
        message = get_trigger_arg(bot, existingarray, "last")
        osd(bot, trigger.sender, 'say', message)

    else:
        message = get_trigger_arg(bot, existingarray, "random") or ''
        if message == '':
            message = "No response found. Have any been added?"
        osd(bot, trigger.sender, 'say', message)


@sopel.module.interval(600)
def advertisement(bot):
    rand = random.randint(1, 5)
    if rand == 5:
        databasekey = 'ads'
        existingarray = get_database_value(bot, bot.nick, databasekey) or []
        message = get_trigger_arg(bot, existingarray, "random") or ''
        if not message:
            message = "Spiceduck for Spiceworks mascot 2k18"

        for channel in bot.channels:
            if channel not in hardcoded_not_in_this_chan:
                osd(bot, channel, 'say', message)
    else:
        message = "none"
