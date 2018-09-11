#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('vote', 'rate', 'poll')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'vote')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Take votes and create polls."""
    now = time.time()
    commandused = trigger.group(1)
    choice = spicemanip(bot, triggerargsarray, 1)
    player = trigger.nick
    if commandused == 'vote':
        if choice == 'results':
            getvotes(bot)
        elif choice == 'settime' and trigger.admin:
            timing = spicemanip(bot, triggerargsarray, 2)
            if timing.isdigit():
                timing = int(timing)
                set_database_value(bot, bot.nick, 'votetimer', timing)
                osd(bot, player, 'priv', "Voting delay set to 10 plus" + str(timing))
            else:
                osd(bot, player, 'priv', "Please enter a valid number")
        else:
            yesvotes = 0
            novotes = 0
            ratings = []
            pollchoice = []
            voters = get_database_value(bot, bot.nick, 'voters') or []
            if player not in voters:
                if choice == 'yes' or choice == 'ya':
                    osd(bot, player, 'priv', "Your yes vote has been recorded")
                    adjust_database_value(bot, bot.nick, 'yesvotes', 1)
                    adjust_database_array(bot, bot.nick, player, 'voters', 'add')
                    set_database_value(bot, bot.nick, 'voting', 1)
                    set_database_value(bot, bot.nick, 'voting', 'True')
                    set_database_value(bot, bot.nick, 'votechannel', trigger.sender)
                    set_database_value(bot, bot.nick, 'votingstart', now)
                elif choice == 'no' or choice == 'na':
                    osd(bot, player, 'priv', "Your no vote has been recorded")
                    adjust_database_value(bot, bot.nick, 'novotes', 1)
                    adjust_database_array(bot, bot.nick, player, 'voters', 'add')
                    set_database_value(bot, bot.nick, 'voting', 'True')
                    set_database_value(bot, bot.nick, 'votechannel', trigger.sender)
                    set_database_value(bot, bot.nick, 'votingstart', now)

                else:
                    osd(bot, trigger.sender, 'say', "Vote yes or no")
            else:
                osd(bot, player, 'priv', "You have already voted")

    elif commandused == 'rate':
        raters = get_database_value(bot, bot.nick, 'raters') or []
        if not choice:
            osd(bot, trigger.sender, 'say', "Rate on scale of -10 through 10")
        elif choice == 'results':
            getrating(bot)
        elif choice == 'settime' and trigger.admin:
            timing = spicemanip(bot, triggerargsarray, 2)
            if timing.isdigit():
                timing = int(timing)
                set_database_value(bot, bot.nick, 'ratetimer', timing)
                osd(bot, player, 'priv', "Rating delay set to 10 plus" + str(timing))
        else:
            if player not in raters:
                if isfloat(choice):
                    choice = float(choice)
                    if choice > 10:
                        choice = 10
                    if choice < -10:
                        choice = -10
                    osd(bot, player, 'priv', "Your rating of " + str(choice) + " has been recorded")
                    adjust_database_array(bot, bot.nick, player, 'raters', 'add')
                    adjust_database_array(bot, bot.nick, choice, 'ratings', 'add')
                    set_database_value(bot, bot.nick, 'rating', 'True')
                    set_database_value(bot, bot.nick, 'ratechannel', trigger.sender)
                    set_database_value(bot, bot.nick, 'ratestart', now)
                else:
                    osd(bot, player, 'priv', str(choice) + " is not a number between -10 and 10")
            else:
                osd(bot, player, 'priv', "You already submitted a rating this round")

    elif commandused == 'poll':
        osd(bot, trigger.sender, 'say', "WIP")


def clearvoting(bot):
    reset_database_value(bot, bot.nick, 'novotes')
    reset_database_value(bot, bot.nick, 'yesvotes')
    reset_database_value(bot, bot.nick, 'voters')
    reset_database_value(bot, bot.nick, 'voting')
    reset_database_value(bot, bot.nick, 'votechannel')


def clearrating(bot):
    reset_database_value(bot, bot.nick, 'raters')
    reset_database_value(bot, bot.nick, 'ratings')
    reset_database_value(bot, bot.nick, 'ratechannel')


@sopel.module.interval(10)
def countdown(bot):
    isvote = get_database_value(bot, bot.nick, 'voting') or ''
    israte = get_database_value(bot, bot.nick, 'rating') or ''
    votetimeout = get_database_value(bot, bot.nick, 'votetimer')
    ratetimeout = get_database_value(bot, bot.nick, 'ratetimer')
    if isvote:
        if get_timesince(bot, bot.nick, 'votestart') > votetimeout:
            getvotes(bot)
    if israte:
        if get_timesince(bot, bot.nick, 'ratestart') > ratetimeout:
            getrating(bot)


def getvotes(bot):
    novotes = get_database_value(bot, bot.nick, 'novotes') or 0
    yesvotes = get_database_value(bot, bot.nick, 'yesvotes') or 0
    channel = get_database_value(bot, bot.nick, 'votechannel') or ''
    if not channel == '':
        dispmsg = str(yesvotes) + " votes for yes and " + str(novotes) + " no votes"
        osd(bot, trigger.sender, 'say', dispmsg)
        clearvoting(bot)


def getrating(bot):
    sum = 0
    ratings = get_database_value(bot, bot.nick, 'ratings')
    channel = get_database_value(bot, bot.nick, 'ratechannel') or ''
    if not channel == '':
        if ratings:
            for n in ratings:
                n = int(n)
                sum = sum + n
            average = sum / len(ratings)
            dispmsg = 'The average is ' + str(average)
            osd(bot, trigger.sender, 'say', dispmsg)
            clearrating(bot)
        else:
            dispmsg = 'No ratings found'
            clearrating(bot)
            osd(bot, trigger.sender, 'say', dispmsg)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
