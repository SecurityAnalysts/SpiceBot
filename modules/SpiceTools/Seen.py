#!/usr/bin/env python
# coding=utf-8
"""
seen.py - Sopel Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright © 2012, Elad Alfassa <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

http://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import time
import datetime
from sopel.tools import Identifier
from sopel.tools.time import get_timezone, format_time
from sopel.module import commands, rule, priority, thread
import sopel.module
import sys
import os

moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@commands('seen')
def execute_main(bot, trigger):
    """Reports when and where the user was last seen."""
    nick = trigger.group(3)
    if not nick:
        osd(bot, trigger.sender, 'say', ".seen <nick> - Reports when <nick> was last seen.")
    elif nick == bot.nick:
        bot.reply("I'm right here!")
    else:
        timestamp = bot.db.get_nick_value(nick, 'seen_timestamp')
        if timestamp:
            channel = bot.db.get_nick_value(nick, 'seen_channel')
            message = bot.db.get_nick_value(nick, 'seen_message')
            action = bot.db.get_nick_value(nick, 'seen_action')

            tz = get_timezone(bot.db, bot.config, None, trigger.nick,
                              trigger.sender)
            saw = datetime.datetime.utcfromtimestamp(timestamp)
            timestamp = format_time(bot.db, bot.config, tz, trigger.nick,
                                    trigger.sender, saw)

            msg = "I last saw {} at {}".format(nick, timestamp)
            if Identifier(channel) == trigger.sender:
                if action:
                    msg = msg + " in here, doing " + nick + " " + message
                else:
                    msg = msg + " in here, saying " + message
            else:
                msg += " in another channel."
            osd(bot, trigger.sender, 'say', str(trigger.nick) + ': ' + msg)
        else:
            osd(bot, trigger.sender, 'say', "Sorry, I haven't seen {} around.".format(nick))


@thread(False)
@rule('(.*)')
@priority('low')
def note(bot, trigger):
    instigator = trigger.nick
    if not trigger.is_privmsg and instigator != bot.nick:
        bot.db.set_nick_value(trigger.nick, 'seen_timestamp', time.time())
        bot.db.set_nick_value(trigger.nick, 'seen_channel', trigger.sender)
        bot.db.set_nick_value(trigger.nick, 'seen_message', trigger)
        bot.db.set_nick_value(trigger.nick, 'seen_action', 'intent' in trigger.tags)
