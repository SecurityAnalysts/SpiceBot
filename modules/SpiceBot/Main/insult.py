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

# author jimender2

insalton = ["lazy",
            "stupid",
            "insecure",
            "idiotic",
            "slimy",
            "slutty",
            "smelly",
            "pompous",
            "communist"
            "dicknose",
            "pie-eating",
            "racist",
            "elitist",
            "white trash",
            "drug-loving",
            "butterface",
            "tone deaf",
            "ugly",
            "creepy"]

insalttw = ["douche",
            "ass",
            "turd",
            "rectum",
            "butt",
            "cock",
            "shit",
            "crotch",
            "bitch",
            "turd",
            "prick",
            "slut",
            "taint",
            "fuck",
            "dick",
            "boner",
            "shart",
            "nut",
            "sphincter"]

insaltth = ["pilot",
            "canoe",
            "captain",
            "pirate",
            "hammer",
            "knob",
            "box",
            "jockey",
            "nazi",
            "waffle",
            "goblin",
            "blossum",
            "biscuit",
            "clown",
            "socket",
            "monster",
            "hound",
            "dragon",
            "balloon"]


@sopel.module.commands('insult')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'insult')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    answer1 = spicemanip(bot, insalton, 'random')
    answer2 = spicemanip(bot, insalttw, 'random')
    answer3 = spicemanip(bot, insaltth, 'random')

    message = "You are a " + answer1 + " " + answer2 + " " + answer3 + "."
    osd(bot, trigger.sender, 'say', message)
