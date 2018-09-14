#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, ADMIN, VOICE, event, rule
import sopel
from sopel import module, tools
import re
import datetime
import git
import ConfigParser
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *
log_path = "data/templog.txt"
log_file_path = os.path.join(moduledir, log_path)

GITWIKIURL = "https://github.com/SpiceBot/SpiceBot/wiki"

# TODO add a notification of traceback errors
# TODO add warn functionality
# TODO channel and user commands

"""
# bot.nick do this
"""


@nickname_commands('uptime', 'modules', 'msg', 'action', 'block', 'github', 'on', 'off', 'devmode', 'update', 'restart', 'permfix', 'debug', 'pip', 'channel', 'gender', 'owner', 'admin', 'canyouseeme', 'help', 'docs', 'cd', 'dir', 'gitpull')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):
    triggerargsarray = spicemanip(bot, trigger.group(0), 'create')
    triggerargsarray = spicemanip(bot, triggerargsarray, '2+')
    triggerargsarray = spicemanip(bot, triggerargsarray, 'create')
    bot_command_process(bot, trigger, triggerargsarray)


def bot_command_process(bot, trigger, triggerargsarray):

    # Dyno Classes
    botcom = class_create('bot')
    instigator = class_create('instigator')
    botcom.instigator = trigger.nick

    # time
    botcom.now = time.time()

    # User
    botcom = bot_command_users(bot, botcom)

    # Channels
    botcom = bot_command_channels(bot, botcom, trigger)

    # Command Used
    botcom.command_main = spicemanip(bot, triggerargsarray, 1)
    if botcom.command_main in triggerargsarray:
        triggerargsarray.remove(botcom.command_main)
    if botcom.command_main == 'help':
        botcom.command_main = 'docs'
    botcom.triggerargsarray = triggerargsarray
    bot_command_function_run = str('bot_command_function_' + botcom.command_main.lower() + '(bot,trigger,botcom,instigator)')
    eval(bot_command_function_run)


"""
Commands
"""


def bot_command_function_gitpull(bot, trigger, botcom, instigator):

    botcom.directory = get_database_value(bot, bot.nick, 'current_admin_dir') or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    osd(bot, botcom.channel_current, 'say', "attempting to git pull " + botcom.directory)
    g = git.cmd.Git(botcom.directory)
    g.pull()


def bot_command_function_dir(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    botcom.directory = get_database_value(bot, bot.nick, 'current_admin_dir') or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    botcom = bot_list_directory(bot, botcom)
    if botcom.directory == []:
        osd(bot, botcom.channel_current, 'say', "It appears this directory is empty.")
        return
    displaymsgarray = []
    displaymsgarray.append("Current files located in " + str(botcom.directory) + " :")
    for filename, filefoldertype in zip(botcom.directory_listing, botcom.filefoldertype):
        displaymsgarray.append(str("["+filefoldertype.title()+"] ")+str(filename))
    osd(bot, botcom.channel_current, 'say', displaymsgarray)


def bot_command_function_cd(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    validfolderoptions = ['..', 'reset']
    botcom.directory = get_database_value(bot, bot.nick, 'current_admin_dir') or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    botcom = bot_list_directory(bot, botcom)

    for filename, filefoldertype in zip(botcom.directory_listing, botcom.filefoldertype):
        if filefoldertype == 'folder':
            validfolderoptions.append(filename)

    movepath = spicemanip(bot, botcom.triggerargsarray, 0)
    if movepath not in validfolderoptions:
        if movepath in botcom.directory_listing and movepath not in validfolderoptions:
            osd(bot, botcom.channel_current, 'say', "You can't Change Directory into a File!")
        else:
            osd(bot, botcom.channel_current, 'say', "Invalid Folder Path")
        return

    if movepath == "..":
        movepath = os.path.dirname(botcom.directory)
    elif movepath == 'reset':
        movepath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    else:
        movepath = os.path.join(botcom.directory, str(movepath+"/"))

    set_database_value(bot, bot.nick, 'current_admin_dir', str(movepath))

    osd(bot, botcom.channel_current, 'say', "Directory Changed to : " + str(movepath))


def bot_command_function_docs(bot, trigger, botcom, instigator):
    osd(bot, botcom.channel_current, 'say', "Online Docs: " + GITWIKIURL)


def bot_command_function_canyouseeme(bot, trigger, botcom, instigator):
    osd(bot, botcom.channel_current, 'say', botcom.instigator + ", I can see you.")


def bot_command_function_owner(bot, trigger, botcom, instigator):
    ownerlist = spicemanip(bot, botcom.owner, 'list')
    osd(bot, botcom.instigator, 'notice', "Bot Owners are: " + ownerlist)


def bot_command_function_admin(bot, trigger, botcom, instigator):
    adminlist = spicemanip(bot, botcom.botadmins, 'list')
    osd(bot, botcom.instigator, 'notice', "Bot Admin are: " + adminlist)


def bot_command_function_gender(bot, trigger, botcom, instigator):
    osd(bot, botcom.channel_current, 'say', "My gender is Female")


def bot_command_function_channel(bot, trigger, botcom, instigator):

    # SubCommand used
    valid_subcommands = ['list', 'op', 'voice']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'list'

    # list channels
    if subcommand == 'list':
        channelarray = []
        for c in bot.channels:
            channelarray.append(c)
        chanlist = spicemanip(bot, channelarray, 'list')
        osd(bot, botcom.channel_current, 'say', "You can find me in " + chanlist)
        return

    # OP list
    if subcommand.lower() == 'op':
        oplist = spicemanip(bot, botcom.chanops, 'list')
        osd(bot, botcom.instigator, 'notice', "Channel Operators are: " + oplist)
        return

    # Voice List
    if subcommand.lower() == 'voice':
        voicelist = spicemanip(bot, botcom.chanvoice, 'list')
        osd(bot, botcom.instigator, 'notice', "Channel VOICE are: " + voicelist)
        return


def bot_command_function_on(bot, trigger, botcom, instigator):

    target = spicemanip(bot, [x for x in botcom.triggerargsarray if x in botcom.users_all], 1) or botcom.instigator
    if target != botcom.instigator and botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function on other users.")
        return
    bot_opted_users = get_database_value(bot, bot.nick, 'users_blocked') or []
    if target not in bot_opted_users:
        if target == botcom.instigator:
            osd(bot, botcom.instigator, 'notice', "It looks like you already have " + bot.nick + " " + botcom.command_main+".")
        else:
            osd(bot, botcom.instigator, 'notice', "It looks like " + target + " already has " + bot.nick + " " + botcom.command_main+".")
        return
    adjust_database_array(bot, bot.nick, target, 'users_opted', 'add')


def bot_command_function_off(bot, trigger, botcom, instigator):
    target = spicemanip(bot, [x for x in botcom.triggerargsarray if x in botcom.users_all], 1) or botcom.instigator
    if target != botcom.instigator and botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function on other users.")
        return
    bot_opted_users = get_database_value(bot, channeltarget, 'users_blocked') or []
    if target in bot_blocked_users:
        if target == botcom.instigator:
            osd(bot, botcom.instigator, 'notice', "It looks like you already have " + bot.nick + " " + botcom.command_main+".")
        else:
            osd(bot, botcom.instigator, 'notice', "It looks like " + target + " already has " + bot.nick + " " + botcom.command_main+".")
        return
    adjust_database_array(bot, bot.nick, target, 'users_opted', 'del')


def bot_command_function_modules(bot, trigger, botcom, instigator):

    # Channel
    channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return

    # SubCommand used
    valid_subcommands = ['enable', 'disable', 'list', 'count']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'list'

    bot_visible_coms = []
    for cmds in bot.command_groups.items():
        for cmd in cmds:
            if str(cmd).endswith("]"):
                for x in cmd:
                    bot_visible_coms.append(x)

    bot_enabled_coms = get_database_value(bot, channeltarget, 'modules_enabled') or []

    if subcommand == 'count':
        osd(bot, botcom.channel_current, 'say', 'There are currently ' + str(len(bot_visible_coms)) + ' custom modules installed.')
        return

    if subcommand == 'list':
        botmessagearray = []
        botmessagearray.append("This is a listing of modules that I can see (E=Enabled, A=Available):")
        for command in bot_visible_coms:
            if command in bot_enabled_coms:
                botmessagearray.append(command+"[E]")
            else:
                botmessagearray.append(command+"[A]")
        osd(bot, botcom.instigator, 'notice', botmessagearray)

    # Enable/Disable
    if subcommand == 'enable' or subcommand == 'disable':

        if botcom.instigator not in botcom.opadmin:
            osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
            return

        module_adjust = spicemanip(bot, [x for x in botcom.triggerargsarray if x in bot_visible_coms or x == 'all'], 1) or 'no_module'
        if module_adjust == 'no_module':
            osd(bot, botcom.instigator, 'notice', "What module do you want to "+str(subcommand)+" for " + channeltarget + "?")
            return

        if module_adjust in bot_enabled_coms and subcommand == 'enable' and module_adjust != 'all':
            osd(bot, botcom.instigator, 'notice', "It looks like "+str(module_adjust)+" is already "+subcommand.lower()+"d for " + channeltarget + "?")
            return

        if module_adjust not in bot_enabled_coms and subcommand == 'disable' and module_adjust != 'all':
            osd(bot, botcom.instigator, 'notice', "It looks like "+str(module_adjust)+" is already "+subcommand.lower()+"d for " + channeltarget + "?")
            return

        if module_adjust == 'all':
            modulesadjustarray = bot_visible_coms
        else:
            modulesadjustarray = [module_adjust]

        if subcommand == 'enable':
            adjust_database_array(bot, channeltarget, modulesadjustarray, 'modules_enabled', 'add')
        else:
            adjust_database_array(bot, channeltarget, modulesadjustarray, 'modules_enabled', 'del')
        osd(bot, botcom.channel_current, 'say', module_adjust + " command(s) should now be "+str(subcommand)+"d for " + channeltarget + ".")


def bot_command_function_msg(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    # Channel
    channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    if channeltarget in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(channeltarget)

    botmessage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not botmessage:
        osd(bot, botcom.instigator, 'notice', "You must specify a message.")
        return
    osd(bot, channeltarget, 'say', botmessage)


def bot_command_function_action(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    # Channel
    channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    if channeltarget in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(channeltarget)

    botmessage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not botmessage:
        osd(bot, botcom.instigator, 'notice', "You must specify a message.")
        return
    osd(bot, channeltarget, 'action', botmessage)


def bot_command_function_block(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    # Channel
    channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    if channeltarget in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(channeltarget)

    # SubCommand used
    valid_subcommands = ['current', 'add', 'del']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'current'

    bot_blocked_users = get_database_value(bot, channeltarget, 'users_blocked') or []

    if subcommand == 'current':
        botmessage = []
        if bot_blocked_users != []:
            botmessage.append("The following users are currently blocked:")
            current_block_list = spicemanip(bot, bot_blocked_users, 'list')
            botmessage.append(str(current_block_list))
        else:
            botmessage.append("No users are currently blocked")
        osd(bot, botcom.channel_current, 'say', botmessage)
        return

    if subcommand == 'add' or subcommand == 'del':
        blocknewlist = []
        if 'all' in botcom.triggerargsarray:
            for user in botcom.users_all:
                if subcommand == 'add' and user not in bot_blocked_users:
                    blocknewlist.append(user)
                if subcommand == 'del' and user in bot_blocked_users:
                    blocknewlist.append(user)
        else:
            for word in botcom.triggerargsarray:
                if word in botcom.users_all and word not in blocknewlist:
                    if subcommand == 'add' and word not in bot_blocked_users:
                        blocknewlist.append(word)
                    if subcommand == 'del' and word in bot_blocked_users:
                        blocknewlist.append(word)

        if blocknewlist == []:
            osd(bot, botcom.instigator, 'notice', "No Valid Users found to block.")
            return

        blocknewlisttext = spicemanip(bot, blocknewlist, 'list')

        if subcommand == 'add':
            adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked', 'add')
            adddelword = "added to"
            osd(bot, botcom.channel_current, 'say', "The following users have been " + adddelword + " the " + channeltarget + " block list: " + blocknewlisttext)
        else:
            adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked', 'del')
            adddelword = "removed from"
            osd(bot, botcom.channel_current, 'say', "The following users have been " + adddelword + " the " + channeltarget + " block list: " + blocknewlisttext)


def bot_command_function_github(bot, trigger, botcom, instigator):

    # main subcom
    valid_main_subcom = ['show', 'block']
    main_subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_main_subcom], 1) or 'show'

    if main_subcommand == 'show':
        osd(bot, botcom.channel_current, 'say', 'Spiceworks IRC Modules     https://github.com/SpiceBot/SpiceBot')
        return

    if main_subcommand == 'block':

        if botcom.instigator not in botcom.opadmin:
            osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
            return

        # Channel
        channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
        if not channeltarget:
            if botcom.channel_current.startswith('#'):
                channeltarget = botcom.channel_current
            else:
                osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
                return
        if channeltarget in botcom.triggerargsarray:
            botcom.triggerargsarray.remove(channeltarget)

        # SubCommand used
        valid_subcommands = ['current', 'add', 'del']
        subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'current'

        bot_blocked_users_github = get_database_value(bot, channeltarget, 'users_blocked_github') or []

        if subcommand == 'current':
            botmessage = []
            if bot_blocked_users_github != []:
                botmessage.append("The following users are currently blocked:")
                current_block_list = spicemanip(bot, bot_blocked_users_github, 'list')
                botmessage.append(str(current_block_list))
            else:
                botmessage.append("No users are currently blocked from github.")
            osd(bot, botcom.channel_current, 'say', botmessage)
            return

        if subcommand == 'add' or subcommand == 'del':
            blocknewlist = []
            if 'all' in botcom.triggerargsarray:
                for user in botcom.users_all:
                    if subcommand == 'add' and user not in bot_blocked_users_github:
                        blocknewlist.append(user)
                    if subcommand == 'del' and user in bot_blocked_users_github:
                        blocknewlist.append(user)
            else:
                for word in botcom.triggerargsarray:
                    if word in botcom.users_all and word not in blocknewlist:
                        if subcommand == 'add' and word not in bot_blocked_users_github:
                            blocknewlist.append(word)
                        if subcommand == 'del' and word in bot_blocked_users_github:
                            blocknewlist.append(word)

            if blocknewlist == []:
                osd(bot, botcom.instigator, 'notice', "No Valid Users found to block from github.")
                return

            blocknewlisttext = spicemanip(bot, blocknewlist, 'list')

            if subcommand == 'add':
                adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked_github', 'add')
                adddelword = "added to"
            else:
                adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked_github', 'del')
                adddelword = "removed from"
            osd(bot, botcom.channel_current, 'say', "The following users have been " + adddelword + " the " + channeltarget + " github block list: " + blocknewlisttext)
        return


def bot_command_function_devmode(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.botadmins:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    # Channel
    channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    if channeltarget in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(channeltarget)

    # SubCommand used
    valid_subcommands = ['on', 'off']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1)
    if not subcommand:
        osd(bot, botcom.instigator, 'notice', "Do you want devmode on or off in " + channeltarget + "?")
        return

    if subcommand == 'on':
        adjust_database_array(bot, bot.nick, [channeltarget], 'channels_dev', 'add')
    else:
        adjust_database_array(bot, bot.nick, [channeltarget], 'channels_dev', 'del')
    osd(bot, botcom.channel_current, 'say', "devmode should now be " + subcommand + " for " + channeltarget + ".")


def bot_command_function_update(bot, trigger, botcom, instigator):

    botcom = bot_config_directory(bot, botcom)

    targetbots = []
    if botcom.triggerargsarray == []:
        targetbots.append(bot.nick)
    elif 'all' in botcom.triggerargsarray:
        for targetbot in botcom.config_listing:
            targetbots.append(targetbot)
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in botcom.config_listing:
                targetbots.append(targetbot)

    for targetbot in targetbots:
        joindpath = os.path.join("/home/spicebot/.sopel/", targetbot)
        if not os.path.isdir(joindpath):
            targetbots.remove(targetbot)

    for targetbot in targetbots:
        targetbotadmins = bot_target_admins(bot, targetbot)
        if botcom.instigator not in targetbotadmins:
            targetbots.remove(targetbot)

    if targetbots == []:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function for the selected bots OR the bots directory is missing.")
        return

    # current bot should be last
    if bot.nick in targetbots:
        targetbots.remove(bot.nick)
        targetbots.append(bot.nick)

    if len(targetbots) == 1:
        if targetbot != bot.nick:
            osd(bot, [botcom.channel_current], 'say', trigger.nick + " commanded me to update " + targetbot + " from Github and restart.")
        else:
            dungeonmasterarray = ['spiceRPG', 'spiceRPGdev']
            if targetbot in dungeonmasterarray:
                osd(bot, botcom.channel_list, 'say', "My Dungeon Master, " + trigger.nick + ", hath commandeth me to performeth an update from the Hub of Gits. I shall return post haste!")
            else:
                osd(bot, botcom.channel_list, 'say', trigger.nick + " commanded me to update from Github and restart. Be Back Soon!")
    else:
        targetbotlist = spicemanip(bot, targetbots, 'list')
        osd(bot, [botcom.channel_current], 'say', trigger.nick + " commanded me to update " + targetbotlist + " from Github and restart.")
    for targetbot in targetbots:
        update(bot, botcom, trigger, targetbot)
        restart(bot, botcom, trigger, targetbot)


def bot_command_function_restart(bot, trigger, botcom, instigator):

    botcom = bot_config_directory(bot, botcom)

    targetbot = spicemanip(bot, [x for x in botcom.triggerargsarray if x in botcom.config_listing], 1) or bot.nick

    if targetbot == bot.nick:
        if botcom.instigator not in botcom.botadmins:
            osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
            return
    else:
        targetbotadmins = bot_target_admins(bot, targetbot)
        if botcom.instigator not in targetbotadmins:
            osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
            return

    joindpath = os.path.join("/home/spicebot/.sopel/", targetbot)
    if not os.path.isdir(joindpath):
        osd(bot, botcom.instigator, 'notice', "That doesn't appear to be a valid bot directory.")
        return

    if targetbot != bot.nick:
        osd(bot, [botcom.channel_current], 'say', trigger.nick + " commanded me to restart " + targetbot + ". Be Back Soon!")
    else:
        dungeonmasterarray = ['spiceRPG', 'spiceRPGdev']
        if targetbot in dungeonmasterarray:
            osd(bot, botcom.channel_list, 'say', "My Dungeon Master, " + botcom.instigator + ", commandeth me to restart. I shall return post haste!")
        else:
            osd(bot, botcom.channel_list, 'say', trigger.nick + " commanded me to restart. Be Back Soon!")
    restart(bot, botcom, trigger, targetbot)


def bot_command_function_permfix(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.botadmins:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    os.system("sudo chown -R spicebot:sudo /home/spicebot/.sopel/")
    osd(bot, botcom.channel_current, 'say', "Permissions should now be fixed")


def bot_command_function_pip(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.botadmins:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    pippackage = spicemanip(bot, botcom.triggerargsarray, '2+')
    if not pippackage:
        osd(bot, botcom.channel_current, 'say', "You must specify a pip package.")
    else:
        osd(bot, botcom.channel_current, 'say', "Attempting to install " + str(pippackage))
        os.system("sudo pip install " + pippackage)
        osd(bot, botcom.channel_current, 'say', "Possibly done installing " + str(pippackage))


def bot_command_function_debug(bot, trigger, botcom, instigator):

    botcom = bot_config_directory(bot, botcom)
    targetbot = spicemanip(bot, [x for x in botcom.triggerargsarray if x in botcom.config_listing], 1) or bot.nick

    if targetbot == bot.nick:
        if botcom.instigator not in botcom.botadmins:
            osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
            return
    else:
        targetbotadmins = bot_target_admins(bot, targetbot)
        if botcom.instigator not in targetbotadmins:
            osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
            return

    joindpath = os.path.join("/home/spicebot/.sopel/", targetbot)
    if not os.path.isdir(joindpath):
        osd(bot, botcom.instigator, 'notice', "That doesn't appear to be a valid bot directory.")
        return

    debugloglinenumberarray = []
    osd(bot, botcom.channel_current, 'action', "Is Copying Log")
    os.system("sudo journalctl -u " + targetbot + " >> " + log_file_path)
    osd(bot, botcom.channel_current, 'action', "Is Filtering Log")
    search_phrase = "Welcome to Sopel. Loading modules..."
    ignorearray = ['session closed for user root', 'COMMAND=/bin/journalctl', 'COMMAND=/bin/rm', 'pam_unix(sudo:session): session opened for user root']
    mostrecentstartbot = 0
    with open(log_file_path) as f:
        line_num = 0
        for line in f:
            line = line.decode('utf-8', 'ignore')
            line_num += 1
            if search_phrase in line:
                mostrecentstartbot = line_num
        line_num = 0
    with open(log_file_path) as fb:
        for line in fb:
            line_num += 1
            currentline = line_num
            if int(currentline) >= int(mostrecentstartbot) and not any(x in line for x in ignorearray):
                osd(bot, botcom.channel_current, 'say', str(line))
    osd(bot, botcom.channel_current, 'action', "Is Removing Log")
    os.system("sudo rm " + log_file_path)


"""
# Bot Restart/Update
"""


def restart(bot, botcom, trigger, service):
    osd(bot, botcom.channel_current, 'action', "Is Restarting the " + service + " Service...")
    os.system("sudo service " + str(service) + " restart")
    if bot.nick == service:
        osd(bot, botcom.channel_current, 'say', "If you see this, the service is hanging. Making another attempt.")
        os.system("sudo service " + str(service) + " restart")


def update(bot, botcom, trigger, targetbot):
    os.system("sudo chown -R spicebot:sudo /home/spicebot/.sopel/")
    joindpath = os.path.join("/home/spicebot/.sopel/", targetbot)
    osd(bot, botcom.channel_current, 'action', "Is Pulling " + str(joindpath) + " From Github...")
    g = git.cmd.Git(joindpath)
    g.pull()


"""
dir listing
"""


def bot_list_directory(bot, botcom):
    botcom.directory_listing = []
    botcom.filefoldertype = []
    for filename in os.listdir(botcom.directory):
        botcom.directory_listing.append(filename)
        joindpath = os.path.join(botcom.directory, filename)
        if os.path.isfile(joindpath):
            botcom.filefoldertype.append("file")
        else:
            botcom.filefoldertype.append("folder")
    return botcom


def bot_config_directory(bot, botcom):
    botcom.config_listing = []
    networkname = str(bot.config.core.user.split("/", 1)[1] + "/")
    validconfigsdir = str("/home/spicebot/.sopel/" + bot.nick + "/System-Files/Configs/" + networkname)
    for filename in os.listdir(validconfigsdir):
        filenameminuscfg = str(filename).replace(".cfg", "")
        botcom.config_listing.append(filenameminuscfg)
    return botcom


def bot_target_admins(bot, targetbot):
    targetbotadmins = []
    networkname = str(bot.config.core.user.split("/", 1)[1] + "/")
    configfile = str("/home/spicebot/.sopel/" + targetbot + "/System-Files/Configs/" + networkname + targetbot + ".cfg")
    config = ConfigParser.ConfigParser()
    config.read(configfile)
    owner = config.get("core", "owner")
    targetbotadmins.append(owner)
    admins = config.get("core", "admins")
    admins = admins.split(",")
    for admin in admins:
        if admin not in targetbotadmins:
            targetbotadmins.append(admin)
    return targetbotadmins


"""
uptime.py - Uptime module
Copyright 2014, Fabian Neundorf
Licensed under the Eiffel Forum License 2.

https://sopel.chat
"""


def setup(bot):
    if "uptime" not in bot.memory:
        bot.memory["uptime"] = datetime.datetime.utcnow()


def bot_command_function_uptime(bot, trigger, botcom, instigator):
    """.uptime - Returns the uptime of Sopel."""
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() -
                                              bot.memory["uptime"])
                                             .total_seconds()))
    osd(bot, trigger.sender, 'say', "I've been sitting here for {} and I keep going!".format(delta))
