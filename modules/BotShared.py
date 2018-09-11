#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import datetime
import arrow
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
import sys
import re
import fnmatch
import random
import urllib
from os.path import exists
reload(sys)
sys.setdefaultencoding('utf-8')


osd_limit = 420  # Ammount of text allowed to display per line

devbot = 'dev'  # If using a development bot and want to bypass commands, this is what the bots name ends in
botdevteam = ['deathbybandaid', 'DoubleD', 'Mace_Whatdo', 'dysonparkes', 'PM', 'under_score']


# This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot, trigger, commandused):

    # Enable Status default is 1 = don't run
    enablestatus = 1

    # Custom args
    try:
        triggerargsarray = spicemanip(bot, trigger.group(2), 'create')
    except IndexError:
        triggerargsarray = spicemanip(bot, trigger.group(1), 'create')

    # Dyno Classes
    botcom = class_create('bot')
    instigator = class_create('instigator')
    instigator.default = trigger.nick
    botcom.instigator = trigger.nick

    # time
    botcom.now = time.time()

    # User
    botcom = bot_command_users(bot, botcom)

    # Channels
    botcom = bot_command_channels(bot, botcom, trigger)

    # User was Blocked by a bot.admin or an OP
    blockedusersarray = get_database_value(bot, botcom.channel_current, 'users_blocked') or []
    if instigator.default in blockedusersarray:
        osd(bot, instigator.default, 'notice', "It looks like you have been blocked from using commands in " + botcom.channel_current+".")
        return enablestatus, triggerargsarray, botcom, instigator

    # devmode bypass
    devenabledchannels = get_database_value(bot, bot.nick, 'channels_dev') or []
    if botcom.channel_current in devenabledchannels:
        enablestatus = 0
        return enablestatus, triggerargsarray, botcom, instigator

    # Channel activated status
    if botcom.channel_current.startswith("#"):
        channelmodulesarray = get_database_value(bot, botcom.channel_current, 'modules_enabled') or []
        if commandused not in channelmodulesarray:
            if botcom.instigator in botcom.opadmin:
                adjust_database_array(bot, botcom.channel_current, commandused, 'modules_enabled', 'add')
            else:
                osd(bot, instigator.default, 'notice', "it looks like the " + str(commandused) + " command has not been enabled in " + botcom.channel_current+".")
                return enablestatus, triggerargsarray, botcom, instigator

    # Bot Enabled Status (botcom.now in an array)
    botusersarray = get_database_value(bot, bot.nick, 'botusers') or []

    if instigator.default not in botcom.users_all:
        osd(bot, instigator.default, 'notice', "you have to run `" + bot.nick + " on` to allow her to listen to you. For help, see the wiki at https://github.com/SpiceBot/sopel-modules/wiki/Using-the-Bot.")
        return enablestatus, triggerargsarray, botcom, instigator

    enablestatus = 0
    increment_counter(bot, trigger, commandused)

    # Send Status Forward

    return enablestatus, triggerargsarray, botcom, instigator


"""
###################################################################
# Below This Line are Shared Functions
###################################################################
"""

"""
##############
# Bot basics #
##############
"""


# Bot Nicks
def bot_config_names(bot):
    config_listing = []
    networkname = str(bot.config.core.user.split("/", 1)[1] + "/")
    validconfigsdir = str("/home/spicebot/.sopel/" + bot.nick + "/System-Files/Configs/" + networkname)
    for filename in os.listdir(validconfigsdir):
        filenameminuscfg = str(filename).replace(".cfg", "")
        config_listing.append(filenameminuscfg)
    return config_listing


# Outputs Nicks with correct capitalization
def actualname(bot, nick):
    nick_actual = str(nick)
    for u in bot.users:
        if u.lower() == str(nick).lower():
            nick_actual = u
    return nick_actual


def nick_actual(bot, nick):
    nick_actual = str(nick)
    for u in bot.users:
        if u.lower() == str(nick).lower():
            nick_actual = u
    return nick_actual


def bot_command_users(bot, botcom):
    botcom.opadmin, botcom.owner, botcom.chanops, botcom.chanvoice, botcom.botadmins, botcom.users_current = [], [], [], [], [], []

    for user in bot.users:
        botcom.users_current.append(str(user))
    adjust_database_array(bot, 'channel', botcom.users_current, 'users_all', 'add')
    botcom.users_all = get_database_value(bot, 'channel', 'users_all') or []

    for user in botcom.users_current:

        if user in bot.config.core.owner:
            botcom.owner.append(user)

        if user in bot.config.core.admins:
            botcom.botadmins.append(user)
            botcom.opadmin.append(user)

        for channelcheck in bot.channels:
            try:
                if bot.privileges[channelcheck][user] == OP:
                    botcom.chanops.append(user)
                    botcom.opadmin.append(user)
            except KeyError:
                dummyvar = 1
            try:
                if bot.privileges[channelcheck][user] == VOICE:
                    botcom.chanvoice.append(user)
            except KeyError:
                dummyvar = 1

    return botcom


def bot_command_channels(bot, botcom, trigger):
    botcom.channel_current = trigger.sender
    if not botcom.channel_current.startswith("#"):
        botcom.channel_priv = 1
        botcom.channel_real = 0
    else:
        botcom.channel_priv = 0
        botcom.channel_real = 1
    botcom.service = bot.nick
    botcom.channel_list = []
    for channel in bot.channels:
        botcom.channel_list.append(channel)
    return botcom


def special_users(bot):
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = [], [], [], [], []
    for channel in bot.channels:
        for u in bot.users:
            allusersinroomarray.append(u)
            if u != bot.nick:

                try:
                    if u.lower() in bot.config.core.owner.lower():
                        botownerarray.append(u)
                except KeyError:
                    dumbyvar = 1

                try:
                    if bot.privileges[channel.lower()][u.lower()] == OP:
                        operatorarray.append(u)
                except KeyError:
                    dumbyvar = 1

                try:
                    if bot.privileges[channel.lower()][u.lower()] == VOICE:
                        voicearray.append(u)
                except KeyError:
                    dumbyvar = 1

                try:
                    if u in bot.config.core.admins:
                        adminsarray.append(u)
                except KeyError:
                    dumbyvar = 1
    return botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray


"""
###########
# Module Counters #
###########
"""


def increment_counter(bot, trigger, commandused):
    instigator = trigger.nick  # Who to increment for
    channel_current = trigger.sender  # Channel to increment for
    adjust_database_value(bot, channel_current, str(commandused + "moduleusage"), 1)  # Channel usage of specific module
    adjust_database_value(bot, channel_current, "spicebottotalusage", 1)  # Channel usage of bot overall
    adjust_database_value(bot, instigator, str(commandused + "moduleusage"), 1)  # User usage of specific module
    adjust_database_value(bot, instigator, "spicebottotalusage", 1)  # User usage of bot overall


"""
##################
# Check for target #
##################
"""


def targetcheck(bot, botcom, target, instigator):
    # Guilty until proven Innocent
    validtarget = 0  # 0 = invalid, 1 = valid 2 = instigator, 3 = bot, 4 =offline
    validtargetmsg = []
    target = target.lower()

    # Target is instigator
    if target == instigator.default:
        validtarget = 2
        validtargetmsg.append("Target is instigator")
        return validtarget, validtargetmsg

    if target == bot.nick:
        validtarget = 3
        validtargetmsg.append("Target is a bot")
        return validtarget, validtargetmsg
        # offline
        # if target not in [x.lower() for x in botcom.users_current] and target in [x.lower() for x in botcom.users_all]:

    # Null Target
    if not target:
        validtarget = 0
        validtargetmsg.append("You must specify a target.")
        return validtarget, validtargetmsg
    if target not in [x.lower() for x in botcom.users_current] and target in [x.lower() for x in botcom.users_all]:
        validtarget = 4
        realnick = nick_actual(bot, target)
        validtargetmsg.append(realnick + " is currently offline")
        return validtarget, validtargetmsg
    if target in [x.lower() for x in botcom.users_current]:
        validtarget = 1
        realnick = nick_actual(bot, target)
        validtargetmsg.append(realnick + " is currently online")
        return validtarget, validtargetmsg
    else:
        validtarget = 0
        validtargetmsg.append(target + " is invalid user")
        return validtarget, validtargetmsg


####################
# EASY targetcheck #
####################


def easytargetcheck(bot, botcom, target, instigator):
    # Guilty until proven Innocent
    validtarget = 'false'  # 0 = invalid, 1 = valid 2 = instigator, 3 = bot, 4 =offline
    target = target.lower()

    # Target is instigator
    if target == instigator:
        validtarget = 'instigator'
        return validtarget

    if target == bot.nick:
        validtarget = 'bot'
        return validtarget

    # Null Target
    if not target:
        validtarget = 'false'
        return validtarget
    if target not in [x.lower() for x in botcom.users_current] and target in [x.lower() for x in botcom.users_all]:
        validtarget = 'offline'
        realnick = nick_actual(bot, target)
        return validtarget
    if target in [x.lower() for x in botcom.users_current]:
        validtarget = 'online'
        realnick = nick_actual(bot, target)
        return validtarget
    else:
        validtarget = 'true'
        return validtarget


"""
##############
# Fix unicode in strings #
##############
"""


def unicode_string_cleanup(string):
    for r in (("\u2013", "-"), ("\u2019", "'"), ("\u2026", "...")):
        string = string.replace(*r)
    return string


def quote(string, safe='/'):
    # modified urllib2.quote that handles unicode properly
    if sys.version_info.major < 3:
        if isinstance(string, unicode):
            string = string.encode('utf8')
        string = urllib.quote(string, safe.encode('utf8'))
    else:
        string = urllib.parse.quote(str(string), safe)
    return string


"""
#####
# Time #
#####
"""


def enoughdaysbetween(earlydate, laterdate, numberofdays):
    datea = arrow.get(laterdate)
    dateb = arrow.get(earlydate)
    timepassed = datea - dateb
    dayspassed = timepassed.days
    if timepassed.days > int(numberofdays):
        longenough = 1
    else:
        longenough = 0
    return longenough


def get_timesince(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey) or 0
    return abs(now - int(last))


def get_timeuntil(now, futuretime):
    a = arrow.get(now)
    b = arrow.get(futuretime)
    timecompare = (b.humanize(a, granularity='auto'))
    return timecompare


def hours_minutes_seconds(countdownseconds):
    time = float(countdownseconds)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = ''
    timearray = ['hour', 'minute', 'second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg


def humanized_time(countdownseconds):
    time = float(countdownseconds)
    year = time // (365 * 24 * 3600)
    time = time % (365 * 24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = ''
    timearray = ['year', 'day', 'hour', 'minute', 'second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg


def hours_minutes_secondsold(countdownseconds):
    time = float(countdownseconds)
    year = time // (365 * 24 * 3600)
    time = time % (365 * 24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = ''
    timearray = ['year', 'day', 'hour', 'minute', 'second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg


"""
######
# Tools #
######
"""


def diceroll(howmanysides):
    diceroll = randint(0, howmanysides)
    return diceroll


"""
#######
# Database #
#######
"""


# Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value


# set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)


# set a value to None
def reset_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)


# add or subtract from current value
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))


# array stored in database length
def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal


# array stored in database, add or remove elements
def adjust_database_array(bot, nick, entries, databasekey, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    reset_database_value(bot, nick, databasekey)
    adjustarray = []
    if adjustmentdirection == 'add':
        for y in entries:
            if y not in adjustarraynew:
                adjustarraynew.append(y)
    elif adjustmentdirection == 'del':
        for y in entries:
            if y in adjustarraynew:
                adjustarraynew.remove(y)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        reset_database_value(bot, nick, databasekey)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)


def database_initialize(bot, nick, array, database):
    databasekey = str(database)
    existingarray = get_database_value(bot, bot.nick, databasekey)
    if not existingarray:
        arraycount = (len(array) - 1)
        i = 0
        while (i <= arraycount):
            inputstring = array[i]
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            i = i + 1


"""
# Sayings Functions
"""


def sayingsmodule(bot, databasekey, inputarray, thingtodo):
    """Handle the creation and manipulation of modules that return sayings."""
    response = "Something went wrong. Oops."
    inputstring = spicemanip(bot, inputarray, '2+')
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    if thingtodo == "initialise":
        database_initialize(bot, bot.nick, inputarray, databasekey)
    elif thingtodo == "add":
        if inputstring not in existingarray:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            response = "Added to database."
        else:
            response = "That is already in the database."
    elif thingtodo == "remove" or thingtodo == 'del':
        if inputstring not in existingarray:
            response = "That was not found in the database."
        else:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'del')
            response = "Removed from database."
    elif thingtodo == "count":
        messagecount = len(existingarray)
        response = "I'm seeing " + str(messagecount) + " responses in the database."
    elif thingtodo == "last":
        response = spicemanip(bot, existingarray, "last") or "I appear to have nothing for that."
    else:
        response = spicemanip(bot, existingarray, "random") or ''
        if response == '':
            response = "I'm afraid I couldn't find an entry for that."
    return response


def sayingscheck(bot, databasekey):
    """Check that there are responses for the given key."""
    saying_entries = get_database_value(bot, bot.nick, databasekey) or []
    saying_entrycount = len(saying_entries)
    if saying_entrycount != 0:
        return True
    else:
        return False


"""
Get line from raw text site.
"""


def randomline(bot, address):
    """Retrieve random line from given raw file."""
    htmlfile = urllib.urlopen(address)
    lines = htmlfile.read().splitlines()
    myline = random.choice(lines)
    if not myline or myline == '\n':
        myline = randomline()
    return myline


"""
On Screen Text
"""


def osd(bot, target_array, text_type_array, text_array):

    # if text_array is a string, make it an array
    textarraycomplete = []
    if not isinstance(text_array, list):
        textarraycomplete.append(text_array)
    else:
        for x in text_array:
            textarraycomplete.append(x)

    # if target_array is a string, make it an array
    texttargetarray = []
    if not isinstance(target_array, list):
        if not str(target_array).startswith("#"):
            target_array = nick_actual(bot, str(target_array))
        texttargetarray.append(target_array)
    else:
        for target in target_array:
            if not str(target).startswith("#"):
                target = nick_actual(bot, str(target))
            texttargetarray.append(target)

    # Handling for text_type
    texttypearray = []
    if not isinstance(text_type_array, list):
        for i in range(len(texttargetarray)):
            texttypearray.append(str(text_type_array))
    else:
        for x in text_type_array:
            texttypearray.append(str(x))
    text_array_common = max(((item, texttypearray.count(item)) for item in set(texttypearray)), key=lambda a: a[1])[0]

    # make sure len() equals
    if len(texttargetarray) > len(texttypearray):
        while len(texttargetarray) > len(texttypearray):
            texttypearray.append(text_array_common)
    elif len(texttargetarray) < len(texttypearray):
        while len(texttargetarray) < len(texttypearray):
            texttargetarray.append('osd_error_handle')

    # Rebuild the text array to ensure string lengths

    for target, text_type in zip(texttargetarray, texttypearray):

        if target == 'osd_error_handle':
            dont_say_it = 1
        else:

            # Text array
            temptextarray = []

            # Notice handling
            if text_type == 'notice':
                temptextarray.insert(0, target + ", ")
                # temptextarray.append(target + ", ")
            for part in textarraycomplete:
                temptextarray.append(part)

            # 'say' can equal 'priv'
            if text_type == 'say' and not str(target).startswith("#"):
                text_type = 'priv'

            # Make sure no individual string ins longer than it needs to be
            currentstring = ''
            texttargetarray = []
            for textstring in temptextarray:
                if len(textstring) > osd_limit:
                    chunks = textstring.split()
                    for chunk in chunks:
                        if currentstring == '':
                            currentstring = chunk
                        else:
                            tempstring = str(currentstring + " " + chunk)
                            if len(tempstring) <= osd_limit:
                                currentstring = tempstring
                            else:
                                texttargetarray.append(currentstring)
                                currentstring = chunk
                    if currentstring != '':
                        texttargetarray.append(currentstring)
                else:
                    texttargetarray.append(textstring)

            # Split text to display nicely
            combinedtextarray = []
            currentstring = ''
            for textstring in texttargetarray:
                if currentstring == '':
                    currentstring = textstring
                elif len(textstring) > osd_limit:
                    if currentstring != '':
                        combinedtextarray.append(currentstring)
                        currentstring = ''
                    combinedtextarray.append(textstring)
                else:
                    tempstring = currentstring + "   " + textstring
                    if len(tempstring) <= osd_limit:
                        currentstring = tempstring
                    else:
                        combinedtextarray.append(currentstring)
                        currentstring = textstring
            if currentstring != '':
                combinedtextarray.append(currentstring)

            # display
            textparts = len(combinedtextarray)
            textpartsleft = textparts
            for combinedline in combinedtextarray:
                if text_type == 'action' and textparts == textpartsleft:
                    bot.action(combinedline, target)
                elif str(target).startswith("#"):
                    bot.msg(target, combinedline)
                elif text_type == 'notice' or text_type == 'priv':
                    bot.notice(combinedline, target)
                elif text_type == 'say':
                    bot.say(combinedline)
                else:
                    bot.say(combinedline)
                textpartsleft = textpartsleft - 1


"""
Array/List/String Manipulation
"""


"""
Array/List/String Manipulation
"""


# Legacy
def get_trigger_arg(bot, inputs, outputtask, output_type='default'):
    return spicemanip(bot, inputs, outputtask, output_type)


# Hub
def spicemanip(bot, inputs, outputtask, output_type='default'):

    mainoutputtask, suboutputtask = None, None

    # Input needs to be a list, but don't split a word into letters
    if not inputs:
        inputs = []
    if not isinstance(inputs, list):
        inputs = list(inputs.split(" "))
        inputs = [x for x in inputs if x and x not in ['', ' ']]
        inputs = [inputspart.strip() for inputspart in inputs]

    # Create return
    if outputtask == 'create':
        return inputs

    # Make temparray to preserve original order
    temparray = []
    for inputpart in inputs:
        temparray.append(inputpart)
    inputs = temparray

    # Convert outputtask to standard
    if outputtask in [0, 'complete']:
        outputtask = 'string'
    elif str(outputtask).isdigit():
        mainoutputtask, outputtask = int(outputtask), 'number'
    elif "^" in str(outputtask):
        mainoutputtask = str(outputtask).split("^", 1)[0]
        suboutputtask = str(outputtask).split("^", 1)[1]
        outputtask = 'rangebetween'
    elif str(outputtask).startswith("split_"):
        mainoutputtask = str(outputtask).replace("split_", "")
        outputtask = 'split'
    elif str(outputtask).endswith(tuple(["!", "+", "-", "<", ">"])):
        mainoutputtask = str(outputtask)
        if str(outputtask).endswith("!"):
            outputtask = 'exclude'
        if str(outputtask).endswith("+"):
            outputtask = 'incrange_plus'
        if str(outputtask).endswith("-"):
            outputtask = 'incrange_minus'
        if str(outputtask).endswith(">"):
            outputtask = 'excrange_plus'
        if str(outputtask).endswith("<"):
            outputtask = 'excrange_minus'
        for r in (("!", ""), ("+", ""), ("-", ""), ("<", ""), (">", "")):
            mainoutputtask = mainoutputtask.replace(*r)

    if outputtask == 'string':
        returnvalue = inputs
    else:
        try:
            returnvalue = eval('spicemanip_' + outputtask + '(bot, inputs, outputtask, mainoutputtask, suboutputtask)')
        except NameError:
            returnvalue = ''

    # default return if not specified
    if output_type == 'default':
        if outputtask in [
                            'string', 'number', 'rangebetween', 'exclude', 'random',
                            'incrange_plus', 'incrange_minus', 'excrange_plus', 'excrange_minus'
                            ]:
            output_type = 'string'
        elif outputtask in ['count']:
            output_type = 'dict'

    # verify output is correct
    if output_type == 'string':
        if isinstance(returnvalue, list):
            returnvalue = ' '.join(returnvalue)
    elif output_type in ['list', 'array']:
        if not isinstance(returnvalue, list):
            returnvalue = list(returnvalue.split(" "))
            returnvalue = [x for x in returnvalue if x and x not in ['', ' ']]
            returnvalue = [inputspart.strip() for inputspart in returnvalue]
    return returnvalue


# split list by string
def spicemanip_split(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    split_array = []
    restring = ' '.join(inputs)
    if mainoutputtask not in inputs:
        split_array = [restring]
    else:
        split_array = restring.split(mainoutputtask)
    split_array = [x for x in split_array if x and x not in ['', ' ']]
    split_array = [inputspart.strip() for inputspart in split_array]
    return split_array


# dedupe list
def spicemanip_dedupe(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    newlist = []
    for inputspart in inputs:
        if inputspart not in newlist:
            newlist.append(inputspart)
    return newlist


# Sort list
def spicemanip_sort(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    return sorted(inputs)


# count items in list, return dictionary
def spicemanip_count(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    returndict = dict()
    if inputs == []:
        return returndict
    uniqueinputitems, uniquecount = [], []
    for inputspart in inputs:
        if inputspart not in uniqueinputitems:
            uniqueinputitems.append(inputspart)
    for uniqueinputspart in uniqueinputitems:
        count = 0
        for ele in inputs:
            if (ele == uniqueinputspart):
                count += 1
        uniquecount.append(count)
    for inputsitem, unumber in zip(uniqueinputitems, uniquecount):
        returndict[inputsitem] = unumber
    return returndict


# random item from list
def spicemanip_random(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    randomselectlist = []
    for temppart in inputs:
        randomselectlist.append(temppart)
    while len(randomselectlist) > 1:
        random.shuffle(randomselectlist)
        randomselect = randomselectlist[random.randint(0, len(randomselectlist) - 1)]
        randomselectlist.remove(randomselect)
    randomselect = randomselectlist[0]
    return randomselect


# remove random item from list
def spicemanip_exrandom(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return []
    randremove = spicemanip_random(bot, inputs, outputtask, mainoutputtask, suboutputtask)
    inputs.remove(randremove)
    return inputs


# Convert list into lowercase
def spicemanip_lower(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return [inputspart.lower() for inputspart in inputs]


# Convert list to uppercase
def spicemanip_upper(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return [inputspart.upper() for inputspart in inputs]


# Convert list to uppercase
def spicemanip_title(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return [inputspart.title() for inputspart in inputs]


# Reverse List Order
def spicemanip_reverse(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return []
    return inputs[::-1]


# comma seperated list
def spicemanip_list(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return ', '.join(str(x) for x in inputs)


# comma seperated list with and
def spicemanip_andlist(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    if len(inputs) < 2:
        return ' '.join(inputs)
    lastentry = str("and " + str(inputs[len(inputs) - 1]))
    del inputs[-1]
    inputs.append(lastentry)
    if len(inputs) == 2:
        return ' '.join(inputs)
    return ', '.join(str(x) for x in inputs)


# comma seperated list with or
def spicemanip_orlist(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    if len(inputs) < 2:
        return ' '.join(inputs)
    lastentry = str("or " + str(inputs[len(inputs) - 1]))
    del inputs[-1]
    inputs.append(lastentry)
    if len(inputs) == 2:
        return ' '.join(inputs)
    return ', '.join(str(x) for x in inputs)


# exclude number
def spicemanip_exclude(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    del inputs[int(mainoutputtask) - 1]
    return ' '.join(inputs)


# Convert list to string
def spicemanip_string(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return ' '.join(inputs)


# Get number item from list
def spicemanip_number(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    elif len(inputs) == 1:
        return inputs[0]
    elif int(mainoutputtask) > len(inputs) or int(mainoutputtask) < 0:
        return ''
    else:
        return inputs[int(mainoutputtask) - 1]


# Get Last item from list
def spicemanip_last(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return inputs[len(inputs) - 1]


# range between items in list
def spicemanip_rangebetween(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    if not str(mainoutputtask).isdigit() or not str(suboutputtask).isdigit():
        return ''
    mainoutputtask, suboutputtask = int(mainoutputtask), int(suboutputtask)
    if suboutputtask == mainoutputtask:
        return spicemanip_number(bot, inputs, outputtask, mainoutputtask, suboutputtask)
    if suboutputtask < mainoutputtask:
        mainoutputtask, suboutputtask = suboutputtask, mainoutputtask
    if mainoutputtask < 0:
        mainoutputtask = 1
    if suboutputtask > len(inputs):
        suboutputtask = len(inputs)
    newlist = []
    for i in range(mainoutputtask, suboutputtask + 1):
        newlist.append(str(spicemanip_number(bot, inputs, outputtask, i, suboutputtask)))
    if newlist == []:
        return ''
    return ' '.join(newlist)


# Forward Range includes index number
def spicemanip_incrange_plus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, int(mainoutputtask), len(inputs))


# Reverse Range includes index number
def spicemanip_incrange_minus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, 1, int(mainoutputtask))


# Forward Range excludes index number
def spicemanip_excrange_plus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, int(mainoutputtask) + 1, len(inputs))


# Reverse Range excludes index number
def spicemanip_excrange_minus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, 1, int(mainoutputtask) - 1)


def array_compare(bot, indexitem, arraytoindex, arraytocompare):
    item = ''
    for x, y in zip(arraytoindex, arraytocompare):
        if x == indexitem:
            item = y
    return item


def array_arrangesort(bot, sortbyarray, arrayb):
    sortbyarray, arrayb = (list(x) for x in zip(*sorted(zip(sortbyarray, arrayb), key=itemgetter(0))))
    return sortbyarray, arrayb


"""
# Empty Classes
"""


def class_create(classname):
    compiletext = """
        def __init__(self):
            self.default = str(self.__class__.__name__)
        def __repr__(self):
            return repr(self.default)
        def __str__(self):
            return str(self.default)
        def __iter__(self):
            return str(self.default)
        pass
        """
    exec(compile("class class_" + str(classname) + ": " + compiletext, "", "exec"))
    newclass = eval('class_'+classname+"()")
    return newclass


"""
# File functions
"""


def txtFileCount(path):
    with open(path) as f:
        line_count = 0
        for line in f:
            line_count += 1

    return line_count


def fileLine(path, number):
    maxLines = txtCount(path)
    if number < 0:
        number = 1
    if number > maxLines:
        number = 1
    file = open(path, "r")
    i = 1
    while i <= number:
        line = file.readline()
        i = i + 1
    return line


def randomFileLine(path):
    maxLines = txtCount(path)
    rand = random.randint(1, maxLines)
    file = open(path, "r")
    i = 1
    while i <= rand:
        line = file.readline()
        i = i + 1
    return line
