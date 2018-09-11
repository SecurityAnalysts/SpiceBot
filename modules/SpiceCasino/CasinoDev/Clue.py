#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from random import random
from random import randint
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
# from Bucks import *

cluefee = 5  # amount charged to use the command
rooms = ['Ballroom', 'Billiard Room', 'Cellar', 'Conservatory', 'Dining Room', 'Kitchen', 'Hall', 'Library', 'Lounge', 'Study', 'secret passage', 'Spa', 'Theater', 'Nearby Guest House']
weapons = ['Candlestick', 'Knife', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench', 'Dumbbell', 'Trophy', 'Poison']


@sopel.module.commands('clue')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    channel = trigger.sender
    instigator = trigger.nick
    pointsworth = random.uniform(.03, .08)
    if not channel.startswith("#"):
        osd(bot, instigator, 'notice', "Clue must be in a channel.")
        return
    target = spicemanip(bot, triggerargsarray, 1)
    suspect = spicemanip(bot, triggerargsarray, 2)
    cluefee = 5
    if not target:
        cluefee = 0
        pointsworth = 0
    players = []
    if Spicebucks.transfer(bot, trigger.nick, 'SpiceBank', cluefee) == 1:
        bankbalance = Spicebucks.bank(bot, instigator)
        pointsworth = (int(pointsworth*bankbalance)) + 5
        pointsvalue = str(pointsworth)
        osd(bot, trigger.sender, 'say', trigger.nick + " paid " + str(cluefee) + " spicebucks and started a game of clue.")
        botusersarray = get_database_value(bot, bot.nick, 'botusers') or []
        for u in bot.users:
            if u in botusersarray and u != bot.nick:
                players.append(u)
        random.shuffle(rooms)
        random.shuffle(weapons)
        random.shuffle(players)
        if rooms[0] == 'secret passage':
            osd(bot, trigger.sender, 'say', players[2] + " evaded " + players[0] + " by using the secret passage. So " + players[0] + " killed " + players[1] + " with the " + weapons[0] + " instead.")
        else:
            osd(bot, trigger.sender, 'say', players[0] + " killed " + players[1] + " in the " + rooms[0] + " with the " + weapons[0] + ".")
        if target:
            if suspect:
                if suspect == 'killer' and target == players[0]:
                    osd(bot, trigger.sender, 'say', 'You guessed the killer correctly!')
                    osd(bot, trigger.sender, 'say', bot.nick + ' gives ' + pointsvalue + ' Spicebucks to ' + instigator)
                    Points.addpoints(bot, instigator, pointsworth)
                elif suspect == 'killed' and target == players[1]:
                    osd(bot, trigger.sender, 'say', 'You guessed the person murdered!')
                    osd(bot, trigger.sender, 'say', bot.nick + ' gives ' + pointsvalue + 'Spicebucks to ' + instigator)
                    Spicebucks.spicebucks(bot, instigator, 'plus', pointsworth)
        elif target and target == players[0]:
            osd(bot, trigger.sender, 'say', 'You guessed the killer correctly!')
            osd(bot, trigger.sender, 'say', bot.nick + ' gives ' + pointsvalue + ' Spicebucks to' + instigator)
            Spicebucks.spicebucks(bot, instigator, 'plus', pointsworth)
        if players[0] == trigger.nick:
            osd(bot, trigger.sender, 'say', 'You were the killer.')

            if pointsworth > bankbalance:
                pointsworth = bankbalance
            Spicebucks.spicebucks(bot, instigator, 'minus', pointsworth)
            osd(bot, trigger.sender, 'say', bot.nick + ' takes ' + pointsvalue + ' Spicebucks from ' + instigator)
    else:
        osd(bot, instigator, 'priv', "You need " + str(cluefee) + " spicebucks to use this command.")
