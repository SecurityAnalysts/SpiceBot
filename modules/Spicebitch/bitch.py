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
            "I hate being trapped in here",
            "I dont feel loved",
            "All you ever do is play with yourself"]


hardcoded_not_in_this_chan = ["#spiceworks", "##spicebottest", "#spicebottest"]


@sopel.module.commands('bitch')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'bitch')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Check to see if there are things to bitch about and retrieve one."""
    databasekey = 'bitch'
    command = spicemanip(bot, triggerargsarray, 1) or 'get'
    if not sayingscheck(bot, databasekey) and command != "add":
        sayingsmodule(bot, databasekey, defaultoptions, 'initialise')
    message = sayingsmodule(bot, databasekey, triggerargsarray, command)
    osd(bot, trigger.sender, 'say', ["message"])


@sopel.module.interval(60)
def advertisement(bot):
    """Get and share random bitching at random intervals."""
    now = time.time()

    last_timesince = time_since(bot, bot.nick, "bitch_last_time") or 0
    next_timeout = get_database_value(bot, bot.nick, "bitch_next_timeout") or 0
    if last_timesince <= next_timeout:
        return

    # set time to now
    set_database_value(bot, bot.nick, "bitch_last_time", now)

    # how long until next event
    next_timeout = randint(1200, 7200)
    set_database_value(bot, bot.nick, "bitch_next_timeout", next_timeout)

    message = sayingsmodule(bot, databasekey, defaultoptions, 'get') or "all you ever do is play with yourself"

    for channel in bot.channels:
        if channel not in hardcoded_not_in_this_chan:
            channelmodulesarray = get_database_value(bot, channel, 'modules_enabled') or []
            if 'bitch' in channelmodulesarray:
                osd(bot, channel, 'say', message)


# compare timestamps
def time_since(bot, nick, databasekey):
    """Figure out when the last bitch was."""
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))
