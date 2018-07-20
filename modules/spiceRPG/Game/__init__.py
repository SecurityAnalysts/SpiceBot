#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
# sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, ADMIN, VOICE, event, rule
from sopel.formatting import bold
import sopel
from sopel import module, tools, formatting
# Additional
import random
from random import randint
import time
import datetime
import re
import sys
import os
from os.path import exists
from num2words import num2words
from difflib import SequenceMatcher
from more_itertools import sort_together
from operator import itemgetter
import requests
from fake_useragent import UserAgent
from lxml import html
from statistics import mean
import itertools
import inspect
import pickle
# Game Folder
from .Global_Vars import *


"""
Triggers for usage
"""


@sopel.module.commands('rpga')
@sopel.module.thread(True)
def rpg_trigger_maina(bot, trigger):

    bot.say("saving")

    testclass = class_create('testclass')
    testclass.testclass = 'awesome'

    set_database_class(bot, bot.nick, 'classtest', testclass)


@sopel.module.commands('rpgb')
@sopel.module.thread(True)
def rpg_trigger_mainb(bot, trigger):

    bot.say("retrieving")

    savedclass = get_database_class(bot, bot.nick, 'classtest')

    bot.say(savedclass.testclass)


def get_database_class(bot, nick, databasekey):
    database_retrieve = get_database_value(bot, nick, databasekey) or 0
    if database_retrieve = o:
        class_value = class_create(databasekey)
        return class_value
    class_value = pickle.load(database_retrieve)
    return class_value


def set_database_class(bot, nick, databasekey, class_to_dump):
    dump_value = pickle.dumps(class_to_dump)
    set_database_value(bot, nick, databasekey, dump_value)


# Base command
@sopel.module.commands('rpg')
@sopel.module.thread(True)
def rpg_trigger_main(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    execute_start(bot, trigger, triggerargsarray)


"""
Command Processing
"""


def execute_start(bot, trigger, triggerargsarray):

    # RPG dynamic Class
    rpg = class_create('main')

    # Time when Module use started
    rpg.start = time.time()

    # instigator
    instigator = class_create('instigator')
    instigator.default = trigger.nick
    rpg.instigator = trigger.nick

    # Channel Listing
    rpg = rpg_command_channels(bot,rpg,trigger)

    # Bacic User List
    rpg = rpg_command_users(bot,rpg)

    # Commands list
    rpg = rpg_valid_commands_all(bot, rpg)  # TODO alt coms

    # TODO valid stats

    # Error Display System Create
    rpg_errors_start(bot, rpg)

    # Run the Process
    execute_main(bot, rpg, instigator, trigger, triggerargsarray)

    # Error Display System Display
    rpg_errors_end(bot, rpg)


def execute_main(bot, rpg, instigator, trigger, triggerargsarray):

    # Verify Game enabled in current channel
    if rpg.channel_current not in rpg.channels_game_enabled and rpg.channel_real:
        if rpg.channels_game_enabled == []:
            errors(bot, rpg, 'commands', 1, 1)
            if rpg.instigator not in rpg.botadmins:
                return
        else:
            errors(bot, rpg, 'commands', 2, 1)
            if rpg.instigator not in rpg.botadmins:
                return

    # No Empty Commands
    if triggerargsarray == []:
        user_capable_coms = []
        for vcom in rpg.valid_commands_all:
            if vcom in rpg_commands_valid_admin:
                if rpg.instigator in rpg.botadmins:
                    user_capable_coms.append(vcom)
            else:
                user_capable_coms.append(vcom)
        valid_commands_list = get_trigger_arg(bot, user_capable_coms, 'andlist')
        errors(bot, rpg, 'commands', 3, 1)
        return

    # Entire command string
    rpg.command_full_complete = get_trigger_arg(bot, triggerargsarray, 0)

    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    rpg.multi_com_list = []

    # Build array of commands used
    if not [x for x in triggerargsarray if x == "&&"]:
        rpg.multi_com_list.append(rpg.command_full_complete)
    else:
        command_full_split = rpg.command_full_complete.split("&&")
        for command_split in command_full_split:
            rpg.multi_com_list.append(command_split)

    # Cycle through command array
    rpg.commands_ran = []
    for command_split_partial in rpg.multi_com_list:
        rpg.triggerargsarray = get_trigger_arg(bot, command_split_partial, 'create')

        # Admin only
        rpg.admin = 0
        if [x for x in rpg.triggerargsarray if x == "-a"]:
            rpg.triggerargsarray.remove("-a")
            if rpg.instigator in rpg.botadmins:
                rpg.admin = 1
            else:
                errors(bot, rpg, 'commands', 4, 1)

        # Split commands to pass
        rpg.command_full = get_trigger_arg(bot, rpg.triggerargsarray, 0)
        rpg.command_main = get_trigger_arg(bot, rpg.triggerargsarray, 1).lower()
        # Check Command can run
        rpg = command_process(bot, trigger, rpg, instigator)
        if rpg.command_run:
            rpg.triggerargsarray.remove(rpg.command_main)
            # Run the command's function
            command_function_run = str('rpg_command_main_' + rpg.command_main + '(bot, rpg, instigator)')
            eval(command_function_run)
        rpg.commands_ran.append(rpg.command_main)


def command_process(bot, trigger, rpg, instigator):

    rpg.command_run = 0

    # allow players to set custom shortcuts to numbers
    if str(rpg.command_main).isdigit():
        number_command = get_database_value(bot, rpg.instigator, 'hotkey_'+str(rpg.command_main)) or 0
        if not number_command:
            errors(bot, rpg, 'commands', 8, rpg.command_main)
            return rpg
        else:
            number_command_list = get_database_value(bot, rpg.instigator, 'hotkey_complete') or []
            if rpg.command_main not in number_command_list:
                adjust_database_array(bot, rpg.instigator, [rpg.command_main], 'hotkey_complete', 'add')
            commandremaining = get_trigger_arg(bot, rpg.triggerargsarray, '2+') or ''
            number_command = str(number_command + " " + commandremaining)
            rpg.triggerargsarray = get_trigger_arg(bot, number_command, 'create')
            rpg.command_full = get_trigger_arg(bot, rpg.triggerargsarray, 0)
            rpg.command_main = get_trigger_arg(bot, rpg.triggerargsarray, 1)

    # Alternate commands convert TODO

    # multicom multiple of the same
    if rpg.command_main in rpg.commands_ran and not rpg.admin:
        errors(bot, rpg, 'commands', 5, 1)
        return rpg

    # Verify Command is valid
    if rpg.command_main not in rpg.valid_commands_all:  # TODO add similar()
        errors(bot, rpg, 'commands', 6, rpg.command_main)
        return rpg

    # Admin Block
    if rpg.command_main in rpg_commands_valid_admin and not rpg.admin:
        errors(bot, rpg, 'commands', 7, rpg.command_main)
        return rpg

    # Safe to run command
    rpg.command_run = 1

    return rpg


"""
Configuration Commands
"""


def rpg_command_main_admin(bot, rpg, instigator):

    # Subcommand
    subcommand_valid = eval('subcommands_valid_' + rpg.command_main)
    subcommand_default = eval('subcommands_default_' + rpg.command_main)
    subcommand = get_trigger_arg(bot, [x for x in rpg.triggerargsarray if x in subcommand_valid], 1) or subcommand_default
    if not subcommand:
        errors(bot, rpg, rpg.command_main, 1, 1)
        return

    if subcommand == 'channel':

        # Toggle Type
        activation_type = get_trigger_arg(bot, [x for x in rpg.triggerargsarray if x in subcommands_valid_admin_channel], 1)
        if not activation_type:
            errors(bot, rpg, 'admin', 2, 1)
            return

        activation_type_db = str(activation_type + "_enabled")

        # Channel
        channeltarget = get_trigger_arg(bot, [x for x in rpg.triggerargsarray if x in rpg.channels_list], 1)
        if not channeltarget:
            if rpg.channel_current.startswith('#'):
                channeltarget = rpg.channel_current
            else:
                errors(bot, rpg, 'admin', 3, 1)
                return

        # on/off
        activation_direction = get_trigger_arg(bot, [x for x in rpg.triggerargsarray if x in onoff_list], 1)
        if not activation_direction:
            errors(bot, rpg, rpg.command_main, 4, 1)
            return

        # Evaluate change
        current_channel_facet = eval("rpg.channels_" + activation_type_db)
        if activation_type == 'devmode':
            if activation_direction in activate_list:
                current_channel_facet_error = 5
            else:
                current_channel_facet_error = 6
        elif activation_type == 'game':
            if activation_direction in activate_list:
                current_channel_facet_error = 7
            else:
                current_channel_facet_error = 8

        # make the change
        if activation_direction in activate_list:
            if channeltarget.lower() in [x.lower() for x in current_channel_facet]:
                errors(bot, rpg, rpg.command_main, current_channel_facet_error, 1)
                return
            adjust_database_array(bot, 'rpg_game_records', [channeltarget], activation_type_db, 'add')
            osd(bot, channeltarget, 'say', "RPG " + activation_type + " has been enabled in " + channeltarget + "!")
        elif activation_direction in deactivate_list:
            if channeltarget.lower() not in [x.lower() for x in current_channel_facet]:
                errors(bot, rpg, rpg.command_main, current_channel_facet_error, 1)
                return
            adjust_database_array(bot, 'rpg_game_records', [channeltarget], activation_type_db, 'del')
            osd(bot, channeltarget, 'say', "RPG " + activation_type + " has been disabled in " + channeltarget + "!")

        if activation_type == 'game':
            errors_reset(bot, rpg, 'commands', 1)

        return


def rpg_command_main_settings(bot, rpg, instigator):

    # Subcommand
    subcommand_valid = eval('subcommands_valid_' + rpg.command_main)
    subcommand_default = eval('subcommands_default_' + rpg.command_main)
    subcommand = get_trigger_arg(bot, [x for x in rpg.triggerargsarray if x in subcommand_valid], 1) or subcommand_default
    if not subcommand:
        errors(bot, rpg, rpg.command_main, 1, 1)
        return

    # Who is the target
    target = get_trigger_arg(bot, [x for x in rpg.triggerargsarray if x in rpg.users_all], 1) or rpg.instigator
    if target != rpg.instigator:
        if not rpg.admin:
            errors(bot, rpg, rpg.command_main, 2, 1)
            return
        if target not in rpg.users_all:
            errors(bot, rpg, rpg.command_main, 3, target)
            return

    # Hokey
    if subcommand == 'hotkey':
        rpg.triggerargsarray.remove(subcommand)

        numberused = get_trigger_arg(bot, [x for x in rpg.triggerargsarray if str(x).isdigit()], 1) or 'nonumber'

        hotkeysetting = get_trigger_arg(bot, [x for x in rpg.triggerargsarray if x in subcommands_valid_settings_hotkey], 1) or 'view'

        if hotkeysetting == 'list':
            hotkeyscurrent = get_database_value(bot, target, 'hotkey_complete') or []
            if hotkeyscurrent == []:
                errors(bot, rpg, rpg.command_main, 5, 1)
                return
            hotkeyslist = []
            for key in hotkeyscurrent:
                keynumber = get_database_value(bot, rpg.instigator, 'hotkey_'+str(key)) or 0
                if keynumber:
                    hotkeyslist.append(str(key) + "=" + str(keynumber))
            hotkeyslist = get_trigger_arg(bot, hotkeyslist, 'list')
            osd(bot, rpg.channel_current, 'say', "Your hotkey list: " + hotkeyslist)
            return

        if numberused == 'nonumber':
            errors(bot, rpg, rpg.command_main, 4, 1)
            return
        number_command = get_database_value(bot, rpg.instigator, 'hotkey_'+str(numberused)) or 0

        if hotkeysetting != 'update':
            if not number_command:
                errors(bot, rpg, rpg.command_main, 6, numberused)
                return

        if hotkeysetting == 'view':
            osd(bot, rpg.channel_current, 'say', "You currently have " + str(numberused) + " set to '" + number_command + "'")
            return

        if hotkeysetting == 'reset':
            reset_database_value(bot, rpg.instigator, 'hotkey_'+str(numberused))
            adjust_database_array(bot, target, [numberused], 'hotkey_complete', 'del')
            osd(bot, rpg.channel_current, 'say', "Your command for hotkey "+str(numberused)+" has been reset")
            return

        if hotkeysetting == 'update':
            if target in rpg.triggerargsarray:
                rpg.triggerargsarray.remove(target)
            rpg.triggerargsarray.remove(numberused)
            rpg.triggerargsarray.remove(hotkeysetting)

            newcommandhot = get_trigger_arg(bot, rpg.triggerargsarray, 0) or 0
            if not newcommandhot:
                errors(bot, rpg, rpg.command_main, 7, 1)
                return

            actualcommand_main = get_trigger_arg(bot, rpg.triggerargsarray, 1) or 0
            if actualcommand_main not in rpg.valid_commands_all:  # TODO altcoms
                errors(bot, rpg, rpg.command_main, 8, str(actualcommand_main))
                return

            set_database_value(bot, rpg.instigator, 'hotkey_'+str(numberused), newcommandhot)
            adjust_database_array(bot, target, [numberused], 'hotkey_complete', 'add')
            osd(bot, rpg.channel_current, 'say', "Your "+str(numberused)+" command has been set to '" + newcommandhot+"'")
            return

        return


"""
Basic User Commands
"""


def rpg_command_main_author(bot, rpg, instigator):

    osd(bot, rpg.channel_current, 'say', "The author of RPG is deathbybandaid.")


def rpg_command_main_intent(bot, rpg, instigator):

    # Who is the target
    target = get_trigger_arg(bot, [x for x in rpg.triggerargsarray if x in rpg.users_all], 1) or rpg.instigator

    osd(bot, rpg.channel_current, 'say', "The intent is to provide "+target+" with a sense of pride and accomplishment...")


def rpg_command_main_about(bot, rpg, instigator):

    osd(bot, rpg.channel_current, 'say', "The purpose behind RPG is for deathbybandaid to learn python, while providing a fun, evenly balanced gameplay.")


def rpg_command_main_version(bot, rpg, instigator):

    # Attempt to get revision date from Github
    versionfetch = versionnumber(bot)

    osd(bot, rpg.channel_current, 'say', "The RPG framework was last modified on " + str(versionfetch) + ".")


def rpg_command_main_docs(bot, rpg, instigator):  # TODO
    bot.say("wip")


def rpg_command_main_usage(bot, rpg, instigator):  # TODO
    bot.say("wip")


"""
Bot Start
"""


@sopel.module.interval(1)  # TODO make this progress with the game
def timed_logcheck(bot):
    channels_game_enabled = get_database_value(bot, 'rpg_game_records', 'game_enabled') or []
    for channel in bot.channels:
        if channel in channels_game_enabled:
            startupmonologue = str("startup_monologue_" + channel)
            if startupmonologue not in bot.memory:
                bot.memory[startupmonologue] = 1

                startup_monologue = []
                startup_monologue.append("The Spice Realms are vast; full of wonder, loot, monsters, and peril!")
                startup_monologue.append("Will you, Brave Adventurers, be triumphant over the challenges that await?")
                osd(bot, channel, 'notice', startup_monologue)


"""
Debug
"""


def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


"""
Errors
"""


def errors(bot, rpg, error_type, number, append):
    current_error_value = eval("rpg.errors." + error_type + str(number))
    current_error_value.append(append)


def errors_reset(bot, rpg, error_type, number):
    current_error_value = str("rpg.errors." + error_type + str(number) + " = []")
    exec(current_error_value)


def rpg_errors_start(bot, rpg):
    rpg.errors = class_create('errors')
    errorscanlist = []
    for vcom in rpg.valid_commands_all:
        errorscanlist.append(vcom)
    for error_type in rpg_error_list:
        errorscanlist.append(error_type)
    for error_type in errorscanlist:
        current_error_type = eval("rpg_error_" + error_type)
        for i in range(0,len(current_error_type)):
            current_error_number = i + 1
            current_error_value = str("rpg.errors." + error_type + str(current_error_number) + " = []")
            exec(current_error_value)


def rpg_errors_end(bot, rpg):
    rpg.error_display = []
    errorscanlist = []
    for vcom in rpg.valid_commands_all:
        errorscanlist.append(vcom)
    for error_type in rpg_error_list:
        errorscanlist.append(error_type)
    for error_type in errorscanlist:
        current_error_type = eval("rpg_error_" + error_type)
        for i in range(0,len(current_error_type)):
            current_error_number = i + 1
            currenterrorvalue = eval("rpg.errors." + error_type + str(current_error_number))
            if currenterrorvalue != []:
                errormessage = get_trigger_arg(bot, current_error_type, current_error_number)
                if error_type in rpg.valid_commands_all:
                    errormessage = str("[" + str(error_type.title()) + "] " + errormessage)
                totalnumber = len(currenterrorvalue)
                errormessage = str("(" + str(totalnumber) + ") " + errormessage)
                if "$list" in errormessage:
                    errorlist = get_trigger_arg(bot, currenterrorvalue, 'list')
                    errormessage = str(errormessage.replace("$list", errorlist))
                if "$valid_coms" in errormessage:
                    validcomslist = get_trigger_arg(bot, rpg.valid_commands_all, 'list')
                    errormessage = str(errormessage.replace("$valid_coms", validcomslist))
                if "$game_chans" in errormessage:
                    gamechanlist = get_trigger_arg(bot, rpg.channels_game_enabled, 'list')
                    errormessage = str(errormessage.replace("$game_chans", gamechanlist))
                if "$valid_channels" in errormessage:
                    validchanlist = get_trigger_arg(bot, rpg.channels_list, 'list')
                    errormessage = str(errormessage.replace("$valid_channels", validchanlist))
                if "$valid_onoff" in errormessage:
                    validtogglelist = get_trigger_arg(bot, onoff_list, 'list')
                    errormessage = str(errormessage.replace("$valid_onoff", validtogglelist))
                if "$valid_subcoms" in errormessage:
                    subcommand_valid = eval('subcommands_valid_' + error_type)
                    subcommand_valid = get_trigger_arg(bot, subcommand_valid, 'list')
                    errormessage = str(errormessage.replace("$valid_subcoms", subcommand_valid))
                if "$valid_game_change" in errormessage:
                    subcommand_arg_valid = get_trigger_arg(bot, subcommands_valid_admin_channel, 'list')
                    errormessage = str(errormessage.replace("$valid_game_change", subcommand_arg_valid))
                if "$dev_chans" in errormessage:
                    devchans = get_trigger_arg(bot, rpg.channels_devmode_enabled, 'list')
                    errormessage = str(errormessage.replace("$dev_chans", devchans))
                if "$game_chans" in errormessage:
                    gamechans = get_trigger_arg(bot, rpg.channels_game_enabled, 'list')
                    errormessage = str(errormessage.replace("$game_chans", gamechans))
                if "$current_chan" in errormessage:
                    if rpg.channel_real:
                        errormessage = str(errormessage.replace("$current_chan", rpg.channel_current))
                    else:
                        errormessage = str(errormessage.replace("$current_chan", 'privmsg'))
                if errormessage not in rpg.error_display:
                    rpg.error_display.append(errormessage)
    if rpg.error_display != []:
        osd(bot, rpg.instigator, 'notice', rpg.error_display)


"""
Commands
"""


# All valid character stats
def rpg_valid_commands_all(bot, rpg):
    rpg.valid_commands_all = []
    for command_type in rpg_valid_command_types:
        typeeval = eval("rpg_commands_valid_"+command_type)
        for vcom in typeeval:
            rpg.valid_commands_all.append(vcom)
    return rpg


"""
Channels
"""


def rpg_command_channels(bot,rpg,trigger):

    # current Channels
    rpg.channel_current = trigger.sender

    # determine the type of channel
    if not rpg.channel_current.startswith("#"):
        rpg.channel_priv = 1
        rpg.channel_real = 0
    else:
        rpg.channel_priv = 0
        rpg.channel_real = 1

    # All channels the bot is in
    rpg.channels_list = []
    for channel in bot.channels:
        rpg.channels_list.append(channel)

    # Game Enabled
    rpg.channels_game_enabled = get_database_value(bot, 'rpg_game_records', 'game_enabled') or []

    # Development mode
    rpg.channels_devmode_enabled = get_database_value(bot, 'rpg_game_records', 'dev_enabled') or []
    rpg.dev_bypass = 0
    if rpg.channel_current.lower() in [x.lower() for x in rpg.channels_devmode_enabled]:
        rpg.dev_bypass = 1
    return rpg


"""
Users
"""


def rpg_command_users(bot,rpg):
    rpg.opadmin,rpg.owner,rpg.chanops,rpg.chanvoice,rpg.botadmins,rpg.users_current = [],[],[],[],[],[]

    for user in bot.users:
        rpg.users_current.append(str(user))
    adjust_database_array(bot, 'channel', rpg.users_current, 'users_all', 'add')
    rpg.users_all = get_database_value(bot, 'channel', 'users_all') or []

    for user in rpg.users_current:

        if user in bot.config.core.owner:
            rpg.owner.append(user)

        if user in bot.config.core.admins:
            rpg.botadmins.append(user)
            rpg.opadmin.append(user)

        for channelcheck in bot.channels:
            try:
                if bot.privileges[channelcheck][user] == OP:
                    rpg.chanops.append(user)
                    rpg.opadmin.append(user)
            except KeyError:
                dummyvar = 1
            try:
                if bot.privileges[channelcheck][user] == VOICE:
                    rpg.chanvoice.append(user)
            except KeyError:
                dummyvar = 1

    return rpg


"""
On Screen Text
"""


def osd(bot, target_array, text_type, text_array):

    # if text_array is a string, make it an array
    textarraycomplete = []
    if not isinstance(text_array, list):
        textarraycomplete.append(str(text_array))
    else:
        for x in text_array:
            textarraycomplete.append(str(x))

    # if target_array is a string, make it an array
    texttargetarray = []
    if not isinstance(target_array, list):
        if not str(target_array).startswith("#"):
            target_array = nick_actual(bot,str(target_array))
        texttargetarray.append(target_array)
    else:
        for target in target_array:
            if not str(target).startswith("#"):
                target = nick_actual(bot,str(target))
            texttargetarray.append(target)

    # Make sure we don't cross over IRC limits
    for target in texttargetarray:
        temptextarray = []
        if text_type == 'notice':
            temptextarray.append(target + ", ")
        for part in textarraycomplete:
            temptextarray.append(part)

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
                bot.action(combinedline,target)
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
How to Display Nicks
"""


# Outputs Nicks with correct capitalization
def nick_actual(bot,nick):
    nick_actual = nick
    for u in bot.users:
        if u.lower() == nick_actual.lower():
            nick_actual = u
            continue
    return nick_actual


"""
RPG Version
"""


def versionnumber(bot):
    rpg_version_plainnow = rpg_version_plain
    page = requests.get(rpg_version_github_page,headers=None)
    if page.status_code == 200:
        tree = html.fromstring(page.content)
        rpg_version_plainnow = str(tree.xpath(rpg_version_github_xpath))
        for r in (("\\n", ""), ("['",""), ("']",""), ("'",""), ('"',""), (',',""), ('Commits on',"")):
            rpg_version_plainnow = rpg_version_plainnow.replace(*r)
        rpg_version_plainnow = rpg_version_plainnow.strip()
    return rpg_version_plainnow


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
    randomselected = random.randint(0,len(temparray) - 1)
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
    for i in range(int(rangea),int(rangeb) + 1):
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
        for i in range(1,len(inputs)):
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
    sortbyarray, arrayb = (list(x) for x in zip(*sorted(zip(sortbyarray, arrayb),key=itemgetter(0))))
    return sortbyarray, arrayb


"""
Database
"""


# Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str('rpg_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value


# set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('rpg_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)


# set a value to None
def reset_database_value(bot, nick, databasekey):
    databasecolumn = str('rpg_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)


# add or subtract from current value
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str('rpg_' + databasekey)
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


"""
Dynamic Classes
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
        def __unicode__(self):
            return str(u+self.default)
        def lower(self):
            return str(self.default).lower()
        pass
        """
    exec(compile("class class_" + str(classname) + ": " + compiletext,"","exec"))
    newclass = eval('class_'+classname+"()")
    return newclass
