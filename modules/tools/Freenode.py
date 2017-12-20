#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
from sopel.module import OP

@sopel.module.commands('msg', 'nick', 'attach', 'server', 'join', 'whois', 'me', 'ban')
def execute_main(bot, trigger):
    for c in bot.channels:
        channel = c
    operatorarray = []
    for u in bot.channels[channel.lower()].users:
        if bot.privileges[channel.lower()][u] == OP:
            operatorarray.append(u)
    if trigger.startswith('.ban') and trigger.nick.lower() not in operatorarray:
        bot.say("You have no power here.")
    else:
        trigger = trigger.replace('.', '/', 1)
        bot.say('"I believe you wanted to say ' + trigger)
                
