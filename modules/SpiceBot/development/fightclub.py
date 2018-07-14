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

rules = ["The first rule of Fight Club is: You do not talk about Fight Club.",
         "The second rule of Fight Club is: You DO NOT TALK ABOUT FIGHT CLUB!",
         "Third rule of Fight Club: Someone yells stop, goes limp, taps out, the fight is over.",
         "Fourth rule: only two guys to a fight.",
         "Fifth rule: one fight at a time, fellas.",
         "Sixth rule: no shirts, no shoes.",
         "Seventh rule: Fights will go on as long as they have to.",
         "And the eighth and final rule: If this is your first night at Fight Club, you have to fight."]


@sopel.module.commands('fightclub')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, fightclub)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):
    message = get_trigger_arg(bot, replies, 'random')
    onscreentext(bot,['say'],message)
