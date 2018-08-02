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
from Bucks import *


@sopel.module.commands('banker', 'bank', 'payday', 'tax', 'taxes', 'funds', 'rob', 'bankreset', 'checkbank', 'transfer')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'banker')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    commandused = trigger.group(1)
    target = (get_trigger_arg(bot, triggerargsarray, 1)).lower() or 'notarget'
    amount = (get_trigger_arg(bot, triggerargsarray, 2)).lower() or 'noamount'
    channel = botcom.channel_current
    player = trigger.nick
    if commandused == '':
        message = "Welcome to the Casino.  Your options are payday, tax, , and bank."
        osd(bot, trigger.sender, 'say', message)
    elif commandused == 'checkbank':
        bot.say("Target: " + target + " Player:" + player)
        validbank = buckscheck(bot, botcom, target)
        bot.say(str(validbank))
    elif commandused == 'payday':
        paydayamount = 0
        paydayamount, msg = checkpayday(bot, botcom, player)
        if paydayamount > 0:
            addbucks(bot, botcom, player, paydayamount)
            message = "You haven't been paid yet today. Here's your " + str(paydayamount) + " spicy chips."
            osd(bot, trigger.sender, 'say', message)
        else:
            message = player + ", you've already been paid today. Now go do some work."
            osd(bot, trigger.sender, 'say', message)
    elif commandused == 'funds' and trigger.admin:  # admin only command
        success = 0
        if not target == 'notarget':
            if target == 'casino':
                success = 1
            elif targetcheck(bot, botcom, target, instigator) == 0:
                osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                success = 0
            else:
                success = 1
        if success == 1:
            amountfund = (get_trigger_arg(bot, triggerargsarray, 3)).lower() or 'noamount'
            if not amountfund == 'noamount':
                if amountfund.isdigit():
                    amountfund = int(amountfund)
                    if amountfund >= 0 and amountfund < 10000001:
                        set_database_value(bot, target, 'spicychips_bank', amountfund)
                        targetbalance = bank(bot, botcom, target)
                        osd(bot, trigger.sender, 'say', target + ' now has ' + str(targetbalance) + ' in the bank')
                    else:
                        osd(bot, trigger.sender, 'say', 'Please enter a postive number less then 1,000,000')
                else:
                    osd(bot, trigger.sender, 'say', 'Please enter a valid a amount to set the bank balance to')
            else:
                osd(bot, trigger.sender, 'say', 'Please enter a target and an amount to set their bank balance at')

        # Taxes
    elif (commandused == 'taxes' or commandused == 'tax'):
        usedamount = (get_database_value(bot, player, 'usedtaxes') or 0) + 1
        if target == 'notarget':
            target = player
        if not channel.startswith("#"):
            osd(bot, player, 'notice', commandused + " can only be used in a channel.")
        else:
            randomaudit = random.randint(1, usedamount)
            if not target == 'notarget':
                if targetcheck(bot, botcom, target, instigator) == 0:
                    osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                elif targetcheck(bot, botcom, target) == 3:
                    message = audit(bot, botcom, player)
                    osd(bot, trigger.sender, 'action', message)
                else:
                    if usedamount == 1:
                        adjust_database_value(bot, player, 'usedtaxes', 3)
                        taxtotal, message = paytaxes(bot, botcom, target)
                        osd(bot, trigger.sender, 'say', message)
                        if taxtotal >= 100:
                            kickback = int(taxtotal*0.1)
                            addbucks(bot, botcom, player, kickback)
                            osd(bot, trigger.sender, 'action', "gives " + player + " a kickback of " + str(kickback) + " for bringing this delinquent to our attention")
                    else:
                        message = audit(bot, botcom, player)
                        osd(bot, trigger.sender, 'action', message)
            else:
                taxtotal, message = paytaxes(bot, player)
                osd(bot, trigger.send, 'say', message)

    elif commandused == 'rob':
        usedamount = (get_database_value(bot, player, 'usedtaxes') or 0) + 2
        balance = bank(bot, botcom, target)
        if buckscheck(bot, botcom, target) == 0:
            osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
        else:
            if usedamount > 10:
                triggerbalance = bank(bot, botcom, player)
                fine = int(triggerbalance*.20)
                osd(bot, trigger.sender, 'say', player + " get's caught for pickpocketing too much and is fined " + str(fine))
                transfer(bot, botcom, 'casino', player, fine)
            else:
                adjust_database_value(bot, player, 'usedtaxes', 1)
                randomcheck = random.randint(0, 5)
                if randomcheck == 3:
                    triggerbalance = bank(bot, botcom, player)
                    fine = int(triggerbalance*.20)
                    osd(bot, trigger.sender, 'say', player + " get's caught trying to pickpocket " + target + " and is fined for " + str(fine))
                    transfer(bot, botcom, 'casino', player, fine)
                else:
                    payout = int(balance * .01)
                    if payout > 0:
                        osd(bot, trigger.sender, 'say', player + " pickpockets " + str(payout) + " from " + target)
                        transfer(bot, botcom, target, player, payout)
                    else:
                        osd(bot, trigger.sender, 'say', target + "'s pockets are empty")
        # Bank
    elif commandused == 'banker' or commandused == 'bank':
        if target == 'notarget':
            target = player
        balance = bank(bot, botcom, target)
        osd(bot, trigger.sender, 'say', target + " has " + str(balance) + " spicy chips.")

    elif commandused == 'bankreset' and trigger.admin:  # admin only command
        if target == 'notarget':
            target = trigger.nick
        validtarget = targetcheck(bot, botcom, target, instigator)
        if validtarget == 0:
            osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
        else:
            reset(bot, target)
            osd(bot, trigger.sender, 'say', 'Payday reset for ' + target)


# admin command reset user values
def reset(bot, target):
    reset_database_value(bot, target, 'spicychips_payday')
    reset_database_value(bot, target, 'spicychips_taxday')
    reset_database_value(bot, target, 'usedtaxes')


def audit(bot, botcom, player):
    inbank = bank(bot, botcom, player)
    auditamount = int(inbank * .20)
    msg = ""
    if auditamount > 0:
        msg = "carries out an audit on " + player + " and takes " + str(auditamount) + " spicy chips for the pleasure."
        transfer(bot, botcom, 'casino', player, auditamount)
    else:
        msg = "carries out an audit on " + player + " but finds no spicy chips to take."
        reset_database_value(bot, player, 'usedtaxes')
    return msg


def checkpayday(bot, botcom, target):
    paydayamount = 0
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    spicebank = bank(bot, botcom, 'casino')
    paydaymsg = "none"
    if spicebank <= 0:
        spicebank = 500
    lastpayday = get_database_value(bot, target, 'spicychips_payday') or 0
    if lastpayday == 0 or lastpayday < datetoday:
        paydayamount = int(spicebank * 0.01)
        set_database_value(bot, target, 'spicychips_payday', datetoday)
        paydaymsg = "Pay day found"
    else:
        paydaymsg = "Spicbank: " + str(spicebank) + "lastpay: " + str(lastpayday) + "Today: " + str(datetoday)
    return paydayamount, paydaymsg


def paytaxes(bot, botcom, target):
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    lasttaxday = get_database_value(bot, target, 'spicychips_taxday') or 0
    inbank = bank(bot, botcom, target) or 0
    taxtotal = 0
    message = ""
    if lasttaxday == 0 or lasttaxday < datetoday:
        reset_database_value(bot, target, 'usedtaxes')
        taxtotal = int(inbank * .1)
        if inbank == 1:
            taxtotal = 1
        if taxtotal > 0:
            transfer(bot, botcom, 'casino', target, taxtotal)
            set_database_value(bot, target, 'spicychips_taxday', datetoday)
            message = "Thank you for reminding me that " + target + " has not paid their taxes today. " + str(taxtotal) + " spicy chips will be transfered to the Casino."
        else:
            message = target + " is broke and cannot pay taxes today"
    else:
        message = "Taxes already paid today."
    return taxtotal, message
