#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import datetime
from sopel.tools import Identifier
from sopel.tools.time import get_timezone, format_time
from sopel.module import commands, rule, priority, thread
import sopel.module
from sopel import module, tools
from sopel.module import OP
from sopel.module import ADMIN
from sopel.module import VOICE
from sopel.module import event, rule
import time
import os
import sys, re
import fnmatch
import random
from os.path import exists

devbot = 'dev'
botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score']

JOINTIMEOUT = 60
LASTTIMEOUT = 60
TOOMANYTIMES = 7
OPTTIMEOUT = 1800
FINGERTIMEOUT = 1800
LASTTIMEOUT = 30
LASTTIMEOUTHOUR = 1800

## This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot,trigger):

    ## Custom args
    triggerargsarray = create_args_array(trigger.group(2))

    ## time
    now = time.time()

    ## used to circumvent
    commandused = trigger.group(1)
    allowedcommandsarray = ['duel','challenge']

    ## Get Name Of Channel
    botchannel = trigger.sender

    ## Nick of user operating command
    instigator = trigger.nick

    ## User's Bot Status
    instigatorbotstatus = get_database_value(bot, instigator, 'disenable')

    ## Enable Status default is 1 = don't run
    enablestatus = 1

    ## Get User's current total uses
    usertotal = get_database_value(bot, instigator, 'usertotal')

    ## When Did the user Join The room
    jointime = get_timesince(bot, instigator, 'jointime')

    ## When Did the User Last Use the bot
    lasttime = get_timesince(bot, instigator, 'lastusagetime')

    ## Has The user already been warned?
    warned = get_database_value(bot, instigator, 'hourwarned')

    ## Check user has spicebotenabled
    if not instigatorbotstatus and not warned:
        message = str(instigator + ", you have to run .spicebot on to allow her to listen to you. For help, see the wiki at https://github.com/SpiceBot/sopel-modules/wiki/Using-the-Bot.")
    elif not instigatorbotstatus and warned:
        message = str(instigator + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.")

    ## Make sure the user hasn't overdone the bot in the past hour
    elif instigatorbotstatus and usertotal > TOOMANYTIMES and botchannel.startswith("#") and not bot.nick.endswith('dev'):
        message = str(instigator + ", you must have used Spicebot more than " + str(TOOMANYTIMES) + " times this past hour.")

    ## Make sure the user hasn't just entered the room
    elif instigatorbotstatus and jointime <= JOINTIMEOUT and botchannel.startswith("#") and not bot.nick.endswith('dev'):
        jointimemath = int(JOINTIMEOUT - jointime)
        message = str(instigator + ", you need to wait " + str(jointimemath) + " seconds to use Spicebot.")

    ## Make users wait between uses
    elif instigatorbotstatus and lasttime <= LASTTIMEOUT and botchannel.startswith("#") and not bot.nick.endswith('dev') and commandused not in allowedcommandsarray:
        lasttimemath = int(LASTTIMEOUT - lasttime)
        message = str(instigator + ", you need to wait " + str(lasttimemath) + " seconds to use Spicebot.")

    ## if user passes ALL above checks, we'll run the module
    else:
        enablestatus = 0
        message = ''

        ## Update user total
        if botchannel.startswith("#") and not trigger.admin:
            adjust_database_value(bot, instigator, 'usertotal', '1')

    ## Update user's last use timestamp
    if botchannel.startswith("#") and not bot.nick.endswith('dev'):
        set_database_value(bot, instigator, 'lastusagetime', now)

    ## Add usage counter for counts
    adjust_database_value(bot, botchannel, str(commandused + "usage"), 1) ## Channel usage of specific module
    adjust_database_value(bot, botchannel, "spicebottotalusage", 1) ## Channel usage of bot overall
    adjust_database_value(bot, trigger.nick, str(commandused + "usage"), 1) ## User usage of specific module
    adjust_database_value(bot, trigger.nick, "spicebottotalusage", 1) ## User usage of bot overall

    ## message, if any
    osd(bot, trigger.sender, 'priv', message)

    ## Send Status Forward
    return enablestatus, triggerargsarray

#####################################################################################################################################
## Data collection
#####################################################################################################################################

## User data collection
@sopel.module.interval(1800)
def halfhour(bot):
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            set_database_value(bot, u, 'usertotal', None)
            set_database_value(bot, u, 'hourwarned', None)

## Don't let users use the bot the first minute after they join the room
@event('JOIN')
@rule('.*')
def waitaminute(bot, trigger):
    now = time.time()
    target = trigger.nick
    set_database_value(bot, target, 'jointime', now)
    lasttime = get_timesince(bot, target, 'lastusagetime')
    if not lasttime or lasttime < LASTTIMEOUTHOUR:
        bot.db.set_nick_value(target, 'spicebot_usertotal', None)
        bot.db.set_nick_value(target, 'spicebothour_warn', None)

## Log out bot.admin
@event('QUIT') ###need to verify if this is the same if a person looses connection or quits
@rule('.spicebotadmin*')
def logoutadmin(bot, trigger):
    botadmins = ['deathbybandaid']
    if trigger.nick in botadmins
    bot.db.set_nick_value(target, 'spicebot_admin', 'out')

## Verify nick is bot.admin and logged in
@event('JOIN') ###need to verify if this is the same if a person looses connection or quits
@rule('.spicebotadmin*')
def logoutadmin(bot, trigger):
    botadmins = ['deathbybandaid']
    loggedin = bot.db.get_nick_value(target, 'spicebot_admin')
    if trigger.nick not in botadmins or loggedin == 'out':
        bot.notify("Please log in before issuing spicebotadmin commands.")

### will need to add coding for adding a pin/password for the bot.admin
### will need to add verification in the .spicebotadmin command


## Autoblock users that
@sopel.module.interval(60)
def autoblock(bot):
    now = time.time()
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            usertotal = get_database_value(bot, u, 'usertotal')
            if usertotal > TOOMANYTIMES and not bot.nick.endswith('dev'):
                set_database_value(bot, u, 'lastopttime', now)
                set_database_value(bot, u, 'disenable', None)
                warned = get_database_value(bot, u, 'hourwarned')
                if not warned:
                    osd(bot, u, 'priv', ", your access to spicebot has been disabled for an hour. If you want to test her, use ##SpiceBotTest")
                    set_database_value(bot, u, 'hourwarned', 'true')

#####################################################################################################################################
## Below This Line are Shared Functions
#####################################################################################################################################

###################
## Special Users ##
###################

def special_users(bot):
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = [], [], [], [], []
    for channel in bot.channels:
        for u in bot.channels[channel.lower()].users:
            allusersinroomarray.append(u)
            udisenable = get_database_value(bot, u, 'disenable')
            if u != bot.nick and udisenable:
                if u.lower() in bot.config.core.owner.lower():
                    botownerarray.append(u)
                if bot.privileges[channel.lower()][u] == OP:
                    operatorarray.append(u)
                if bot.privileges[channel.lower()][u.lower()] == VOICE:
                    voicearray.append(u)
                if u in bot.config.core.admins:
                    adminsarray.append(u)
    return botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray, channel

##########
## ARGS ##
##########

def create_args_array(fullstring):
    triggerargsarray = []
    if fullstring:
        for word in fullstring.split():
            triggerargsarray.append(word)
    return triggerargsarray

def get_trigger_arg(triggerargsarray, number):
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    triggerarg = ''
    if "^" in str(number) or number == 0 or str(number).endswith("+") or str(number).endswith("-") or str(number).endswith("<") or str(number).endswith(">"):
        if str(number).endswith("+"):
            rangea = re.sub(r"\+", '', str(number))
            rangea = int(rangea)
            rangeb = totalarray
        elif str(number).endswith("-"):
            rangea = 1
            rangeb = re.sub(r"-", '', str(number))
            rangeb = int(rangeb) + 1
        elif str(number).endswith(">"):
            rangea = re.sub(r">", '', str(number))
            rangea = int(rangea) + 1
            rangeb = totalarray
        elif str(number).endswith("<"):
            rangea = 1
            rangeb = re.sub(r"<", '', str(number))
            rangeb = int(rangeb)
        elif "^" in str(number):
            rangea = number.split("^", 1)[0]
            rangeb = number.split("^", 1)[1]
            rangea = int(rangea)
            rangeb = int(rangeb) + 1
        elif number == 0:
            rangea = 1
            rangeb = totalarray
        if rangea <= totalarray:
            for i in range(rangea,rangeb):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif number == 'last':
        if totalarray > 1:
            totalarray = totalarray -2
            triggerarg = str(triggerargsarray[totalarray])
    elif str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
        for i in range(1,totalarray):
            if int(i) != int(number):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif number == 'random':
        if totalarray > 1:
            randomselected = random.randint(0,len(triggerargsarray) - 1)
            triggerarg = str(triggerargsarray [randomselected])
    elif number == 'list':
        for x in triggerargsarray:
            if triggerarg != '':
                triggerarg  = str(triggerarg  + ", " + x)
            else:
                triggerarg  = str(x)
    else:
        number = int(number) - 1
        try:
            triggerarg = triggerargsarray[number]
        except IndexError:
            triggerarg = ''
    return triggerarg

##############
## Database ##
##############

def get_database_value(bot, nick, databasekey):
    databasecolumn = str('spicebot_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)

def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str('spicebot_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))

def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal

def adjust_database_array(bot, nick, entry, databasekey, adjustmentdirection):
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    set_database_value(bot, nick, databasekey, None)
    adjustarray = []
    if adjustmentdirection == 'add':
        if entry not in adjustarraynew:
            adjustarraynew.append(entry)
    elif adjustmentdirection == 'del':
        if entry in adjustarraynew:
            adjustarraynew.remove(entry)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        set_database_value(bot, nick, databasekey, None)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)

############################
## Fix unicode in strings ##
############################

def unicode_string_cleanup(string):
    for r in (("\u2013", "-"), ("\u2019", "'"), ("\u2026", "...")):
        string = string.replace(*r)
    return string

##########
## Time ##
##########

def get_timesince(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey) or 0
    return abs(now - int(last))

###########
## Tools ##
###########

def diceroll(howmanysides):
    diceroll = randint(0, howmanysides)
    return diceroll
