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

databasekey = "bribe"

# author jimender2


@sopel.module.commands('bribe')
def mainfunction(bot, trigger):
    """Checks whether the module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Handles bribing other users."""
    instigator = trigger.nick
    command = get_trigger_arg(bot, triggerargsarray, 1)
    target = get_trigger_arg(bot, triggerargsarray, 1)
    amo = get_database_value(bot, instigator, databasekey) or '0'
    amount = int(amo)
    if command == "accept":
        reset_database_value(bot, instigator, databasekey)
        spicebucks(bot, instigator, "plus", amount)
        if amount == 0:
            osd(bot, trigger.sender, 'action', "There are no bribes for you to accept")
        else:
            message = str(instigator) + " accepted the bribe of $" + str(amount) + "."
            osd(bot, trigger.sender, 'action',  message)
    elif command == "decline":
        message = str(instigator) + " declines a bribe worth $" + str(amount) + "."
        osd(bot, trigger.sender, 'action',  message)
        reset_database_value(bot, instigator, databasekey)
    elif command == "money":
        amount = 1000
        spicebucks(bot, instigator, "plus", amount)
        osd(bot, trigger.sender, 'say', "you got money")

    else:
        if target == instigator:
            osd(bot, trigger.sender, 'action', "Stupid person. You can't bribe yourself")
        elif target == bot.nick:
            osd(bot, trigger.sender, 'action', "Moron. You can't bribe me with money. Try terabytes")
        elif target.lower() in [u.lower() for u in bot.users]:
            balance = bank(bot, instigator)
            money = random.randint(0, balance)
            if money == 0:
                osd(bot, trigger.sender, 'action', instigator + " attempts to bribe " + target + " with $" + str(money) + " but " + target + " wacks them upside the head.")
            elif money == 1:
                osd(bot, trigger.sender, 'action', instigator + " bribes " + target + " with $" + str(money) + " in an unmarked bill.")
            else:
                osd(bot, trigger.sender, 'action', instigator + " bribes " + target + " with $" + str(money) + " in nonsequental, unmarked bills.")
            inputstring = str(money)
            set_database_value(bot, target, databasekey, inputstring)
            spicebucks(bot, instigator, 'minus', money)
        else:
            osd(bot, trigger.sender, 'action', "I'm sorry, I do not know who " + target + " is.")


def bank(bot, nick):
    balance = get_database_value(bot, nick, 'spicebucks_bank') or 0
    return balance


def spicebucks(bot, target, plusminus, amount):
    # command for getting and adding money to account
    success = 'false'
    if type(amount) == int:
        inbank = bank(bot, target)
    if plusminus == 'plus':
        adjust_database_value(bot, target, 'spicebucks_bank', amount)
        success = 'true'
    elif plusminus == 'minus':
        if inbank - amount < 0:
            success = 'false'
        else:
            adjust_database_value(bot, target, 'spicebucks_bank', -amount)
            success = 'true'
    else:
        success = 'false'
    return success


def get_database_value(bot, nick, databasekey):
    databasecolumn = databasekey
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value
