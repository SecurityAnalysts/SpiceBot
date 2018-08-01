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
from random import randint
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
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
             "I feel neglected. Use me more. Duel assualt in me!"]


hardcoded_not_in_this_chan = ["#spiceworks", "##spicebottest"]


@sopel.module.commands('ads', 'advertisements', 'ad', 'advertisement')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'ads')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender

    # database_initialize(bot, bot.nick, testarray, 'ads')
    existingarray = get_database_value(bot, bot.nick, 'ads') or []
    if existingarray == []:
        adjust_database_array(bot, bot.nick, testarray, 'ads', 'add')
        existingarray = testarray

    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')

    if command == "add":
        if inputstring not in existingarray:
            adjust_database_array(bot, bot.nick, inputstring, 'ads', 'add')
            osd(bot, trigger.sender, 'say', "Added to database.")
        else:
            osd(bot, trigger.sender, 'say', "That response is already in the database.")
        return

    if command == "remove":
        if inputstring not in existingarray:
            osd(bot, trigger.sender, 'say', "That response was not found in the database.")
        else:
            adjust_database_array(bot, bot.nick, inputstring, 'ads', 'del')
            osd(bot, trigger.sender, 'say', "Removed from database.")
        return

    if command == "count":
        osd(bot, trigger.sender, 'say', "There are currently " + str(len(existingarray)) + " ads in the database.")
        return

    if command == "last":
        osd(bot, trigger.sender, 'say', ["[Advertisement]", get_trigger_arg(bot, existingarray, "last"), "[Advertisement]"])
        return

    message = get_trigger_arg(bot, existingarray, "random") or "No response found. Have any been added?"
    osd(bot, trigger.sender, 'say', ["[Advertisement]", message, "[Advertisement]"])


@sopel.module.interval(60)
def advertisement(bot):

    now = time.time()

    last_timesince = time_since(bot, bot.nick, "ads_last_time") or 0
    next_timeout = get_database_value(bot, bot.nick, "ads_next_timeout") or 0
    if last_timesince <= next_timeout:
        return

    # set time to now
    set_database_value(bot, bot.nick, "ads_last_time", now)

    # how long until next event
    next_timeout = randint(1200, 7200)
    set_database_value(bot, bot.nick, "ads_next_timeout", next_timeout)

    existingarray = get_database_value(bot, bot.nick, 'ads') or []
    message = get_trigger_arg(bot, existingarray, "random") or "Spiceduck for Spiceworks mascot 2k18"

    for channel in bot.channels:
        if channel not in hardcoded_not_in_this_chan:
            channelmodulesarray = get_database_value(bot, channel, 'modules_enabled') or []
            if 'ads' in channelmodulesarray:
                osd(bot, channel, 'say', ["[Advertisement]", message, "[Advertisement]"])


# compare timestamps
def time_since(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))
