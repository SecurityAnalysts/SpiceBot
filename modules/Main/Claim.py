#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import arrow
import sys
import os
import datetime
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)

from SpicebotShared import *
import Spicebucks

# Commands that work in privmsg
privcmdlist = ['check','admin','bladder','drink','fridge']

# Admin Commands
admincommands = ['reset']

# Names of drinks
drinkslist = ['Gatorade','Water','Soda','Beer']

# Days before reclaim available
maxtime = 7
# Spicebuck reward values
firstclaim = 5
renewclaim = 2
stolenclaim = 10
masterclaim = 5 #take, not give


@sopel.module.commands('claim')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    # Names/nicks for code
    instigator = trigger.nick
    creator = "IT_Sean"
    owner = bot.config.core.owner
    mastername = bot.db.get_nick_value(instigator,'claimed') or ''
    target = get_trigger_arg(bot, triggerargsarray, 1)
    admintarget = get_trigger_arg(bot, triggerargsarray, 2)
    # Names of channel
    inchannel = trigger.sender
    channel = trigger.sender
    # Dates for usage
    todaydate = datetime.date.today()
    storedate = str(todaydate)
    # Good to claim?
    okaytoclaim = 1

    # Make sure claims happen in channel, not privmsg
    if not inchannel.startswith("#") and target not in privcmdlist:
        okaytoclaim = 0
        bot.say("Claims must be done in channel")

    # Handle if no target is specified
    elif not target:
        okaytoclaim = 0
        bot.say("Who do you want to claim?")

    # Check if somebody is claimed, return if/when
    elif target == 'check':
        okaytoclaim = 0
        if not admintarget:
            admintarget = instigator
        claimdate = bot.db.get_nick_value(admintarget, 'claimdate')
        claimedby = bot.db.get_nick_value(admintarget,'claimed')
        if not claimedby:
            if admintarget == instigator:
                bot.say("Nobody has a claim on you yet, " + str(instigator) +".")
            elif admintarget == creator:
                bot.say("No mere mortal can claim the almighty " + str(creator) +"!")
            else:
                bot.say("Nobody appears to have claimed " + str(admintarget) + " yet, " + str(instigator) + ".")
        else:
            if admintarget == instigator:
                bot.say("You were claimed by " + str(claimedby) + " on " + str(claimdate) +", " + str(instigator) + ".")
            elif claimedby == instigator:
                bot.say("You claimed " + str(admintarget) + " on " + str(claimdate) +", " + instigator + ".")
            else:
                bot.say(str(admintarget) + " was claimed by " + str(claimedby) + " on " + str(claimdate) +", " + instigator + ".")

    # Admin functions
elif target == 'admin':
        okaytoclaim = 0
        function = get_trigger_arg(bot,triggerargsarray, 2)
        admintarget = get_trigger_arg(bot, triggerargsarray, 3)
        if trigger.admin:
            if function not in admincommands:
                bot.say("Please specify what you would like to do. Valid options are: " + str(admincommands))
            else:
                if function == 'reset':
                    if not admintarget:
                        bot.say("Please specify someone to reset claim on.")
                    elif admintarget.lower() not in [u.lower() for u in bot.users]:
                        bot.say("I'm not sure who that is.")
                    else:
                        bot.db.set_nick_value(admintarget,'claimed','')
                        bot.db.set_nick_value(admintarget,'claimdate','')
                        bot.say("Claim info for " + admintarget + " has been reset!"")
        else:
            bot.say("Ha. You're not an admin, get lost.")

    # Can't claim yourself
    elif target == instigator:
        okaytoclaim = 0
        bot.say("You can't claim yourself!")
        bot.action('mutters "moron".')

    # Can't claim the bot
    elif target == bot.nick:
        okaytoclaim = 0
        if instigator == creator:
            bot.say("I'm sorry Sir, but I cannot be claimed by anyone but " + owner + ".")
        else:
            bot.say("I have already been claimed by " + owner +"!")

    # Can't claim the creator
    elif target == creator:
        okaytoclaim = 0
        bot.say("Foolish mortal! Tremble before the might of the Almighty " + creator + "!")
        bot.db.set_nick_value(instigator,'claimed',target)
        bot.db.set_nick_value(instigator,'claimdate',storedate)

    # Can't claim your claimant
    elif target == mastername:
        okaytoclaim = 0
        bot.action("facepalms")
        bot.say("You can't claim " + target + ", "+ instigator + ". They already have a claim on you.")
        # Take Spicebucks from instigator (masterclaim)
        Spicebucks.spicebucks(bot, instigator, 'minus', masterclaim)

    # Can't claim everyone at once
    elif target == 'everyone':
        okaytoclaim = 0
        bot.say(instigator + " couldn't decide where to aim and pisses everywhere!")

    # If the target is not online OR a subcommand, handle it
    elif target.lower() not in [u.lower() for u in bot.users] and target not in privcmdlist:
        okaytoclaim = 0
        bot.say("I'm not sure who that is.")

    # Input checks out. Verify dates and go ahead.
    elif okaytoclaim:
        claimedby = bot.db.get_nick_value(target,'claimed') or ''
        # First time claimed
        if claimedby == '':
            if instigator == creator:
                bot.say(instigator + " releases the contents of his bladder on " + target + "! All should recognize this profound claim of ownership upon " + target +"!")
            else:
                bot.say(instigator + " urinates on " + target + "! Claimed!")
            bot.db.set_nick_value(target,'claimed',instigator)
            bot.db.set_nick_value(target,'claimdate',storedate)
            # Pay instigator Spicebucks (firstclaim)
            Spicebucks.spicebucks(bot, instigator, 'plus', firstclaim)

        # Renewed claim
        elif claimedby == instigator:
            claimdate = bot.db.get_nick_value(target, 'claimdate') or '1999-12-31'
            datea = arrow.get(todaydate)
            dateb = arrow.get(claimdate)
            timepassed = datea - dateb
            dayspassed = timepassed.days
            if timepassed.days >= int(maxtime):
                if instigator == creator:
                    bot.say(instigator + " releases the contents of his bladder on " + target + "! His Lordship has been renewed for all to recognize!")
                else:
                    bot.say(instigator + " urinates on " + target + " again! The claim has been renewed!")
                bot.db.set_nick_value(target,'claimed',instigator)
                bot.db.set_nick_value(target,'claimdate',storedate)
                # Pay instigator Spicebucks (renewclaim)
                Spicebucks.spicebucks(bot, instigator, 'plus', renewclaim)
            else:
                bot.say(instigator + ", you already claimed " + target +".")
        else:
            # Stolen claim
            claimdate = bot.db.get_nick_value(target, 'claimdate') or '1999-12-31'
            datea = arrow.get(todaydate)
            dateb = arrow.get(claimdate)
            timepassed = datea - dateb
            dayspassed = timepassed.days
            if timepassed.days >= int(maxtime):
                if instigator == creator:
                    bot.say(instigator + ' releases the contents of his bladder on ' + target + '! ' + target +' should be grateful for their new lord and master!')
                else:
                    bot.say(instigator + " urinates on " + target + "! The claim has been stolen from " + claimedby + "!")
                bot.db.set_nick_value(target,'claimed',instigator)
                bot.db.set_nick_value(target,'claimdate',storedate)
                # Pay instigator Spicebucks (stolenclaim)
                Spicebucks.spicebucks(bot, instigator, 'plus', stolenclaim)
            else:
                bot.say(target + " has already been claimed by " + str(claimedby) + ", so back off!")
    elif not okaytoclaim:
        return
    else:
        bot.say(bot.nick + " had an issue with their aim and peed absolutely everywhere!")
