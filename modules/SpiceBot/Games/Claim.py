#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import arrow
import sys
import os
import datetime
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
# import Spicebucks

# Commands that work in privmsg
privcmdlist = ['check', 'admin', 'bladder', 'fridge']

# Admin Commands
admincommands = ['reset']

# Protected users
protectednicks = ['rycuda', 'Tech_Angel']
# Creator user
creatornicks = ["IT_Sean"]

# Drinks
drinkslist = ['Gatorade', 'Water', 'Soda', 'Beer']
drinkscost = 5

# Days before reclaim available
maxtime = 7

# Spicebuck reward values
firstclaim = 10
renewclaim = 5
stolenclaim = 20
masterclaim = 10  # Take, not give

# Bladder capacity
bladdersize = 10
claimcost = 2
SeanCost = 1


@sopel.module.commands('claim')
def mainfunction(bot, trigger):
    """Function to check if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    # Names/nicks for code
    instigator = trigger.nick
    owner = bot.config.core.owner
    mastername = bot.db.get_nick_value(instigator, 'claimed') or ''
    target = get_trigger_arg(bot, triggerargsarray, 1)
    admintarget = get_trigger_arg(bot, triggerargsarray, 2)
    # Names of channel
    inchannel = trigger.sender
    # Dates for usage
    todaydate = datetime.date.today()
    storedate = str(todaydate)
    # List all Bots
    botnicks = bot_config_names(bot)
    # Good to claim?
    okaytoclaim = 1

    # Make sure claims happen in channel, not privmsg
    if not inchannel.startswith("#") and target not in privcmdlist:
        okaytoclaim = 0
        osd(bot, trigger.sender, 'say', "Claims must be done in channel")

    # Handle if no target is specified
    elif not target:
        okaytoclaim = 0
        osd(bot, trigger.sender, 'say', "Who do you want to claim?")

    # Check if somebody is claimed, return if/when
    elif target == 'check':
        okaytoclaim = 0
        if not admintarget:
            admintarget = instigator
        claimdate = bot.db.get_nick_value(admintarget, 'claimdate')
        claimedby = bot.db.get_nick_value(admintarget, 'claimed')
        if not claimedby:
            if admintarget == instigator:
                osd(bot, trigger.sender, 'say', "Nobody has a claim on you yet, %s." % instigator)
            elif admintarget.lower() in [u.lower() for u in creatornicks]:
                osd(bot, trigger.sender, 'say', "No mere mortal can claim the almighty %s!" % admintarget)
            else:
                osd(bot, trigger.sender, 'say', "Nobody appears to have claimed %s yet, %s." % (admintarget, instigator))
        else:
            if admintarget == instigator:
                osd(bot, trigger.sender, 'say', "You were claimed by " + str(claimedby) + " on " + str(claimdate) + ", " + str(instigator) + ".")
            elif claimedby == instigator:
                osd(bot, trigger.sender, 'say', "You claimed " + str(admintarget) + " on " + str(claimdate) + ", " + instigator + ".")
            else:
                osd(bot, trigger.sender, 'say', str(admintarget) + " was claimed by " + str(claimedby) + " on " + str(claimdate) + ", " + instigator + ".")

    # Check how full your bladder is
    elif target == 'bladder':
        okaytoclaim = 0
        if not admintarget:
            admintarget = instigator
        bladdercontents = bot.db.get_nick_value(admintarget, 'bladdercapacity')
        if not bladdercontents:
            if admintarget.lower() not in [u.lower() for u in bot.users]:
                osd(bot, trigger.sender, 'say', "Please specify someone to check")
            elif admintarget == instigator:
                bot.db.set_nick_value(admintarget, 'bladdercapacity', bladdersize)
                bladdercontents = bladdersize
                osd(bot, trigger.sender, 'say', "You have " + str(int(bladdercontents/claimcost)) + " claims left in your bladder at present.")
            elif admintarget in creatornick:
                bot.db.set_nick_value(admintarget, 'bladdercapacity', bladdersize)
                bladdercontents = bladdersize
                osd(bot, trigger.sender, 'say', admintarget + "has " + str(int(bladdercontents/SeanCost)) + " claims left in his almighty bladder.")
            else:
                bot.db.set_nick_value(admintarget, 'bladdercapacity', bladdersize)
                bladdercontents = bladdersize
                osd(bot, trigger.sender, 'say', admintarget + " has " + str(int(bladdercontents/claimcost)) + " claims left in their bladder at present.")
        else:
            if admintarget.lower() not in [u.lower() for u in bot.users]:
                osd(bot, trigger.sender, 'say', "Please specify someone to check")
            elif admintarget == instigator:
                osd(bot, trigger.sender, 'say', "You have " + str(int(bladdercontents/claimcost)) + " claims left in your bladder at present.")
            elif admintarget in creatornick:
                osd(bot, trigger.sender, 'say', admintarget + "has " + str(int(bladdercontents/SeanCost)) + " claims left in his almighty bladder.")
            else:
                osd(bot, trigger.sender, 'say', admintarget + " has " + str(int(bladdercontents/claimcost)) + " claims left in their bladder at present.")

    # The fridge houses your drinks (similar to loot). You can buy them with spicebucks
    elif target.lower() == 'fridge':
        okaytoclaim = 0
        if not admintarget:
            admintarget = instigator
        fridgecontents = bot.db.get_nick_value(admintarget, 'fridgecontents')
        osd(bot, trigger.sender, 'say', "The fridge is a Work in Progress, " + admintarget)

    # Admin functions
    elif target.lower() == 'admin':
        okaytoclaim = 0
        function = get_trigger_arg(bot, triggerargsarray, 2)
        admintarget = get_trigger_arg(bot, triggerargsarray, 3)
        if trigger.admin:
            if function not in admincommands:
                osd(bot, trigger.sender, 'say', "Please specify what you would like to do. Valid options are: " + str(', '.join(admincommands)))
            else:
                if function == 'reset':
                    if not admintarget:
                        osd(bot, trigger.sender, 'say', "Please specify someone to reset claim on.")
                    elif admintarget.lower() not in [u.lower() for u in bot.users]:
                        osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
                    else:
                        bot.db.set_nick_value(admintarget, 'claimed', '')
                        bot.db.set_nick_value(admintarget, 'claimdate', '')
                        osd(bot, trigger.sender, 'say', "Claim info for " + admintarget + " has been reset!")
        else:
            osd(bot, trigger.sender, 'say', "Ha. You're not an admin, get lost.")

    # Can't claim yourself
    elif target == instigator:
        okaytoclaim = 0
        osd(bot, trigger.sender, 'say', "You can't claim yourself!")
        osd(bot, trigger.sender, 'action', 'mutters "moron".')

    # Can't claim the bot
    elif target.lower() in [u.lower() for u in botnicks]:
        okaytoclaim = 0
        if instigator in creatornicks:
            osd(bot, trigger.sender, 'say', "I'm sorry Sir, but %s cannot be claimed by anyone but %s." % (target, owner))
        else:
            osd(bot, trigger.sender, 'say', "Nope. %s has a permanent claim on %s!" % (owner, target))

    # Can't claim the creator
    elif target.lower() in [u.lower() for u in creatornicks]:
        okaytoclaim = 0
        osd(bot, trigger.sender, 'say', "Foolish mortal! Tremble before the might of the Almighty %s!" % target)
        bot.db.set_nick_value(instigator, 'claimed', target)
        bot.db.set_nick_value(instigator, 'claimdate', storedate)

    # Can't claim your claimant
    elif target.lower() == mastername.lower():
        okaytoclaim = 0
        osd(bot, trigger.sender, 'action', "facepalms")
        osd(bot, trigger.sender, 'say', "You can't claim " + target + ", " + instigator + ". They already have a claim on you.")
        # Take Spicebucks from instigator (masterclaim)
        # Spicebucks.spicebucks(bot, instigator, 'minus', masterclaim)

    # Can't claim everyone at once
    elif target == 'everyone':
        okaytoclaim = 0
        osd(bot, trigger.sender, 'say', instigator + " couldn't decide where to aim and pisses everywhere!")

    # Can't claim protected individuals
    elif target in protectednicks:
        okaytoclaim = 0
        osd(bot, trigger.sender, 'say', target + " is under my protection, " + instigator)
        osd(bot, trigger.sender, 'action', "pisses all over " + instigator + " to teach them a lesson")

    # If the target is not online OR a subcommand, handle it
    elif target.lower() not in [u.lower() for u in bot.users] and target not in privcmdlist:
        okaytoclaim = 0
        osd(bot, trigger.sender, 'say', "I'm not sure who that is.")

    # Input checks out. Verify dates and go ahead.
    elif okaytoclaim:
        claimedby = bot.db.get_nick_value(target, 'claimed') or ''
        bladdercontents = bot.db.get_nick_value(instigator, 'bladdercapacity') or bladdersize
        # First time claimed
        if claimedby == '':
            if instigator in creatornicks:
                osd(bot, trigger.sender, 'say', instigator + " releases the contents of his bladder on " + target + "! All should recognize this profound claim of ownership upon " + target + "!")
            else:
                osd(bot, trigger.sender, 'say', instigator + " urinates on " + target + "! Claimed!")
            bot.db.set_nick_value(target, 'claimed', instigator)
            bot.db.set_nick_value(target, 'claimdate', storedate)
            # Pay instigator Spicebucks (firstclaim)
            # Spicebucks.spicebucks(bot, instigator, 'plus', firstclaim)

        # Renewed claim
        elif claimedby == instigator:
            claimdate = bot.db.get_nick_value(target, 'claimdate') or '1999-12-31'
            datea = arrow.get(todaydate)
            dateb = arrow.get(claimdate)
            timepassed = datea - dateb
            dayspassed = timepassed.days
            if timepassed.days >= int(maxtime):
                if instigator in creatornicks:
                    osd(bot, trigger.sender, 'say', instigator + " releases the contents of his bladder on " + target + "! His Lordship has been renewed for all to recognize!")
                else:
                    osd(bot, trigger.sender, 'say', instigator + " urinates on " + target + " again! The claim has been renewed!")
                bot.db.set_nick_value(target, 'claimed', instigator)
                bot.db.set_nick_value(target, 'claimdate', storedate)
                # Pay instigator Spicebucks (renewclaim)
                # Spicebucks.spicebucks(bot, instigator, 'plus', renewclaim)
            else:
                osd(bot, trigger.sender, 'say', instigator + ", you already claimed " + target + ".")
        else:
            # Stolen claim
            claimdate = bot.db.get_nick_value(target, 'claimdate') or '1999-12-31'
            datea = arrow.get(todaydate)
            dateb = arrow.get(claimdate)
            timepassed = datea - dateb
            dayspassed = timepassed.days
            if timepassed.days >= int(maxtime):
                if instigator in creatornicks:
                    osd(bot, trigger.sender, 'say', instigator + ' releases the contents of his bladder on ' + target + '! ' + target + ' should be grateful for their new lord and master!')
                else:
                    osd(bot, trigger.sender, 'say', instigator + " urinates on " + target + "! The claim has been stolen from " + claimedby + "!")
                bot.db.set_nick_value(target, 'claimed', instigator)
                bot.db.set_nick_value(target, 'claimdate', storedate)
                # Pay instigator Spicebucks (stolenclaim)
                #spicebucks(bot, instigator, 'plus', stolenclaim)
            else:
                osd(bot, trigger.sender, 'say', target + " has already been claimed by " + str(claimedby) + ", so back off!")
    elif not okaytoclaim:
        return
    else:
        osd(bot, trigger.sender, 'say', bot.nick + " had an issue with their aim and peed absolutely everywhere!")


def spicebucks(bot, target, plusminus, amount):
    """Add or remove Spicebucks from account."""
    # command for getting and adding money to account
    success = 'false'
    if type(amount) == int:
        inbank = bank(bot, target)
    if plusminus == 'plus':
        adjust_database_value(bot, target, 'spicebucks_bank', amount)
        success = 'true'
    elif plusminus == 'minus':
        if inbank - amount < 0:
            # osd(bot, trigger.sender, 'say', "I'm sorry, you do not have enough spicebucks in the bank to complete this transaction.")
            success = 'false'
        else:
            adjust_database_value(bot, target, 'spicebucks_bank', -amount)
            success = 'true'
    else:
        # osd(bot, trigger.sender, 'say', "The amount you entered does not appear to be a number.  Transaction failed.")
        success = 'false'
    return success  # returns simple true or false so modules can check the if tranaction was a success


@sopel.module.interval(1800)  # 30 minute automation
def halfhourtimer(bot):
    """Function for bladder refill on half-hour timer."""
    for u in bot.users:
        bladdercontents = bot.db.get_nick_value(u, 'bladdercapacity') or 'unused'
        if bladdercontents == 'unused':
            bladdercontents = 10
            bot.db.set_nick_value(u, 'bladdercapacity', bladdercontents)
        elif bladdercontents < bladdersize:
            bladdercontents = bladdercontents + 1
            bot.db.set_nick_value(u, 'bladdercapacity', bladdercontents)
