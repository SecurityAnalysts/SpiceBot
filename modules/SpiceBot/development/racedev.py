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

vehicleType = ["ford f150", "toyota corrola", "Kia Ultima", "shermin tank", "walking"]

maximumHealth = ["100", "90", "50", "1000", "1"]


@sopel.module.commands('racedev')
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
        osd(bot, trigger.sender, 'say', "For right now do .race random or .race person to race")
    elif command == "track":
        osd(bot, trigger.sender, 'say', "For right now this is not set up yet.")
    elif command == "location":
        osd(bot, trigger.sender, 'say', "For right now this is not set up yet.")
    elif command == "practice":
        osd(bot, trigger.sender, 'say', "For right now this is not set up yet.")
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
            race(bot, botcom, target, instigator, trigger)
        else:
            osd(bot, trigger.sender, 'say', "You cannot race someone that I have never seen!")


def race(bot, botcom, target, instigator, trigger):
    osd(bot, trigger.sender, 'say', instigator + " vs. " + str(target))
    targetVehicle, targetMaxHealth = pickVehicle(bot, botcom, target)
    instigatorVehicle, instigatorMaxHealth = pickVehicle(bot, botcom, instigator)
    osd(bot, trigger.sender, 'say', instigator + " is driving a " + instigatorVehicle)
    osd(bot, trigger.sender, 'say', target + " is driving a " + targetVehicle)
    targetVehicleStats = random.randint(1, targetMaxHealth)
    instigatorVehicleStats = random.randint(1, instigatorMaxHealth)
    targetVehicleStats = damage(targetVehicleStats)
    instigatorVehicleStats = damage(instigatorVehicleStats)
    if targetVehicleStats <= 0:
        osd(bot, trigger.sender, 'say', target + " crashes their " + targetVehicle)
    if instigatorVehicleStats <= 0:
        osd(bot, trigger.sender, 'say', instigator + " crashes their " + instigatorVehicle)
    if targetVehicleStats >= 0 and instigatorVehicleStats >= 0:
        if targetVehicleStats > instigatorVehicleStats:
            osd(bot, trigger.sender, 'say', target + " is the winner of the race")
            increaseWin(bot, botcom, target)
            resetWin(bot, botcom, instigator)
        elif targetVehicleStats < instigatorVehicleStats:
            osd(bot, trigger.sender, 'say', instigator + " is the winner of the race")
            increaseWin(bot, botcom, instigator)
            resetWin(bot, botcom, target)
        else:
            osd(bot, trigger.sender, 'say', target + " and " + instigator + " end the race in a tie.")
    elif targetVehicleStats < 0:
        osd(bot, trigger.sender, 'say', instigator + " wins the race")
        increaseWin(bot, botcom, instigator)
        resetWin(bot, botcom, target)
    elif instigatorVehicleStats < 0:
        osd(bot, trigger.sender, 'say', target + " wins the race")
        increaseWin(bot, botcom, target)
        resetWin(bot, botcom, instigator)


def resetWin(bot, botcom, person):
    databasekey = "devRaceStreak"
    set_database_value(bot, person, databasekey, 0)


def increaseWin(bot, botcom, person):
    databasekey = "devRaceStreak"
    wins = get_database_value(bot, person, databasekey) or 0
    wins = int(wins) + 1
    set_database_value(bot, person, databasekey, wins)


def getWins(bot, botcom, trigger, person):
    databasekey = "devRaceStreak"
    wins = get_database_value(bot, person, databasekey) or 0
    osd(bot, trigger.sender, 'say', person + " has a streak of " + str(wins) + " wins")


def damage(vehicleStats):
    damage = random.randint(0, 200) - 100
    vehicleStats = vehicleStats - damage
    return vehicleStats


def pickVehicle(bot, botcom, target):
    rand = random.randint(1,5)
    vehicle = get_trigger_arg(bot, vehicleType, rand) or 'walkin'
    maxHealth = get_trigger_arg(bot, maximumHealth, rand)
    maxHealth = int(maxHealth)
    return vehicle, maxHealth


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
