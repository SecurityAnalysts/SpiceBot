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
from random import randint, randrange
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
reload(sys)
sys.setdefaultencoding('utf-8')


"""
Triggers for usage
"""


# Base command
@sopel.module.commands('rpg')
@sopel.module.thread(True)
def rpg_trigger_main(bot, trigger):
    command_type = 'normalcom'
    triggerargsarray = spicemanip(bot, trigger.group(2), 'create')
    execute_start(bot, trigger, triggerargsarray, command_type)


"""
Command Processing
"""


def execute_start(bot, trigger, triggerargsarray, command_type):

    # RPG dynamic Class
    rpg = class_create('rpg')
    rpg.default = 'rpg'

    # Command type
    rpg.command_type = command_type

    # Time when Module use started
    rpg.start = time.time()

    # instigator
    instigator = class_create('instigator')
    instigator.default = trigger.nick
    rpg.instigator = trigger.nick

    rpg.tier_current = get_user_dict(bot, rpg, 'rpg_game_records', 'current_tier') or 0

    # Channel Listing
    rpg = rpg_command_channels(bot, rpg, trigger)

    # Commands list
    rpg = rpg_valid_commands_all(bot, rpg)

    # Bacic User List
    rpg = rpg_command_users(bot, rpg)

    # Error Display System Create
    rpg_errors_start(bot, rpg)

    # Get Map
    rpg_map_read(bot, rpg)

    # Run the Process
    execute_main(bot, rpg, instigator, trigger, triggerargsarray)

    # Error Display System Display
    rpg_errors_end(bot, rpg)

    # Save any open user values
    save_user_dicts(bot, rpg)


def execute_main(bot, rpg, instigator, trigger, triggerargsarray):

    # No Empty Commands
    if triggerargsarray == []:
        user_capable_coms = []
        for vcom in rpg.valid_commands_all:
            if vcom in rpg_commands_valid_administrator:
                if rpg.instigator in rpg.botadmins:
                    user_capable_coms.append(vcom)
            else:
                user_capable_coms.append(vcom)
        errors(bot, rpg, 'commands', 3, 1)
        return

    # Entire command string
    rpg.command_full_complete = spicemanip(bot, triggerargsarray, 0)

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
        rpg.triggerargsarray = spicemanip(bot, command_split_partial, 'create')

        # Admin only
        rpg.adminswitch = 0
        if [x for x in rpg.triggerargsarray if x == "-a"]:
            rpg.triggerargsarray.remove("-a")
            if rpg.instigator in rpg.botadmins:
                rpg.adminswitch = 1
            else:
                errors(bot, rpg, 'commands', 4, 1)

        # Split commands to pass
        rpg.command_full = spicemanip(bot, rpg.triggerargsarray, 0)
        rpg.command_main = spicemanip(bot, rpg.triggerargsarray, 1)
        # Check Command can run
        rpg = command_process(bot, trigger, rpg, instigator)
        if rpg.command_run:
            command_run(bot, rpg, instigator)
        rpg.commands_ran.append(rpg.command_main.lower())


def command_process(bot, trigger, rpg, instigator):

    rpg.command_run = 0

    # block instigator if
    instigatorcantplayarray = []
    instigatorcantplayarrays = ['rpg.valid_commands_all', 'rpg.valid_commands_alts', 'rpg.bots_list', 'rpg_map_names']
    for nicklist in instigatorcantplayarrays:
        currentnicklist = eval(nicklist)
        for x in currentnicklist:
            if x not in instigatorcantplayarray:
                instigatorcantplayarray.append(x)
    if rpg.instigator.lower() in [x.lower() for x in instigatorcantplayarray]:
        errors(bot, rpg, 'commands', 17, 1)
        return rpg

    # allow players to set custom shortcuts to numbers
    if str(rpg.command_main).isdigit():
        number_command = get_user_dict(bot, rpg, rpg.instigator, 'hotkey_'+str(rpg.command_main)) or 0
        if not number_command:
            errors(bot, rpg, 'commands', 8, rpg.command_main)
            return rpg
        else:
            number_command_list = get_user_dict(bot, rpg, rpg.instigator, 'hotkey_complete') or []
            if rpg.command_main.lower() not in number_command_list:
                adjust_user_dict_array(bot, rpg, rpg.instigator, 'hotkey_complete', [rpg.command_main.lower()], 'add')
            commandremaining = spicemanip(bot, rpg.triggerargsarray, '2+') or ''
            number_command = str(number_command + " " + commandremaining)
            rpg.triggerargsarray = spicemanip(bot, number_command, 'create')
            rpg.command_full = spicemanip(bot, rpg.triggerargsarray, 0)
            rpg.command_main = spicemanip(bot, rpg.triggerargsarray, 1)

    # Spell Check
    if rpg.command_main.lower() not in rpg.valid_commands_all and rpg.command_main.lower() not in rpg.valid_commands_alts and rpg.command_main.lower() not in [x.lower() for x in rpg.users_all]:
        startcom = rpg.command_main
        sim_com, sim_num = [], []
        command_type_list = ['valid_commands_all', 'valid_commands_alts', 'users_all']
        for comtype in command_type_list:
            comtype_eval = eval('rpg.' + comtype)
            for com in comtype_eval:
                similarlevel = similar(rpg.command_main.lower(), com.lower())
                if similarlevel >= .75:
                    sim_com.append(com)
                    sim_num.append(similarlevel)
        if sim_com != [] and sim_num != []:
            sim_num, sim_com = array_arrangesort(bot, sim_num, sim_com)
            rpg.command_main = spicemanip(bot, sim_com, 'last')
        if rpg.command_main.lower() != startcom.lower():
            rpg.triggerargsarray.remove(startcom)
            rpg.triggerargsarray.insert(0, rpg.command_main)
            rpg.command_full = spicemanip(bot, rpg.triggerargsarray, 0)

    # Instigator versus Instigator
    if rpg.command_main.lower() == rpg.instigator.lower() and not rpg.adminswitch:
        errors(bot, rpg, 'commands', 13, 1)
        return rpg

    # Instigator versus Bot
    if rpg.command_main.lower() == bot.nick.lower() and not rpg.adminswitch:
        errors(bot, rpg, 'commands', 12, 1)
        return rpg

    # Instigator versus Other Bots
    if rpg.command_main.lower() in [x.lower() for x in rpg.bots_list]:
        errors(bot, rpg, 'commands', 11, nick_actual(bot, rpg.command_main))
        return rpg

    # Targets
    if rpg.command_main.lower() in [x.lower() for x in rpg.users_all] and rpg.command_main.lower() not in rpg.valid_commands_all:
        rpg.command_main = 'combat'
        rpg.triggerargsarray.insert(0, rpg.command_main)
        rpg.command_full = spicemanip(bot, rpg.triggerargsarray, 0)

    # Alternate commands convert
    if rpg.command_main.lower() in rpg.valid_commands_alts:
        startcom = rpg.command_main
        rpg.triggerargsarray.remove(rpg.command_main)
        rpg.command_main = eval("rpg." + str(rpg.command_main.lower()) + ".realcom") or 'invalidcommand'
        if rpg.command_main.lower() == 'invalidcommand':
            errors(bot, rpg, 'commands', 9, startcom)
            return rpg
        rpg.triggerargsarray.insert(0, rpg.command_main)
        rpg.command_full = spicemanip(bot, rpg.triggerargsarray, 0)

    # multicom multiple of the same
    if rpg.command_main.lower() in rpg.commands_ran and not rpg.adminswitch:
        errors(bot, rpg, 'commands', 5, 1)
        return rpg

    # konami

    # Verify Command is valid
    if rpg.command_main.lower() not in rpg.valid_commands_all:
        errors(bot, rpg, 'commands', 6, rpg.command_main)
        return rpg

    # Verify Game enabled in current channel
    if rpg.channel_current not in rpg.channels_game_enabled and rpg.channel_real and rpg.command_main.lower() not in rpg_commands_valid_administrator:
        if rpg.channels_game_enabled == []:
            errors(bot, rpg, 'commands', 1, 1)
            if rpg.instigator not in rpg.botadmins:
                return rpg
        else:
            errors(bot, rpg, 'commands', 2, 1)
            if rpg.instigator not in rpg.botadmins:
                return rpg

    # Admin Block
    if rpg.command_main.lower() in rpg_commands_valid_administrator and not rpg.adminswitch:
        errors(bot, rpg, 'commands', 7, rpg.command_main)
        return rpg

    # Commands that Must be run in a channel
    if rpg.command_main.lower() in rpg_commands_valid_inchannel and not rpg.adminswitch:
        errors(bot, rpg, 'commands', 10, rpg.command_main)
        return rpg

    # action commands
    if rpg.command_type == 'action' and rpg.command_main.lower() not in rpg_commands_valid_action:
        errors(bot, rpg, 'commands', 14, rpg.command_main)
        return rpg

    # Tier Check
    command_tier_required = int(eval("rpg." + rpg.command_main.lower() + ".tier_number")) or 0
    if command_tier_required > int(rpg.tier_current):
        errors(bot, rpg, 'commands', 15, rpg.command_main)
        return rpg

    # Safe to run command
    rpg.command_run = 1

    return rpg


def command_run(bot, rpg, instigator):

    # Clear triggerargsarray of the main command
    rpg.triggerargsarray.remove(rpg.command_main)

    # Check Initial Stamina
    instigator.stamina = get_user_dict(bot, rpg, instigator.default, 'stamina') or 10
    rpg.staminarequired, rpg.staminacharge = 0, 0
    """ TODO track rpg.staminarequired  adding/subtracting in comparison to completion of any action, and error if not enough"""

    # Run the command's function
    command_function_run = str('rpg_command_main_' + rpg.command_main.lower() + '(bot, rpg, instigator)')
    eval(command_function_run)

    if rpg.staminacharge:
        bot.say("charge")

    # Deduct stamina from instigator
    # if rpg.staminarequired:
    #    adjust_user_dict(bot, rpg, instigator.default, 'stamina', -abs(rpg.staminarequired))

    # usage counter - instigator
    adjust_user_dict(bot, rpg, rpg.instigator, 'usage_' + rpg.command_main.lower(), 1)
    adjust_user_dict(bot, rpg, rpg.instigator, 'usage_total', 1)

    # usage counter - Total
    adjust_user_dict(bot, rpg, 'rpg_game_records', 'usage_' + rpg.command_main.lower(), 1)
    adjust_user_dict(bot, rpg, 'rpg_game_records', 'usage_total', 1)


"""
Exploration
"""


def rpg_command_main_travel(bot, rpg, instigator):

    subcommand_valid = ['north', 'south', 'east', 'west', 'town', 'current']
    subcommand = spicemanip(bot, [x for x in rpg.triggerargsarray if x in subcommand_valid], 1) or 'current'

    nickmap, nickcoord = rpg_map_nick_get(bot, rpg, rpg.instigator)
    nickcoord = eval(str(nickcoord))
    locationdict = rpg_get_latlong(bot, rpg, nickmap, str(nickcoord), 'returndict')

    if subcommand == 'current':
        bot.say(str(nickmap))
        bot.say(str(nickcoord))
        bot.say(str(locationdict))
        return

    latitude = nickcoord[0]
    longitude = nickcoord[1]
    newlatitude = latitude
    newlongitude = longitude

    if subcommand == 'north':
        newlatitude = int(latitude) + 1
    elif subcommand == 'south':
        newlatitude = int(latitude) - 1
    elif subcommand == 'east':
        newlongitude = int(longitude) + 1
    elif subcommand == 'west':
        newlongitude = int(longitude) - 1
    elif subcommand == 'town':
        towncoordinates = rpg_map_town(bot, rpg, nickmap)
        towncoordinates = eval(str(towncoordinates))
        newlatitude = towncoordinates[0]
        newlongitude = towncoordinates[1]

    mapsize = get_user_dict(bot, rpg, nickmap, 'mapsize')
    if int(newlatitude) > abs(mapsize):
        bot.say("cant go north anymore")
        return
    if int(newlatitude) < -abs(mapsize):
        bot.say("cant go south anymore")
        return
    if int(newlongitude) > abs(mapsize):
        bot.say("cant go east anymore")
        return
    if int(newlongitude) < -abs(mapsize):
        bot.say("cant go west anymore")
        return
    if str(latitude) == str(newlatitude) and str(longitude) == str(newlongitude):
        bot.say("stay current location")
        return

    newnickcoord = str("(" + str(newlatitude) + "," + str(newlongitude) + ")")

    rpg_map_move_nick(bot, rpg, rpg.instigator, nickmap, str(newnickcoord))
    bot.say("moved to " + str(newnickcoord))


def rpg_map_nick_get(bot, rpg, nick):

    nickmap, nickcoord = 0, 0

    cyclemapnumber = 0
    for map in rpg_map_names:
        cyclemapnumber += 1

        mapnicklist = get_user_dict(bot, rpg, map, 'mapnicklist')
        if not mapnicklist:
            mapnicklist = []
            set_user_dict(bot, rpg, map, 'mapnicklist', mapnicklist)
        if nick in mapnicklist:
            nickmap = map

            mapsize = get_user_dict(bot, rpg, map, 'mapsize')
            if not mapsize:
                mapsize = rpg_map_scale * cyclemapnumber
                set_user_dict(bot, rpg, map, 'mapsize', mapsize)

            # map size from center
            latitudearray, longitudearray = [], []
            for i in range(-abs(mapsize), mapsize + 1):
                latitudearray.append(i)
                longitudearray.append(i)

            # generate dictionary values for all locations
            coordinatecombinations = []
            for coordcombo in itertools.product(latitudearray, longitudearray):
                coordinatecombinations.append(coordcombo)
            for coordinates in coordinatecombinations:
                latlongnicklist = rpg_get_latlong(bot, rpg, map, str(coordinates), 'latlongnicklist') or []
                bot.say(str(coordinates) + " = " + str(latlongnicklist))
                if nick in latlongnicklist:
                    nickcoord = coordinates

    if not nickmap:
        nickmap = spicemanip(bot, rpg_map_names, 1)
    if not nickcoord:
        nickcoord = rpg_map_town(bot, rpg, nickmap)
    rpg_map_move_nick(bot, rpg, nick, nickmap, str(nickcoord))

    return nickmap, nickcoord


def rpg_map_move_nick(bot, rpg, nick, newmap, newcoordinates):

    for map in rpg_map_names:

        mapnicklist = get_user_dict(bot, rpg, map, 'mapnicklist') or []
        if map == newmap:
            if nick not in mapnicklist:
                mapnicklist.append(nick)
        else:
            if nick in mapnicklist:
                mapnicklist.remove(nick)
        set_user_dict(bot, rpg, map, 'mapnicklist', mapnicklist)

        mapsize = get_user_dict(bot, rpg, map, 'mapsize')
        if not mapsize:
            mapsize = rpg_map_scale * cyclemapnumber
            set_user_dict(bot, rpg, map, 'mapsize', mapsize)

        # map size from center
        latitudearray, longitudearray = [], []
        for i in range(-abs(mapsize), mapsize + 1):
            latitudearray.append(i)
            longitudearray.append(i)

        # generate dictionary values for all locations
        coordinatecombinations = []
        townfound = 0
        for coordcombo in itertools.product(latitudearray, longitudearray):
            coordinatecombinations.append(coordcombo)
        for coordinates in coordinatecombinations:
            latlongnicklist = rpg_get_latlong(bot, rpg, map, str(coordinates), 'mapnicklist') or []
            if str(coordinates) == str(newcoordinates):
                if nick not in latlongnicklist:
                    bot.say("move to " + str(coordinates))
                    latlongnicklist.append(nick)
                    rpg_set_latlong(bot, rpg, map, str(coordinates), 'mapnicklist', latlongnicklist)
            else:
                if nick in latlongnicklist:
                    bot.say("move from " + str(coordinates))
                    latlongnicklist.remove(nick)
                    rpg_set_latlong(bot, rpg, map, str(coordinates), 'mapnicklist', latlongnicklist)


def rpg_map_town(bot, rpg, map):

    returntown = str((0, 0))

    mapsize = get_user_dict(bot, rpg, map, 'mapsize')
    if not mapsize:
        mapsize = rpg_map_scale * cyclemapnumber
        set_user_dict(bot, rpg, map, 'mapsize', mapsize)

    # map size from center
    latitudearray, longitudearray = [], []
    for i in range(-abs(mapsize), mapsize + 1):
        latitudearray.append(i)
        longitudearray.append(i)

    # generate dictionary values for all locations
    coordinatecombinations = []
    townfound = 0
    for coordcombo in itertools.product(latitudearray, longitudearray):
        coordinatecombinations.append(coordcombo)
    for coordinates in coordinatecombinations:
        latlongdict = rpg_get_latlong(bot, rpg, map, str(coordinates), 'returndict')
        if 'town' in latlongdict.keys():
            townfound += 1
        mapnicklist = rpg_get_latlong(bot, rpg, map, str(coordinates), 'mapnicklist')
        if not mapnicklist:
            mapnicklist = []
            rpg_set_latlong(bot, rpg, map, str(coordinates), 'mapnicklist', mapnicklist)
    if not townfound:
        townlatitude = randint(-abs(mapsize), mapsize)
        townlongitude = randint(-abs(mapsize), mapsize)
        rpg_set_latlong(bot, rpg, map, str((townlatitude, townlongitude)), 'town', 1)
    for coordinates in coordinatecombinations:
        latlongdict = rpg_get_latlong(bot, rpg, map, str(coordinates), 'returndict')
        if 'town' in latlongdict.keys():
            returntown = str(coordinates)
    return returntown


def rpg_map_read(bot, rpg):

    cyclemapnumber = 0
    for map in rpg_map_names:
        cyclemapnumber += 1

        maptier = get_user_dict(bot, rpg, map, 'maptier')
        if not maptier:
            maptier = cyclemapnumber
            set_user_dict(bot, rpg, map, 'maptier', maptier)

        mapsize = get_user_dict(bot, rpg, map, 'mapsize')
        if not mapsize:
            mapsize = rpg_map_scale * cyclemapnumber
            set_user_dict(bot, rpg, map, 'mapsize', mapsize)

        # map size from center
        latitudearray, longitudearray = [], []
        for i in range(-abs(mapsize), mapsize + 1):
            latitudearray.append(i)
            longitudearray.append(i)

        # generate dictionary values for all locations
        coordinatecombinations = []
        townfound = 0
        for coordcombo in itertools.product(latitudearray, longitudearray):
            coordinatecombinations.append(coordcombo)
        for coordinates in coordinatecombinations:
            coordlatitude = coordinates[0]
            coordlongitude = coordinates[1]
            latlongdict = rpg_get_latlong(bot, rpg, map, str(coordinates), 'returndict')
            if 'town' in latlongdict.keys():
                townfound += 1
            mapnicklist = rpg_get_latlong(bot, rpg, map, str(coordinates), 'mapnicklist')
            if not mapnicklist:
                mapnicklist = []
                rpg_set_latlong(bot, rpg, map, str(coordinates), 'mapnicklist', mapnicklist)
            coordquadrant = rpg_get_latlong(bot, rpg, map, str(coordinates), 'coordquadrant')
            if not coordquadrant:
                if int(coordlatitude) > 0 and int(coordlongitude) > 0:
                    coordquadrant = 'northeast'
                elif int(coordlatitude) > 0 and int(coordlongitude) < 0:
                    coordquadrant = 'northwest'
                elif int(coordlatitude) < 0 and int(coordlongitude) > 0:
                    coordquadrant = 'southeast'
                elif int(coordlatitude) < 0 and int(coordlongitude) < 0:
                    coordquadrant = 'southwest'
                else:
                    coordquadrant = 'center'
                rpg_set_latlong(bot, rpg, map, str(coordinates), 'coordquadrant', coordquadrant)
        if not townfound:
            townlatitude = randint(-abs(mapsize), mapsize)
            townlongitude = randint(-abs(mapsize), mapsize)
            rpg_set_latlong(bot, rpg, map, str((townlatitude, townlongitude)), 'town', 1)


# Database map
def rpg_map_read_old(bot, dclass):

    # check that db list is there
    if not hasattr(dclass, 'map'):
        dclass.map = class_create('map')
    if not hasattr(dclass.map, 'list'):
        dclass.map.list = rpg_map_names

    cyclemapnumber = 0
    for map in dclass.map.list:
        cyclemapnumber += 1

        # Get current map subdictionary
        if not hasattr(dclass.map, map):
            mapdict = get_user_dict(bot, dclass, 'rpg_game_records', map) or dict()
            createmapdict = str("dclass.map." + map + " = mapdict")
            exec(createmapdict)
        else:
            if not hasattr(dclass.map, map):
                mapdict = dict()
            else:
                mapdict = eval('dclass.map' + map)

        # set tier that the map is accessible to a player
        if 'maptier' not in mapdict.keys():
            mapdict['maptier'] = cyclemapnumber

        # max height/width (from zero center)
        if 'mapsize' not in mapdict.keys():
            mapdict['mapsize'] = rpg_map_scale * cyclemapnumber

        # map size from center
        maxfromcenter = mapdict['mapsize']
        latitudearray, longitudearray = [], []
        for i in range(-abs(maxfromcenter), maxfromcenter + 1):
            latitudearray.append(i)
            longitudearray.append(i)

        # generate dictionary values for all locations
        for latitude, longitude in zip(latitudearray, longitudearray):

            bot.say(str(latitude) + "x" + str(longitude))

        # set town location
        # if 'town_latitude' not in mapdict.keys():
        #    mapdict['town_latitude'] = randint(-abs(maxfromcenter), maxfromcenter)
        # if 'town_longitude' not in mapdict.keys():
        #    mapdict['town_longitude'] = randint(-abs(maxfromcenter), maxfromcenter)


def rpg_map_save_old(bot, dclass):

    # check that db list is there
    if not hasattr(dclass, 'map'):
        dclass.map = class_create('map')
    if not hasattr(dclass.map, 'list'):
        dclass.map.list = rpg_map_names

    for map in dclass.map.list:

        if not hasattr(dclass.map, map):
            mapdict = dict()
        else:
            mapdict = eval('dclass.map.' + map)
        set_user_dict(bot, dclass, 'rpg_game_records', map, mapdict)


def rpg_get_latlong(bot, rpg, map, coordinates, dictkey):
    latlongdict = get_user_dict(bot, rpg, map, str(coordinates))
    if not latlongdict:
        latlongdict = dict()
        set_user_dict(bot, rpg, map, str(coordinates), latlongdict)
    if dictkey == 'returndict':
        returnvalue = latlongdict
    else:
        if dictkey not in latlongdict.keys():
            latlongdict[dictkey] = 0
        returnvalue = latlongdict[dictkey]
    return returnvalue


def rpg_set_latlong(bot, rpg, map, coordinates, dictkey, value):
    latlongdict = get_user_dict(bot, rpg, map, str(coordinates)) or dict()
    latlongdict[dictkey] = value
    set_user_dict(bot, rpg, map, str(coordinates), latlongdict)


"""
Combat
"""


def rpg_command_main_combat(bot, rpg, instigator):
    bot.say("combat not written yet")


"""
Configuration Commands
"""


def rpg_command_main_administrator(bot, rpg, instigator):

    # Subcommand
    subcommand_valid = eval('subcommands_valid_' + rpg.command_main.lower())
    subcommand_default = eval('subcommands_default_' + rpg.command_main.lower())
    subcommand = spicemanip(bot, [x for x in rpg.triggerargsarray if x in subcommand_valid], 1) or subcommand_default
    if not subcommand:
        errors(bot, rpg, rpg.command_main, 1, 1)
        return

    if subcommand == 'channel':

        # Toggle Type
        activation_type = spicemanip(bot, [x for x in rpg.triggerargsarray if x in subcommands_valid_administrator_channel], 1)
        if not activation_type:
            errors(bot, rpg, 'administrator', 2, 1)
            return

        activation_type_db = str(activation_type + "_enabled")

        # Channel
        channeltarget = spicemanip(bot, [x for x in rpg.triggerargsarray if x in rpg.channels_list], 1)
        if not channeltarget:
            if rpg.channel_current.startswith('#'):
                channeltarget = rpg.channel_current
            else:
                errors(bot, rpg, 'administrator', 3, 1)
                return

        # on/off
        activation_direction = spicemanip(bot, [x for x in rpg.triggerargsarray if x in onoff_list], 1)
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
            adjust_user_dict_array(bot, rpg, 'rpg_game_records', activation_type_db, [channeltarget], 'add')
            osd(bot, channeltarget, 'say', "RPG " + activation_type + " has been enabled in " + channeltarget + "!")
        elif activation_direction in deactivate_list:
            if channeltarget.lower() not in [x.lower() for x in current_channel_facet]:
                errors(bot, rpg, rpg.command_main, current_channel_facet_error, 1)
                return
            adjust_user_dict_array(bot, rpg, 'rpg_game_records', activation_type_db, [channeltarget], 'del')
            osd(bot, channeltarget, 'say', "RPG " + activation_type + " has been disabled in " + channeltarget + "!")

        if activation_type == 'game':
            errors_reset(bot, rpg, 'commands', 1)

        return


def rpg_command_main_settings(bot, rpg, instigator):

    # Subcommand
    subcommand_valid = eval('subcommands_valid_' + rpg.command_main.lower())
    subcommand_default = eval('subcommands_default_' + rpg.command_main.lower())
    subcommand = spicemanip(bot, [x for x in rpg.triggerargsarray if x in subcommand_valid], 1) or subcommand_default
    if not subcommand:
        errors(bot, rpg, rpg.command_main, 1, 1)
        return

    # Who is the target
    target = spicemanip(bot, [x for x in rpg.triggerargsarray if x in rpg.users_all], 1) or rpg.instigator
    if target != rpg.instigator:
        if not rpg.adminswitch:
            errors(bot, rpg, rpg.command_main, 2, 1)
            return
        if target not in rpg.users_all:
            errors(bot, rpg, rpg.command_main, 3, target)
            return

    # Hotkey
    if subcommand == 'hotkey':
        rpg.triggerargsarray.remove(subcommand)

        numberused = spicemanip(bot, [x for x in rpg.triggerargsarray if str(x).isdigit()], 1) or 'nonumber'

        hotkeysetting = spicemanip(bot, [x for x in rpg.triggerargsarray if x in subcommands_valid_settings_hotkey], 1) or 'view'

        if hotkeysetting == 'list':
            hotkeyscurrent = get_user_dict(bot, rpg, target, 'hotkey_complete') or []
            if hotkeyscurrent == []:
                errors(bot, rpg, rpg.command_main, 5, 1)
                return
            hotkeyslist = []
            for key in hotkeyscurrent:
                keynumber = get_user_dict(bot, rpg, rpg.instigator, 'hotkey_'+str(key)) or 0
                if keynumber:
                    hotkeyslist.append(str(key) + "=" + str(keynumber))
            hotkeyslist = spicemanip(bot, hotkeyslist, 'list')
            osd(bot, rpg.channel_current, 'say', "Your hotkey list: " + hotkeyslist)
            return

        if numberused == 'nonumber':
            errors(bot, rpg, rpg.command_main, 4, 1)
            return
        number_command = get_user_dict(bot, rpg, rpg.instigator, 'hotkey_'+str(numberused)) or 0

        if hotkeysetting != 'update':
            if not number_command:
                errors(bot, rpg, rpg.command_main, 6, numberused)
                return

        if hotkeysetting == 'view':
            osd(bot, rpg.channel_current, 'say', "You currently have " + str(numberused) + " set to '" + number_command + "'")
            return

        if hotkeysetting == 'reset':
            reset_user_dict(bot, rpg, rpg.instigator, 'hotkey_'+str(numberused))
            adjust_user_dict_array(bot, rpg, target, 'hotkey_complete', [numberused], 'del')
            osd(bot, rpg.channel_current, 'say', "Your command for hotkey "+str(numberused)+" has been reset")
            return

        if hotkeysetting == 'update':
            if target in rpg.triggerargsarray:
                rpg.triggerargsarray.remove(target)
            rpg.triggerargsarray.remove(numberused)
            rpg.triggerargsarray.remove(hotkeysetting)

            newcommandhot = spicemanip(bot, rpg.triggerargsarray, 0) or 0
            if not newcommandhot:
                errors(bot, rpg, rpg.command_main, 7, 1)
                return

            actualcommand_main = spicemanip(bot, rpg.triggerargsarray, 1) or 0
            if actualcommand_main not in rpg.valid_commands_all:  # TODO altcoms
                errors(bot, rpg, rpg.command_main, 8, str(actualcommand_main))
                return

            set_user_dict(bot, rpg, rpg.instigator, 'hotkey_'+str(numberused), newcommandhot)
            adjust_user_dict_array(bot, rpg, target, 'hotkey_complete', [numberused], 'add')
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
    target = spicemanip(bot, [x for x in rpg.triggerargsarray if x in rpg.users_all], 1) or rpg.instigator

    osd(bot, rpg.channel_current, 'say', "The intent is to provide " + target + " with a sense of pride and accomplishment...")


def rpg_command_main_about(bot, rpg, instigator):

    osd(bot, rpg.channel_current, 'say', "The purpose behind RPG is for deathbybandaid to learn python, while providing a fun, evenly balanced gameplay.")


def rpg_command_main_version(bot, rpg, instigator):

    # Attempt to get revision date from Github
    versionfetch = versionnumber(bot)

    osd(bot, rpg.channel_current, 'say', "The RPG framework was last modified on " + str(versionfetch) + ".")


def rpg_command_main_docs(bot, rpg, instigator):  # TODO
    bot.say("wip")


def rpg_command_main_usage(bot, rpg, instigator):  # TODO

    # Get The Command Used
    subcommand = spicemanip(bot, [x for x in rpg.triggerargsarray if x in rpg.valid_commands_all], 1) or 'total'

    # Who is the target
    target = spicemanip(bot, [x for x in rpg.triggerargsarray if x in rpg.users_all or x == 'channel'], 1) or rpg.instigator
    targetname = target
    if target == 'channel':
        target = 'rpg_game_records'
        targetname = "The channel"

    # Usage Counter
    totaluses = get_user_dict(bot, rpg, target, 'usage_' + subcommand) or 0
    if not totaluses:
        if subcommand == 'total':
            subcommand = ''
        osd(bot, rpg.channel_current, 'say', targetname + " has no record of using rpg " + subcommand + ". ")
        return

    # Display
    if subcommand == 'total':
        subcommand = 'a total of'
    else:
        subcommand = str(subcommand + ' a total of')
    osd(bot, rpg.channel_current, 'say', targetname + " has used rpg " + subcommand + " " + str(totaluses) + " times.")


"""
Bot Start
"""


@sopel.module.interval(1)  # TODO make this progress with the game
def rpg_bot_start_script(bot):
    rpg = class_create('rpg')
    rpg.default = 'rpg'
    channels_game_enabled = get_user_dict(bot, rpg, 'rpg_game_records', 'game_enabled') or []
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
Switches
"""


def find_switch_equal(bot, inputarray, switch):
    exitoutput = ''
    switchtofind = str("-"+str(switch)+'="')
    arraymarker = 0
    beguinemark, finishmark = 0, 0
    if [wordpart for wordpart in inputarray if wordpart.startswith(switchtofind)]:
        for partial in inputarray:
            arraymarker += 1
            if partial.startswith(switchtofind):
                beguinemark = arraymarker
            if partial.endswith('"'):
                if not finishmark and beguinemark != 0:
                    finishmark = arraymarker
                    continue
        if finishmark != 0:
            exitoutputrange = str(str(beguinemark) + "^" + str(finishmark))
            exitoutput = spicemanip(bot, inputarray, exitoutputrange)
            exitoutput = spicemanip(bot, exitoutput, 0)  # new
            # exitoutput = exitoutput.replace("-"+switch+'=', ' ')
            # exitoutput = exitoutput.replace('"', '')
            # exitoutput = exitoutput.strip()
    return exitoutput


"""
Small Functions
"""


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


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
        for i in range(0, len(current_error_type)):
            current_error_number = i + 1
            current_error_value = str("rpg.errors." + error_type + str(current_error_number) + " = []")
            exec(current_error_value)


def rpg_errors_end(bot, rpg):
    rpg.error_display = []
    rpg.tier_current = get_user_dict(bot, rpg, 'rpg_game_records', 'current_tier') or 0
    errorscanlist = []
    for vcom in rpg.valid_commands_all:
        errorscanlist.append(vcom)
    for error_type in rpg_error_list:
        errorscanlist.append(error_type)
    for error_type in errorscanlist:
        current_error_type = eval("rpg_error_" + error_type.lower())
        for i in range(0, len(current_error_type)):
            current_error_number = i + 1
            currenterrorvalue = eval("rpg.errors." + error_type.lower() + str(current_error_number)) or []
            if currenterrorvalue != []:
                errormessage = spicemanip(bot, current_error_type, current_error_number)
                if error_type in rpg.valid_commands_all:
                    errormessage = str("[" + str(error_type.title()) + "] " + errormessage)
                totalnumber = len(currenterrorvalue)
                errormessage = str("(" + str(totalnumber) + ") " + errormessage)
                if "$list" in errormessage:
                    errorlist = spicemanip(bot, currenterrorvalue, 'list')
                    errormessage = str(errormessage.replace("$list", errorlist))
                if "$tiers_nums_peppers" in errormessage:
                    numberarray, pepperarray, combinedarray = [], [], []
                    for command in currenterrorvalue:
                        peppereval = eval("rpg." + command.lower() + ".tier_pepper")
                        pepperarray.append(peppereval)
                        numbereval = int(eval("rpg." + command.lower() + ".tier_number"))
                        numberarray.append(numbereval)
                    for num, pepp in zip(numberarray, pepperarray):
                        combinedarray.append(str(num) + " " + pepp)
                    errorlist = spicemanip(bot, combinedarray, 'list')
                    errormessage = str(errormessage.replace("$tiers_nums_peppers", errorlist))
                if "$valid_coms" in errormessage:
                    validcomslist = spicemanip(bot, rpg.valid_commands_all, 'list')
                    errormessage = str(errormessage.replace("$valid_coms", validcomslist))
                if "$game_chans" in errormessage:
                    gamechanlist = spicemanip(bot, rpg.channels_game_enabled, 'list')
                    errormessage = str(errormessage.replace("$game_chans", gamechanlist))
                if "$valid_channels" in errormessage:
                    validchanlist = spicemanip(bot, rpg.channels_list, 'list')
                    errormessage = str(errormessage.replace("$valid_channels", validchanlist))
                if "$valid_onoff" in errormessage:
                    validtogglelist = spicemanip(bot, onoff_list, 'list')
                    errormessage = str(errormessage.replace("$valid_onoff", validtogglelist))
                if "$valid_subcoms" in errormessage:
                    subcommand_valid = eval('subcommands_valid_' + error_type.lower())
                    subcommand_valid = spicemanip(bot, subcommand_valid, 'list')
                    errormessage = str(errormessage.replace("$valid_subcoms", subcommand_valid))
                if "$valid_game_change" in errormessage:
                    subcommand_arg_valid = spicemanip(bot, subcommands_valid_administrator_channel, 'list')
                    errormessage = str(errormessage.replace("$valid_game_change", subcommand_arg_valid))
                if "$dev_chans" in errormessage:
                    devchans = spicemanip(bot, rpg.channels_devmode_enabled, 'list')
                    errormessage = str(errormessage.replace("$dev_chans", devchans))
                if "$game_chans" in errormessage:
                    gamechans = spicemanip(bot, rpg.channels_game_enabled, 'list')
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


# All valid commands
def rpg_valid_commands_all(bot, rpg):

    # make list of all valid commands
    rpg.valid_commands_all = []
    rpg.valid_commands_alts = []
    for command_type in rpg_valid_command_types:
        typeeval = eval("rpg_commands_valid_"+command_type)
        for vcom in typeeval:
            if vcom not in rpg.valid_commands_all:
                rpg.valid_commands_all.append(vcom)

    # data regarding each command
    for vcom in rpg.valid_commands_all:

        # create class
        currentcommandclass = class_create(vcom)
        exec("rpg." + str(vcom) + " = currentcommandclass")

        # Tier number
        currenttiernumber = 0
        for i in range(0, len(rpg_commands_tier_unlocks)):
            current_tier_eval_number = i + 1
            currenttiereval = spicemanip(bot, rpg_commands_tier_unlocks, current_tier_eval_number) or []
            if vcom in currenttiereval:
                currenttiernumber = current_tier_eval_number
        exec("rpg." + str(vcom) + ".tier_number = currenttiernumber")

        # Tier Pepper
        currentpepper = spicemanip(bot, rpg_commands_pepper_levels, currenttiernumber) or 'Spicy'
        exec("rpg." + str(vcom) + ".tier_pepper = currentpepper")

        # alternate commands
        current_alts = eval("rpg_commands_valid_alt_"+vcom) or []
        for acom in current_alts:
            if acom not in rpg.valid_commands_alts:
                rpg.valid_commands_alts.append(acom)

            # create class
            currentaltcommandclass = class_create(acom)
            exec("rpg." + str(acom) + " = currentcommandclass")
            exec("rpg." + str(acom) + ".realcom = vcom")

        exec("rpg." + str(vcom) + ".altcoms = current_alts")

    return rpg


"""
Channels
"""


def rpg_command_channels(bot, rpg, trigger):

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
    rpg.channels_game_enabled = get_user_dict(bot, rpg, 'rpg_game_records', 'game_enabled') or []

    # Development mode
    rpg.channels_devmode_enabled = get_user_dict(bot, rpg, 'rpg_game_records', 'dev_enabled') or []
    rpg.dev_bypass = 0
    if rpg.channel_current.lower() in [x.lower() for x in rpg.channels_devmode_enabled]:
        rpg.dev_bypass = 1
    return rpg


"""
Users
"""


def rpg_command_users(bot, rpg):
    usertypes = ['users_all', 'opadmin', 'owner', 'chanops', 'chanvoice', 'botadmins', 'users_current', 'users_offline', 'bots_list']
    for x in usertypes:
        currentvalue = str("rpg."+x+"=[]")
        exec(currentvalue)

    for user in bot.users:
        if user not in rpg.valid_commands_all and user not in rpg.valid_commands_alts:
            rpg.users_current.append(str(user))
    users_all = get_user_dict(bot, rpg, 'channel', 'users_all') or []
    for user in users_all:
        if user not in rpg.users_current and user in users_all:
            rpg.users_offline.append(user)
    adjust_user_dict_array(bot, rpg, 'channel', 'users_all', rpg.users_current, 'add')

    rpg.bots_list = bot_config_names(bot)

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


# Bot Nicks
def bot_config_names(bot):
    config_listing = []
    networkname = str(bot.config.core.user.split("/", 1)[1] + "/")
    validconfigsdir = str("/home/spicebot/.sopel/" + bot.nick + "/System-Files/Configs/" + networkname)
    for filename in os.listdir(validconfigsdir):
        filenameminuscfg = str(filename).replace(".cfg", "")
        config_listing.append(filenameminuscfg)
    return config_listing


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
How to Display Nicks
"""


# Outputs Nicks with correct capitalization
def nick_actual(bot, nick):
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
    page = requests.get(rpg_version_github_page, headers=None)
    if page.status_code == 200:
        tree = html.fromstring(page.content)
        rpg_version_plainnow = str(tree.xpath(rpg_version_github_xpath))
        for r in (("\\n", ""), ("['", ""), ("']", ""), ("'", ""), ('"', ""), (',', ""), ('Commits on', "")):
            rpg_version_plainnow = rpg_version_plainnow.replace(*r)
        rpg_version_plainnow = rpg_version_plainnow.strip()
    return rpg_version_plainnow


"""
Counter
"""


def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count


"""
Array/List/String Manipulation
"""


# Hub
def spicemanip(bot, inputs, outputtask, output_type='default'):

    mainoutputtask, suboutputtask = None, None

    # Input needs to be a list, but don't split a word into letters
    if not inputs:
        inputs = []
    if not isinstance(inputs, list):
        inputs = list(inputs.split(" "))

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
    return returnvalue


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
    bot.db.set_nick_value(nick, databasecolumn, float(oldvalue) + float(value))


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


# Database Users
def get_user_dict(bot, rpg, nick, dictkey):

    # check that db list is there
    if not hasattr(rpg, 'userdb'):
        rpg.userdb = class_create('userdblist')
    if not hasattr(rpg.userdb, 'list'):
        rpg.userdb.list = []

    returnvalue = 0

    # check if nick has been pulled from db already
    if nick not in rpg.userdb.list:
        rpg.userdb.list.append(nick)
        nickdict = get_database_value(bot, nick, rpg.default) or dict()
        createuserdict = str("rpg.userdb." + nick + " = nickdict")
        exec(createuserdict)
    else:
        if not hasattr(rpg.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('rpg.userdb.' + nick)

    if dictkey in nickdict.keys():
        returnvalue = nickdict[dictkey]
    else:
        nickdict[dictkey] = 0
        returnvalue = 0

    return returnvalue


# set a value
def set_user_dict(bot, rpg, nick, dictkey, value):
    currentvalue = get_user_dict(bot, rpg, nick, dictkey)
    nickdict = eval('rpg.userdb.' + nick)
    nickdict[dictkey] = value


# reset a value
def reset_user_dict(bot, rpg, nick, dictkey):
    currentvalue = get_user_dict(bot, rpg, nick, dictkey)
    nickdict = eval('rpg.userdb.' + nick)
    if dictkey in nickdict:
        del nickdict[dictkey]


# add or subtract from current value
def adjust_user_dict(bot, rpg, nick, dictkey, value):
    oldvalue = get_user_dict(bot, rpg, nick, dictkey)
    if not str(oldvalue).isdigit():
        oldvalue = 0
    nickdict = eval('rpg.userdb.' + nick)
    nickdict[dictkey] = oldvalue + value


# Save all database users in list
def save_user_dicts(bot, rpg):

    # check that db list is there
    if not hasattr(rpg, 'userdb'):
        rpg.userdb = class_create('userdblist')
    if not hasattr(rpg.userdb, 'list'):
        rpg.userdb.list = []

    for nick in rpg.userdb.list:
        if not hasattr(rpg.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('rpg.userdb.' + nick)
        set_database_value(bot, nick, rpg.default, nickdict)


# add or subtract from current value
def adjust_user_dict_array(bot, rpg, nick, dictkey, entries, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    oldvalue = get_user_dict(bot, rpg, nick, dictkey)
    nickdict = eval('rpg.userdb.' + nick)
    if not isinstance(oldvalue, list):
        oldvalue = []
    for x in entries:
        if adjustmentdirection == 'add':
            if x not in oldvalue:
                oldvalue.append(x)
        elif adjustmentdirection == 'del':
            if x in oldvalue:
                oldvalue.remove(x)
    nickdict[dictkey] = oldvalue


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
    exec(compile("class class_" + str(classname) + ": " + compiletext, "", "exec"))
    newclass = eval('class_'+classname+"()")
    return newclass
