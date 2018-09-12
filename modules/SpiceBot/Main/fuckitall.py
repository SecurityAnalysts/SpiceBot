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

# author SniperClif


@sopel.module.commands('fuckitall', 'fia')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'fuckitall')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    message = ["Find that caring has made you a gasping ball of stress?",
               "Tired of giving a flying fuck about the next chucklehead that decides you need to fix their problems?",
               "Wish the whole world would eat 3 handfuls of Sugar-Free Haribo Gummy Bears so they wouldn't be so full of shit anymore?",
               "Try all new and improved Fuck-It-Allᵀᴹ",
               "With Fuck-It-Allᵀᴹs patented formula of THC, alcohol, and traces of MDMA, the whole world will feel great!"
               ]
    osd(bot, trigger.sender, 'say', message)
    message = ["Side effects may include:",
               "Anal leakage, penile shrinkage, halitosis, HIV, GhonoherpesyphilAIDS, and a serious case of homicidal rage.",
               "Please see your Dr. if you experience a raging erection for more than 4 hours or wake up from a rage induced blackout in the middle of rush hour traffic with the blood of your enemies smeared across you bare chest."
               ]
    osd(bot, trigger.sender, 'say', message)
