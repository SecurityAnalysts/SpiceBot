# Variblies for casino

from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
sys.path.append(moduledir)
from BotShared import *

development_team = ['deathbybandaid', 'Mace_Whatdo', 'dysonparkes', 'under_score', 'jimender2']
casino_bot_owner = "under_score"


def deal(bot, cardcount):
    # choose a random card from a deck and remove it from deck
    hand = []
    deckofcards = deck()
    for i in range(cardcount):
        card = spicemanip(bot, deckofcards, 'random')
        hand.append(card)
    return hand


def lotterypayout(bot, level):
    balance = bankdev(bot, 'casino')
    if balance < 500:
        addbucksdev(bot, 'casino', 500)
        balance = bank(bot, botcom, 'casino')
    payout = 0
    if level == 1:
        payout = int(0.04 * balance)  # min 20
        if payout < 20:
            payout = 20
    elif level == 2:
        payout = int(0.08 * balance)  # min 40
        if payout < 20:
            payout = 8
    elif level == 3:
        payout = int(0.1 * balance)  # min 50
        if payout < 50:
            payout = 8
    elif level == 4:
        payout = int(0.5 * balance)  # min 250
        if payout < 250:
            payout = 8
    elif level == 5:
        payout = int(balance)
    return payout


def lotterytimeout(bot):
    time = get_database_value(bot, 'casino', 'lotterytimeout')
    return time


def setlotterytimeout(bot, commandvalue):
    success = False
    if commandvalue.isdigit():
        lotterytime = int(commandvalue)
        if lotterytime >= 10:
            set_database_value(bot, 'casino', 'lotterytimeout', lotterytime)
            success = True
        return success


# ______banking
def bank(bot, botcom, nick):
    balance = 0
    if nick == 'casino':
        balance = get_database_value(bot, nick, 'spicychips_bank') or 0
    else:
        isvalid = buckscheck(bot, botcom, nick)
        if isvalid == 1 or isvalid == 2:
            balance = get_database_value(bot, nick, 'spicychips_bank') or 0
    return balance


def bankdev(bot,  nick):
    balance = 0
    balance = get_database_value(bot, nick, 'spicychips_bank') or 0
    return balance


def transfer(bot, botcom, target, instigator, amount):
    success = False
    if not (target == 'casino' or instigator == 'casino'):
        isvalid = buckscheck(bot, botcom, target)
        isvalidtarget = buckscheck(bot, botcom, instigator)
        if not (isvalid == 1 and isvalidtarget == 1):
            return success

    if amount >= 0:
        # bot.say(str(amount))
        instigator_balance = bank(bot, botcom, instigator)
        # bot.say(str(instigator_balance))
        if amount <= instigator_balance:
            testamount = instigator_balance - amount
            # bot.say(str(testamount))
            adjust_database_value(bot, target, 'spicychips_bank', amount)
            adjust_database_value(bot, instigator, 'spicychips_bank', -(amount))
            success = True
        return success


def transferdev(bot,  target, instigator, amount):
    success = False
    if amount >= 0:
        # bot.say(str(amount))
        instigator_balance = bankdev(bot, instigator)
        # bot.say(str(instigator_balance))
        if amount <= instigator_balance:
            testamount = instigator_balance - amount
            # bot.say(str(testamount))
            adjust_database_value(bot, target, 'spicychips_bank', amount)
            adjust_database_value(bot, instigator, 'spicychips_bank', -(amount))
            success = True
        return success


def addbucks(bot, botcom, target, amount):
    success = False
    if not (target == 'casino'):
        isvalid = buckscheck(bot, botcom, target)
        if not (isvalid == 1):
            return success
    if amount > 0:
        adjust_database_value(bot, target, 'spicychips_bank', amount)
        success = True
    return success


def addbucksdev(bot, target, amount):
    success = False
    if amount > 0:
        adjust_database_value(bot, target, 'spicychips_bank', amount)
        success = True
    return success


def minusbucks(bot, botcom, target, amount):
    success = False
    isvalid = buckscheck(bot, botcom, target)
    if not (isvalid == 1):
        return success
    if amount > 0:
        adjust_database_value(bot, target, 'spicychips_bank', -(amount))
        success = True
    return success


def buckscheck(bot, botcom, target):
    # Guilty until proven Innocent
    validtarget = 1
    validtargetmsg = []
    # target = target.lower()
    """ Target is instigator
    if target == ''botcom.botcom.instigator'':
        validtarget = 2
        validtargetmsg.append("Target is instigator")
        return validtarget, validtargetmsg
    """

    if target == bot.nick:
        validtarget = 3
        validtargetmsg.append("Target is a bot")
        return validtarget

    # Null Target
    if not target:
        validtarget = 0
        validtargetmsg.append("You must specify a target.")
        return validtarget, validtargetmsg

    if target in botcom.users_current:
        return validtarget
    else:
        validtarget = 0
        validtargetmsg.append(target + " isn't a valid user")
        return validtarget
