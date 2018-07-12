#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import arrow
import sys
import os
import datetime
import random
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)

from SpicebotShared import *

commandarray = ["accept","delete","money"]

@sopel.module.commands('bribe')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    databasekey = "bribe"
    instigator = trigger.nick
    command = get_trigger_arg(bot, triggerargsarray, 1)
    target = get_trigger_arg(bot, triggerargsarray, 1)
    if command in commandarray:
        if command == "accept":
            amo = get_botdatabase_value(bot, instigator, 'bets') or '0'
            amount = int(amo)
	    reset_botdatabase_value(bot,instigator, 'bets')
            spicebucks(bot, instigator, "plus", amount)
            if amount == 0:
                bot.say("There are no bribes for you to accept")
            else:
		bot.say(instigator + " accepted the bribe of $" + amount + ".")
        elif command == "decline":
            bot.say(instigator + " declines a bribe worth $" + amount +".")
    
    else:
         if target.lower() in [u.lower() for u in bot.users]:
            balance = bank(bot, instigator)
            money = random.randint(0, balance)
            bot.say(instigator + " bribes " + target + " with $" + str(money) + " in nonsequental, unmarked bills.")
            inputstring = str(money)
            set_botdatabase_value(bot,target, 'bets', inputstring)
            spicebucks(bot, instigator, 'minus', money)
         else:
            bot.say("I'm sorry, I do not know who " + target + " is.")

def bank(bot, nick):
    balance = get_botdatabase_value(bot,nick,'spicebucks_bank') or 0
    return balance

def spicebucks(bot, target, plusminus, amount):
    #command for getting and adding money to account
    success = 'false'
    if type(amount) == int:
        inbank = bank(bot,target)
    if plusminus == 'plus':
       adjust_botdatabase_value(bot,target, 'spicebucks_bank', amount)
       success = 'true'
    elif plusminus == 'minus':
        if inbank - amount < 0:
            success = 'false'
        else:
            adjust_botdatabase_value(bot,target, 'spicebucks_bank', -amount)
            success = 'true'
    else:
        success = 'false'
    return success

def get_database_value(bot, nick, databasekey):
	databasecolumn = databasekey
	database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
	return database_value