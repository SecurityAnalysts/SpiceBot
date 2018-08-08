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

osd_limit = 420  # Ammount of text allowed to display per line

devbot = 'dev'  # If using a development bot and want to bypass commands, this is what the bots name ends in
botdevteam = ['deathbybandaid', 'DoubleD', 'Mace_Whatdo', 'dysonparkes', 'PM', 'under_score']


# This runs for every custom module and decides if the module runs or not
def spicebot_prerun(bot, trigger, commandused):

    # Enable Status default is 1 = don't run
    enablestatus = 1

    # Custom args
    try:
        triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    except IndexError:
        triggerargsarray = get_trigger_arg(bot, trigger.group(1), 'create')

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


def sayingsmodule(bot, databasekey, triggerargsarray, thingtodo):
    """Handle the creation and manipulation of modules that return sayings."""
    # add, remove, last, count, list, initialise?
    resultstring = "test"
    return resultstring


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
            textarraycomplete.append(str(x))

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
                    tempstring = str(currentstring + "   " + textstring)
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


# Hub
def get_trigger_arg(bot, inputs, outputtask):
    # Create
    if outputtask == 'create':
        return create_array(bot, inputs)
    # reverse
    if outputtask == 'reverse':
        return reverse_array(bot, inputs)
    # Comma Seperated List
    if outputtask == 'list':
        return list_array(bot, inputs)
    if outputtask == 'andlist':
        return andlist_array(bot, inputs)
    if outputtask == 'orlist':
        return orlist_array(bot, inputs)
    if outputtask == 'random':
        return random_array(bot, inputs)
    # Last element
    if outputtask == 'last':
        return last_array(bot, inputs)
    # Complete String
    if outputtask == 0 or outputtask == 'complete' or outputtask == 'string':
        return string_array(bot, inputs)
    # Number
    if str(outputtask).isdigit():
        return number_array(bot, inputs, outputtask)
    # Exlude from array
    if str(outputtask).endswith("!"):
        return excludefrom_array(bot, inputs, outputtask)
    # Inclusive range starting at
    if str(outputtask).endswith("+"):
        return incrange_plus_array(bot, inputs, outputtask)
    # Inclusive range ending at
    if str(outputtask).endswith("-"):
        return incrange_minus_array(bot, inputs, outputtask)
    # Exclusive range starting at
    if str(outputtask).endswith(">"):
        return excrange_plus_array(bot, inputs, outputtask)
    # Exclusive range ending at
    if str(outputtask).endswith("<"):
        return excrange_minus_array(bot, inputs, outputtask)
    # Range Between Numbers
    if "^" in str(outputtask):
        return rangebetween_array(bot, inputs, outputtask)
    string = ''
    return string


# Convert String to array
def create_array(bot, inputs):
    if isinstance(inputs, list):
        string = ''
        for x in inputs:
            if string != '':
                string = str(string + " " + str(x))
            else:
                string = str(x)
        inputs = string
    outputs = []
    if inputs:
        for word in inputs.split():
            outputs.append(word.encode('ascii', 'ignore').decode('ascii'))
    return outputs


# Convert Array to String
def string_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    for x in inputs:
        if string != '':
            string = str(string + " " + str(x))
        else:
            string = str(x)
    return string


# output reverse order
def reverse_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    if len(inputs) == 1:
        return inputs
    outputs = []
    if inputs == []:
        return outputs
    for d in inputs:
        outputs.append(d)
    outputs.reverse()
    return outputs


# Comma Seperated List
def list_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    for x in inputs:
        if string != '':
            string = str(str(string) + ", " + str(x))
        else:
            string = str(x)
    return string


# Comma Seperated List
def andlist_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    inputnumberstart = len(inputs)
    inputsnumber = len(inputs)
    for x in inputs:
        if inputsnumber == 1 and inputsnumber != inputnumberstart:
            string = str(str(string) + ", and " + str(x))
        elif string != '':
            string = str(str(string) + ", " + str(x))
        else:
            string = str(x)
        inputsnumber = inputsnumber - 1
    return string


# Comma Seperated List
def orlist_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    inputnumberstart = len(inputs)
    inputsnumber = len(inputs)
    for x in inputs:
        if inputsnumber == 1 and inputsnumber != inputnumberstart:
            string = str(str(string) + ", or " + str(x))
        elif string != '':
            string = str(str(string) + ", " + str(x))
        else:
            string = str(x)
        inputsnumber = inputsnumber - 1
    return string


# Random element
def random_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    temparray = []
    for d in inputs:
        temparray.append(d)
    shuffledarray = random.shuffle(temparray)
    randomselected = random.randint(0, len(temparray) - 1)
    string = str(temparray[randomselected])
    return string


# Last element
def last_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    string = inputs[len(inputs)-1]
    return string


# select a number
def number_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if str(number).isdigit():
        numberadjust = int(number) - 1
        if numberadjust < len(inputs) and numberadjust >= 0:
            number = int(number) - 1
            string = inputs[number]
    return string


# range
def range_array(bot, inputs, rangea, rangeb):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    if int(rangeb) == int(rangea):
        return number_array(bot, inputs, rangeb)
    if int(rangeb) < int(rangea):
        tempa, tempb = rangeb, rangea
        rangea, rangeb = tempa, tempb
    if int(rangea) < 1:
        rangea = 1
    if int(rangeb) > len(inputs):
        return string
    for i in range(int(rangea), int(rangeb) + 1):
        arg = number_array(bot, inputs, i)
        if string != '':
            string = str(string + " " + arg)
        else:
            string = str(arg)
    return string


# exclude a number
def excludefrom_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
    if str(number).isdigit():
        for i in range(1, len(inputs)):
            if int(i) != int(number):
                arg = number_array(bot, inputs, i)
                if string != '':
                    string = str(string + " " + arg)
                else:
                    string = str(arg)
    return string


# range between
def rangebetween_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if "^" in str(number):
        rangea = number.split("^", 1)[0]
        rangeb = number.split("^", 1)[1]
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)


# inclusive forward
def incrange_plus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("+"):
        rangea = re.sub(r"\+", '', str(number))
        rangeb = len(inputs)
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)


# inclusive reverse
def incrange_minus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("-"):
        rangea = 1
        rangeb = re.sub(r"-", '', str(number))
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)


# excluding forward
def excrange_plus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith(">"):
        rangea = re.sub(r">", '', str(number))
        rangea = int(rangea) + 1
        rangeb = len(inputs)
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)


# excluding reverse
def excrange_minus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("<"):
        rangea = 1
        rangeb = re.sub(r"<", '', str(number))
        rangeb = int(rangeb) - 1
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)


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
