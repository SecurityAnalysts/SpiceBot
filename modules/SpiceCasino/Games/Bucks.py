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
        card = get_trigger_arg(bot, deckofcards, 'random')
        hand.append(card)
    return hand


def lotterypayout(bot, level):
    balance = casino(bot)
    payout = 0
    if level == 1:
        payout = int(0.04 * balance)
        if payout < 20:
            payout = 20
    elif level == 2:
        payout = int(0.08 * balance)
        if payout < 20:
            payout = 8
    elif level == 3:
        balance = casino(bot)
        payout = int(0.1 * balance)
        if payout < 50:
            payout = 8
    elif level == 4:
        balance = casino(bot)
        payout = int(0.5 * balance)
        if payout < 250:
            payout = 8
    elif level == 5:
        balance = casino(bot)
        payout = int(balance)
        if payout < 500:
            payout = 500
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


def transfer(bot, botcom, target, instigator, amount):
    success = False
    if not (target == 'casino' or instigator == 'casino'):
        isvalid = buckscheck(bot, botcom, target)
        isvalidtarget = buckscheck(bot, botcom, instigator)
        if not (isvalid == 1 and isvalidtarget == 1):
            return success

    if amount >= 0:
        bot.say(str(amount))
        instigator_balance = bank(bot, botcom, instigator)
        bot.say(str(instigator_balance))
        if amount <= instigator_balance:
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
    if target == ''botcom.instigator.default'':
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
