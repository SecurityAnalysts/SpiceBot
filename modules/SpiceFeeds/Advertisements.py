#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from random import randint
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author jimender2

defaultoptions = [
            "DoubleD recommends these new drapes https://goo.gl/BMTMde", "Spiceduck for spicerex mascot 2k18", "Deathbybandaid is looking for developers for spicebot and spicethings",
            "Upgrade to premium to remove ads", "Selling panties cheap. Msg DoubleD for more info.", "On sale now: tears of an orphan child!", "One-way ticket to Hell just $199",
            "Get a free xboner here", "Extra, Extra, read all about it! A giant Beaver is attacking Canadian people!", "Want to make fast money? Sell Drugs", "Syrup",
            "I love Apple products .... In the trash", "Did you know that I am a female?", "Wanna be friends?", "New Features released every day", "I feel neglected. Use me more. Duel assault in me!"]


hardcoded_not_in_this_chan = ["#spiceworks", "##spicebottest", "#spicebottest"]


@sopel.module.commands('ads', 'advertisements', 'ad', 'advertisement', 'spam')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'ads')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Check to see if there are ads and retrieve one."""
    databasekey = 'ads'
    command = spicemanip(bot, triggerargsarray, 1) or 'get'
    if not sayingscheck(bot, databasekey) and command != "add":
        sayingsmodule(bot, databasekey, defaultoptions, 'initialise')
    message = sayingsmodule(bot, databasekey, triggerargsarray, command)
    osd(bot, trigger.sender, 'say', ["[Advertisement]", message, "[Advertisement]"])


@sopel.module.interval(60)
def advertisement(bot):
    """Get and share random advert at random intervals."""
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

    message = sayingsmodule(bot, databasekey, defaultoptions, 'get') or "Spiceduck for Spiceworks mascot 2k18"

    for channel in bot.channels:
        if channel not in hardcoded_not_in_this_chan:
            channelmodulesarray = get_database_value(bot, channel, 'modules_enabled') or []
            if 'ads' in channelmodulesarray:
                osd(bot, channel, 'say', ["[Advertisement]", message, "[Advertisement]"])


# compare timestamps
def time_since(bot, nick, databasekey):
    """Figure out when the last ad was."""
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))
