#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import datetime
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('spicebucks', 'bank')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'spicebucks')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    botusersarray = get_database_value(bot, bot.nick, 'botusers') or []
    channel = trigger.sender
    commandused = spicemanip(bot, triggerargsarray, 1) or 'nocommand'
    botuseron = []
    for u in bot.users:
        if u in botusersarray and u != bot.nick:
            botuseron.append(u)

    if commandused == 'nocommand':
        osd(bot, trigger.sender, 'say', "Welcome to the SpiceBank.  Your options are payday, tax, makeitrain, and bank.")
    else:
        # #PayDay
        if commandused == 'payday':
            paydayamount = 0
            paydayamount = checkpayday(bot, trigger.nick)
            if paydayamount > 0:
                spicebucks(bot, trigger.nick, 'plus', paydayamount)
                osd(bot, trigger.sender, 'say', "You haven't been paid yet today. Here's your " + str(paydayamount) + " spicebucks.")
            else:
                osd(bot, trigger.sender, 'say', trigger.nick + ", you've already been paid today. Now go do some work.")
        # ###MakeitRain
        elif commandused == 'makeitrain':
            if not channel.startswith("#"):
                osd(bot, trigger.nick, 'notice', commandused + " can only be used in a channel.")
            else:
                    target = spicemanip(bot, triggerargsarray, 2) or 'notarget'
                    if (target == 'notarget' or target == 'everyone'):
                        target = 'Everyone'
                        osd(bot, trigger.sender, 'action', "rains " + trigger.nick + "'s Spicebucks down on " + target)
                    else:
                        if not checkpayday(bot, trigger.nick) == 0:
                            if (target == 'random' or target == trigger.nick or target == bot.nick):
                                target = randomuser(bot, trigger.nick)
                                if target == 'None':
                                    target = randomuser(bot, trigger.nick)
                                spicebucks(bot, trigger.nick, 'plus', 50)
                                bankbalance = bank(bot, trigger.nick)
                                maxpayout = bankbalance-(int(bankbalance*.50))
                                osd(bot, trigger.sender, 'say', trigger.nick + ' rains Spicebucks down on ' + target)
                                winnings = random.randint(1, maxpayout)
                                transfer(bot, trigger.nick, target, winnings)
                                mypayday = 0-winnings
                                if mypayday >= 0:
                                    osd(bot, trigger.sender, 'say', trigger.nick + " gets " + str(mypayday) + " spicebucks and " + target + " manages to keep " + str(winnings) + " of " + trigger.nick + "'s spicebucks.")
                                else:
                                    mypayday = abs(mypayday)
                                    osd(bot, trigger.sender, 'say', trigger.nick + " loses " + str(mypayday) + " spicebucks and " + target + " manages to keep " + str(winnings) + " of " + trigger.nick + "'s spicebucks.")
                            elif targetcheck(bot, target, trigger.nick) == 0:
                                osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                            else:
                                spicebucks(bot, trigger.nick, 'plus', 50)
                                bankbalance = bank(bot, trigger.nick)
                                maxpayout = bankbalance-(int(bankbalance * .50))
                                osd(bot, trigger.sender, 'say', trigger.nick + ' rains Spicebucks down on ' + target)
                                winnings = random.randint(1, maxpayout)
                                mypayday = 0-winnings
                                if mypayday >= 0:
                                    osd(bot, trigger.sender, 'say', trigger.nick + " gets " + str(mypayday) + " spicebucks and " + target + " manages to keep " + str(winnings) + " of " + trigger.nick + "'s spicebucks.")
                                else:
                                    mypayday = abs(mypayday)
                                    osd(bot, trigger.sender, 'say', trigger.nick + " loses " + str(mypayday) + " spicebucks and " + target + " manages to keep " + str(winnings) + " of " + trigger.nick + "'s spicebucks.")

                                transfer(bot, trigger.nick, target, winnings)
                        else:
                            osd(bot, trigger.sender, 'say', trigger.nick + ", you have already been paid today")
        # Reset
        elif commandused == 'reset' and trigger.admin:  # admin only command
            target = spicemanip(bot, triggerargsarray, 2) or 'notarget'
            validtarget = targetcheck(bot, target, trigger.nick)
            if target == 'notarget' or target == trigger.nick:
                reset(bot, target)
                osd(bot, trigger.sender, 'say', 'Payday reset for ' + trigger.nick)
            elif not validtarget == 0:
                reset(bot, target)
                osd(bot, trigger.sender, 'say', 'Payday reset for ' + target)
            else:
                osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")

        # Funds
        elif commandused == 'funds' and trigger.admin:  # admin only command
            success = 0
            target = spicemanip(bot, triggerargsarray, 2) or 'notarget'
            if not target == 'notarget':
                if target.lower() == 'spicebank':
                    target = 'SpiceBank'
                    success = 1
                elif targetcheck(bot, target, trigger.nick) == 0:
                    osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                    success = 0
                else:
                    success = 1
            if success == 1:
                amount = spicemanip(bot, triggerargsarray, 3) or 'noamount'
                if not amount == 'noamount':
                    if amount.isdigit():
                        amount = int(amount)
                        if amount >= 0 and amount < 10000001:
                            set_database_value(bot, target, 'spicebucks_bank', amount)
                            targetbalance = bank(bot, target)
                            osd(bot, trigger.sender, 'say', target + ' now has ' + str(targetbalance) + ' in the bank')
                        else:
                            osd(bot, trigger.sender, 'say', 'Please enter a postive number less then 1,000,000')
                    else:
                        osd(bot, trigger.sender, 'say', 'Please enter a valid a amount to set the bank balance to')
                else:
                    osd(bot, trigger.sender, 'say', 'Please enter a target and an amount to set their bank balance at')

        # Taxes
        elif (commandused == 'taxes' or commandused == 'tax'):
            if not channel.startswith("#"):
                osd(bot, trigger.nick, 'priv', commandused + " can only be used in a channel.")
            else:
                target = spicemanip(bot, triggerargsarray, 2) or 'notarget'
                if not target == 'notarget':
                    if targetcheck(bot, target, trigger.nick) == 0:
                        osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                    elif targetcheck(bot, target, trigger.nick) == 2:
                        inbank = bank(bot, trigger.nick)
                        auditamount = int(inbank * .20)
                        if auditamount > 0:
                            osd(bot, trigger.sender, 'action', "carries out an audit on " + trigger.nick + " and takes " + str(auditamount) + " spicebucks for the pleasure.")
                            spicebucks(bot, trigger.nick, 'minus', auditamount)

                        else:
                            osd(bot, trigger.sender, 'action', "carries out an audit on " + trigger.nick + " but finds no spicebucks to take.")
                            reset_database_value(bot, target, 'usedtaxes')
                    else:
                        if get_database_value(bot, trigger.nick, 'usedtaxes') < 2:
                            adjust_database_value(bot, trigger.nick, 'usedtaxes', 1)
                            taxtotal = paytaxes(bot, target)
                            if taxtotal >= 100:
                                kickback = int(taxtotal * 0.1)
                                adjust_database_value(bot, trigger.nick, 'spicebucks_bank', kickback)
                                osd(bot, trigger.sender, 'action', "gives " + trigger.nick + " a kickback of " + str(kickback) + " for bringing this delinquent to our attention")

                        else:
                            inbank = bank(bot, trigger.nick)
                            auditamount = int(inbank * .20)
                            if auditamount > 0:
                                osd(bot, trigger.sender, 'action', "carries out an audit on " + trigger.nick + " and takes " + str(auditamount) + " spicebucks for the pleasure.")
                                spicebucks(bot, trigger.nick, 'minus', auditamount)

                            else:
                                osd(bot, trigger.sender, 'action', "carries out an audit on " + trigger.nick + " but finds no spicebucks to take.")
                                reset_database_value(bot, target, 'usedtaxes')
                else:
                    adjust_database_value(bot, trigger.nick, 'usedtaxes', 1)
                    taxtotal = paytaxes(bot, trigger.nick)

        elif commandused == 'rob':
            target = spicemanip(bot, triggerargsarray, 2) or 'notarget'
            balance = bank(bot, target)
            if targetcheck(bot, target, trigger.nick) == 0:
                osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
            else:
                if get_database_value(bot, trigger.nick, 'usedtaxes') > 2:
                    adjust_database_value(bot, trigger.nick, 'usedtaxes', 1)
                    triggerbalance = bank(bot, trigger.nick)
                    fine = int(triggerbalance*.20)
                    osd(bot, trigger.sender, 'say', trigger.nick + " get's caught for pickpocketing too much and is fined " + str(fine))
                    spicebucks(bot, trigger.nick, 'minus', fine)
                else:
                    adjust_database_value(bot, trigger.nick, 'usedtaxes', 1)
                    randomcheck = random.randint(0, 5)
                    if randomcheck == 3:
                        triggerbalance = bank(bot, trigger.nick)
                        fine = int(triggerbalance*.20)
                        osd(bot, trigger.sender, 'say', trigger.nick + " get's caught trying to pickpocket " + target + " and is fined for " + str(fine))
                        spicebucks(bot, trigger.nick, 'minus', fine)
                    else:
                        payout = int(balance * .01)
                        osd(bot, trigger.sender, 'say', trigger.nick + " pickpockets " + str(payout) + " from " + target)

                        transfer(bot, target, trigger.nick, payout)

        # Bank
        elif commandused == 'bank':
            target = spicemanip(bot, triggerargsarray, 2) or 'notarget'
            checkedtarget = targetcheck(bot, target, trigger.nick) or 0

            if not target == 'notarget':
                if target == 'spicebank':
                    balance = bank(bot, 'spicebucks') or 0
                    osd(bot, trigger.sender, 'say', 'The current casino jackpot is ' + str(balance))
                elif checkedtarget == 0:
                    osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                else:
                    balance = bank(bot, target)
                    osd(bot, trigger.sender, 'say', target + ' has ' + str(balance) + " spicebucks in the bank.")
            else:
                balance = bank(bot, trigger.nick)
                osd(bot, trigger.sender, 'say', "You have " + str(balance) + " spicebucks in the bank.")


# admin command reset user values
def reset(bot, target):
    reset_database_value(bot, target, 'spicebucks_payday')
    reset_database_value(bot, target, 'spicebucks_taxday')
    reset_database_value(bot, target, 'usedtaxes')


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
            # osd(bot, trigger.sender, 'say', "I'm sorry, you do not have enough spicebucks in the bank to complete this transaction.")
            success = 'false'
        else:
            adjust_database_value(bot, target, 'spicebucks_bank', -amount)
            success = 'true'
    else:
        # osd(bot, trigger.sender, 'say', "The amount you entered does not appear to be a number.  Transaction failed.")
        success = 'false'
    return success  # returns simple true or false so modules can check the if tranaction was a success


def checkpayday(bot, target):
    paydayamount = 0
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    spicebank = bank(bot, 'SpiceBank')
    lastpayday = get_database_value(bot, target, 'spicebucks_payday') or 0
    if lastpayday == 0 or lastpayday < datetoday:
        paydayamount = int(spicebank * 0.01)
        set_database_value(bot, target, 'spicebucks_payday', datetoday)
    else:
        paydayamount = 0
    return paydayamount


def paytaxes(bot, target):
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    lasttaxday = get_database_value(bot, target, 'spicebucks_taxday') or 0
    inbank = bank(bot, target) or 0
    taxtotal = 0
    if lasttaxday == 0 or lasttaxday < datetoday:
        reset_database_value(bot, target, 'usedtaxes')
        taxtotal = int(inbank * .1)
        if inbank == 1:
            taxtotal = 1
        if taxtotal > 0:
            spicebucks(bot, 'SpiceBank', 'plus', taxtotal)
            spicebucks(bot, target, 'minus', taxtotal)
            set_database_value(bot, target, 'spicebucks_taxday', datetoday)
            osd(bot, trigger.sender, 'say', "Thank you for reminding me that " + target + " has not paid their taxes today. " + str(taxtotal) + " spicebucks will be transfered to the SpiceBank.")
            return taxtotal
        else:
            osd(bot, trigger.sender, 'say', target + ' is broke and cannot pay taxes today')
            return taxtotal
    else:
        osd(bot, trigger.sender, 'say', "Taxes already paid today.")
        return taxtotal


def transfer(bot, instigator, target, amount):
    validamount = 0
    if amount >= 0:
        if spicebucks(bot, instigator, 'minus', amount) == 'true':
            spicebucks(bot, target, 'plus', amount)
            validamount = 1
    return validamount


def randomuser(bot, nick):
    randompersons = []
    randomperson = ''
    botusersarray = get_database_value(bot, bot.nick, 'botusers') or []
    for u in bot.users:
        if u in botusersarray and u != bot.nick and u != nick:
            randompersons.append(u)
    randomperson = spicemanip(bot, randompersons, 'random')
    return randomperson
