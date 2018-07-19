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

development_team = ['deathbybandaid','Mace_Whatdo','dysonparkes','under_score','jimender2']
casino_bot_owner = "under_score"


# general


maxbet = 100
minjackbot = 500
wikiurl = 'https://github.com/deathbybandaid/SpiceBot/wiki/Casino'
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']*4
lotterymax = 30
slotwheel = ['MODEM', 'BSOD', 'RAM', 'CPU', 'RAID', 'VLANS', 'PATCH', 'WIFI', 'CPU', 'CLOUD', 'VLANS', 'AI','DARKWEB','BLOCKCHAIN','PASSWORD']
slottimeout = 5
colors = ['red', 'black']
roulettetimeout = 25
maxwheel = 29


def jackpot(bot):
    nick = 'SpiceBank'
    balance = bank(bot,nick)


def deal(bot, cardcount):
    # choose a random card from a deck and remove it from deck
    hand = []
    deckofcards = deck()
    for i in range(cardcount):
        card = get_trigger_arg(bot, deckofcards,'random')
        hand.append(card)
    return hand


def lotterypayout(bot,level):
    balance = jackpot(bot)
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
        balance = jackpot(bot)
        payout = int(0.1 * balance)
        if payout < 50:
            payout = 8
    elif level == 4:
        balance = jackpot(bot)
        payout = int(0.5 * balance)
        if payout < 250:
            payout = 8
    elif level == 5:
        balance = jackpot(bot)
        payout = int(balance)
        if payout < 500:
            payout = 500
    return payout


def lotterytimeout(bot):
    time = get_database_value(bot,'casino', 'lotterytimeout')
    return time


def setlotterytimeout(bot,commandvalue):
    success = False
    if commandvalue.isdigit():
        lotterytime = int(commandvalue)
        if lotterytime >= 10:
            set_database_value(bot,'casino', 'lotterytimeout',lotterytime)
            success = True
        return success


# ______banking
def bank(bot, nick):
    balance = 0
    if nick == 'SpiceBank':
        balance = get_database_value(bot,nick,'spicebucks_bank') or 0
    else:
        isvalid = targetcheck(bot,botcom,nick)
        if isvalid == 1:
            balance = get_database_value(bot,nick,'spicebucks_bank') or 0
    return balance


def transfer(bot, instigator, target, amount):
    success = False
    if not (target == 'Spicebank' or instigator == 'Spicebank'):
        isvalid = targetcheck(bot,target,instigator)
        isvalidtarget = targetcheck(bot,instigator,target)
        if not (isvalid == 1 and isvalidtarget == 1):
            return success

    if amount >= 0:
        instigator_balance = bank(bot,instigator)
        if amount <= instigator_balance:
            adjust_database_value(bot,instigator, 'spicebucks_bank', -(amount))
            adjust_database_value(bot,target, 'spicebucks_bank', amount)
            success = True
    return success


def addbucks(bot,target,amount):
    instigator = bot
    if not (target == 'Spicebank' or instigator == 'Spicebank'):
        isvalid = targetcheck(bot,target,instigator)
        isvalidtarget = targetcheck(bot,instigator,target)
        if not (isvalid == 1 and isvalidtarget == 1):
            return success
    success = False
    if amount > 0:
        adjust_database_value(bot,target, 'spicebucks_bank', amount)
        success = True
    return success


def minusbucks(bot,target,amount):
    success = False
    if amount > 0:
        adjust_database_value(bot,target, 'spicebucks_bank', -(amount))
        success = True
    return success