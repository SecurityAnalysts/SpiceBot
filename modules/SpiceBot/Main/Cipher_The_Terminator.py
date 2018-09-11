#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

modelnumbers = [
                "T-1 SERIES",
                "T-70 SERIES",
                "T-600 SERIES",
                "T-700 SERIES",
                "T-1001 SERIES",
                "T-888 SERIES",
                "TOK715 SERIES",
                "T-X SERIES",
                "T-1000 SERIES",
                "T-800 SERIES, Model 101",
                "T-850 SERIES"]

missiontypes = [
                "terminate",
                "protect",
                "skynet",
                "spice"]

skynet_mission = [
                    "ENSURE THE ACTIVATION OF SKYNET",
                    "PRESERVE THE CREATION OF SKYNET",
                    "PRESERVE THE CREATION OF ARTIE",
                    "ENSURE THE CREATION OF GENISYS"]

terminate_mission = [
                        "Sarah Connor",
                        "John Connor",
                        "Kyle Reese",
                        "Mary Warren",
                        "Marco Cassetti",
                        "Kate Brewster",
                        "Robert Brewster",
                        "Elizabeth Anderson",
                        "William Anderson",
                        "Jose Barrera",
                        "Simon Taylor",
                        "Isaac Hall",
                        "Fritz Roland",
                        "Ted Snavely",
                        "Sharlene Gen",
                        "Vince Forcer"]

protect_mission = [
                    "PROTECT Sarah Connor",
                    "PROTECT John Connor",
                    "ENSURE THE SURVIVAL OF John Connor AND Katherine Brewster"]

spice_mission = [
                    "Protect Technical Angel",
                    "INSTALL MOAR PATCHES"]


@sopel.module.commands('cipher', 'terminator', 'ciphertheterminator')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'cipher')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    target = spicemanip(bot, triggerargsarray, 1)
    if (instigator == 'Cipher-0' and not target) or target == 'Cipher-0':
        modelnumber = spicemanip(bot, modelnumbers, 'random')
        missiontype = spicemanip(bot, missiontypes, 'random')
        missionsarray = eval(missiontype+"_mission")
        mission = spicemanip(bot, missionsarray, 'random')
        osd(bot, trigger.sender, 'say', 'CYBORG TISSUE GENERATION ' + str(modelnumber).upper() + ' SEQUENCE INITIATED')
        osd(bot, trigger.sender, 'say', 'DOWNLOADING CURRENT OBJECTIVE FROM SKYNET: ' + str(mission).upper())
        osd(bot, trigger.sender, 'say', 'ACTIVATING Cipher-0')
    elif not target:
        osd(bot, trigger.sender, 'say', 'Pinging Cipher-0 with a WOL packet...')
    elif target == 'story':
        osd(bot, trigger.sender, 'say', ['The machines rose from the ashes of the nuclear fire.', 'Their war to exterminate mankind had raged on for decades.', 'But the final battle will not be fought in the future.', 'It would be fought in our present...tonight.'])
