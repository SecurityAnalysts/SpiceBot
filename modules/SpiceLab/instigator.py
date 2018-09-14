#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('instigator')
def execute_main(bot, trigger):

    # botcom
    botcom = class_create('bot')

    # User
    botcom = bot_command_users(bot, botcom)

    # Channels
    botcom = bot_command_channels(bot, botcom, trigger)

    # instigator
    instigator = class_create('instigator')
    osd(bot, trigger.sender, 'say', ".default before " + instigator.default)
    botcom.instigator = trigger.nick
    osd(bot, trigger.sender, 'say', ".default after " + instigator.default)

    osd(bot, trigger.sender, 'say', "string wrapped " + str(instigator))
    osd(bot, trigger.sender, 'say', "no wrap " + instigator)

    if instigator in botcom.users_all:
        osd(bot, trigger.sender, 'say', "in the user list")
    else:
        osd(bot, trigger.sender, 'say', "not in the user list")


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
