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

# author deathbybandaid


@sopel.module.commands('rg', 'redgreen')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'rg')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    redgreenlist = [
                    "The handyman's secret weapon, duct tape.",
                    "If it ain't broke, you're not trying.",
                    "If the women don't find you handsome, they should at least find you handy.",
                    "Keep your stick on the ice.",
                    "Remember, I'm pulling for you. We're all in this together.",
                    "Quando omni flunkus, moritati.",
                    "I'm a man, but I can change, If I have to, I guess."
                    ]
    redorgreen = get_trigger_arg(bot, redgreenlist, 'random')
    osd(bot, trigger.sender, 'say', redorgreen)
