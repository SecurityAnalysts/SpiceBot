#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('eyeroll')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'sbc')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    inchannel = trigger.sender
    target = get_trigger_arg(bot, triggerargsarray, 1)
    message = get_trigger_arg(bot, triggerargsarray, '2+')
    if not message:
        message = instigator + " rolls their eyes at " + target
    bot.say(message)

    databasekey = 'murder'
    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')
    existingarray = get_botdatabase_value(bot, bot.nick, databasekey) or []
    if command in commandarray:
        if command == "gender":
            gender = get_trigger_arg(bot, triggerargsarray, 3)
            if gender == male
                adjust_botdatabase_array
            if inputstring not in existingarray:
                adjust_botdatabase_array(bot, bot.nick, inputstring, databasekey, 'add')
                message = "Added to database."
		bot.say(message)
            else:
                message = "You are already a " + gender
		bot.say(message)
        
        elif command == "last":
		message = get_trigger_arg(bot, existingarray, "last")
		bot.say(message)
    
	# No target specified
	if not target:
		bot.say("Who/what would you like to murder?")

	# Target is fine
	else:
		if not reason:
			message = instigator + " rolls " + gender + " at " + target + "."
        		bot.say(message)
		else:
			message = instigator + " rolls " + gender + " at " + target + " because " + reason + "."
        		bot.say(message)

def get_database_value(bot, nick, databasekey):
	databasecolumn = str(databasekey)
	database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
	return database_value