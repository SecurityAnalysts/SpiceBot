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

fishtypes = ["Pike", "Carp", "Marlin", "Trout", "Cod", "Anchovy", "Venezuelan Beaverfish",
             "fish", "Ocean Sunfish", "blobfish", "red-bellied pacu", "oyster toadfish",
             "Halichoeres bivittatus (slippery dick)", "Humuhumunukunukuāpuaʻa", "Giant Goliath Tiger Fish",
             "Red-lipped batfish", "suckermouth catfish", "Northern red snapper", "Tasseled Wobbegong", "Sarcastic fringehead",
             "Collared carpetshark", "Naked-back knifefish"]
vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')


@sopel.module.commands('fish', 'slap')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'fish')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    reason = get_trigger_arg(bot, triggerargsarray, '2+')
    message = "Whoops, something went wrong."
    fishtype = get_trigger_arg(bot, fishtypes, 'random')
    fishmsg = "a " + fishtype
    # Vowel awareness
    if fishtype.startswith(vowels):
        fishmsg = "an " + fishtype

    # No target specified
    if not target:
        message = "You haven't told me who or what you want to slap, you moron."

    # Can't slap the bot
    if target == bot.nick:
        message = "Get fucked, that's not gonna happen."

    # Target is bear
    elif target.startswith("bear"):
        if not reason:
            message = trigger.nick + " feeds " + target + " a tasty " + fishtype + "."
        else:
            if reason.startswith('for ') or reason.startswith('because ') or reason.startswith('cause '):
                message = trigger.nick + " feeds " + target + " a tasty " + fishtype + " " + reason + "."
            else:
                message = trigger.nick + " feeds " + target + " a tasty " + fishtype + " for " + reason + "."

    # Target is fine
    else:
        if not reason:
            message = trigger.nick + " slaps " + target + " with " + fishmsg + "."
        else:
            if reason.startswith('for ') or reason.startswith('because ') or reason.startswith('cause '):
                message = trigger.nick + " slaps " + target + " with " + fishmsg + " " + reason + "."
            else:
                message = trigger.nick + " slaps " + target + " with " + fishmsg + " for " + reason + "."

    osd(bot, trigger.sender, 'say', message)
