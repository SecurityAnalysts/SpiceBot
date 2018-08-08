#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2

vehicalType = ["ford f150", "toyota corrola", "Kia Ultima", "shermin tank", "walking"]

maximumHealth = ["100", "90", "50", "1000", "1"]


@sopel.module.commands('race')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'race')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    # setting up variables
    osd(bot, trigger.sender, 'say', "")
    instigator = trigger.nick
    command = get_trigger_arg(bot, triggerargsarray, 1)

    if command == "help":
        test
    elif command == "track":
        test
    elif command == "location":
        test
    elif command == "practice":
        test
    elif command == "random":
        target = randomUser(bot, botcom, instigator)
        race(bot, botcom, target, instigator, trigger)
    else:
        target = command
        # get the opposing person
        targetcheck = easytargetcheck(bot, botcom, target, instigator)
        if targetcheck == "instigator":
            osd(bot, trigger.sender, 'say', "Sorry dude. You cant race yourself.")
        elif targetcheck == "bot":
            osd(bot, trigger.sender, 'say', "I would let you race me but I am under Asimov's laws. Your feelings would be crushed by my winningness")
        elif targetcheck == "false":
            osd(bot, trigger.sender, 'say', "Dude, You cant race your imaginary friend ")
        elif targetcheck == "offline":
            osd(bot, trigger.sender, 'say', "You cannot race someone that is offline")
        elif targetcheck == "online":
            test
        else:
            osd(bot, trigger.sender, 'say', "You cannot race someone that I have never seen!")


def race(bot, botcom, target, instigator, trigger):
    osd(bot, trigger.sender, 'say', instigator + " vs. " + str(target))
    targetVehical, targetMaxHealth = pickVehical(bot, botcom, target)
    instigatorVehical, instigatorMaxHealth = pickVehical(bot, botcom, instigator)
    osd(bot, trigger.sender, 'say', instigator + " is driving a " + instigatorVehical)
    osd(bot, trigger.sender, 'say', target + " is driving a " + targetVehical)
    targetVehicalStats = random.randint(1, targetMaxHealth)
    instigatorVehicalStats = random.randint(1, instigatorMaxHealth)
    targetVehicalStats = damage(targetVehical)
    instigatorVehicalStats = damage(instigatorVehical)
    if targetVehicalStats  <= 0:
        osd(bot, trigger.sender, 'say', target + " crashes their " + targetVehical)
    if instigatorVehicalStats  <= 0:
        osd(bot, trigger.sender, 'say', instigator + " crashes their " + instigatorVehical)
    winner


def damage(vehical):
    damage = random.randint(-100, 100)
    vehical = vehical - damage
    return vehical


def pickVehical():
    rand = random.randint(1,5)
    vehical = get_trigger_arg(bot, vehicalType, rand) or 'walkin'
    maxHealth = get_trigger_arg(bot, maximumHealth, rand) or '1'
    return vehical, maxHealth


def randomUser(bot, botcom, instigator):
    allUsers = [u.lower() for u in bot.users]
    user = get_trigger_arg(bot, allUsers, "random") or 'spicebot'
    return user


def userCheck(bot, botcom, target, instigator):
    target = command
    # get the opposing person
    targetcheck = easytargetcheck(bot, botcom, target, instigator)
    if targetcheck == "instigator":
        osd(bot, trigger.sender, 'say', "Sorry dude. You cant race yourself.")
    elif targetcheck == "bot":
        osd(bot, trigger.sender, 'say', "I would let you race me but I am under Asimov's laws. Your feelings would be crushed by my winningness")
    elif targetcheck == "false":
        osd(bot, trigger.sender, 'say', "Dude, You cant race your imaginary friend ")
    elif targetcheck == "offline":
        osd(bot, trigger.sender, 'say', "You cannot race someone that is offline")
    elif targetcheck == "online":
        test
    else:
        osd(bot, trigger.sender, 'say', "You cannot race someone that I have never seen!")
