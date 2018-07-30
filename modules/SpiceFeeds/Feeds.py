#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import ConfigParser
import requests
from xml.dom import minidom
from fake_useragent import UserAgent
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

# author deathbybandaid

feeds_dir = "feeds/"
feeds_file_path = os.path.join(moduledir, feeds_dir)


@sopel.module.commands('feeds')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    # feeds dynamic Class
    feeds = class_create('feeds')

    valid_commands = ['enable', 'disable', 'reset', 'run']
    command = get_trigger_arg(bot, [x for x in triggerargsarray if x in valid_commands], 1) or 'run'
    if command in triggerargsarray:
        triggerargsarray.remove(command)

    feeds = feeds_configs(bot, feeds)

    bot.say(str(feeds.list))

    if command == 'reset':
        bot.say("reset")
        return

    elif command == 'enable':
        bot.say("enable")
        return

    elif command == 'disable':
        bot.say("disable")
        return

    elif command == 'run':
        bot.say("run")
        return


# rss feeds list
def feeds_configs(bot, feeds):
    feeds.list = []
    for feed_dir_type in os.listdir(feeds_file_path):
        feed_type_file_path = os.path.join(feeds_file_path, feed_dir_type)
        for feed in os.listdir(feed_type_file_path):

            # Add to main list
            feeds.list.append(feed)

            # Every feed gets a class
            current_feed = class_create(feed)
            exec("feeds." + feed + " = current_feed")

            # file name
            exec("feeds." + feed + ".feed_filename = feed")

            # get file path
            feedfile = os.path.join(feed_type_file_path, feed)
            exec("feeds." + feed + ".file_path = feedfile")

            # Read configuration
            config = ConfigParser.ConfigParser()
            config.read(feedfile)
            for each_section in config.sections():
                for (each_key, each_val) in config.items(each_section):
                    exec("feeds." + feed + "." + each_key + " = each_val")

    for feed in feeds.list:
        feed_name = eval("feeds." + feed + ".displayname")
        feed_url = eval("feeds." + feed + ".url")
        feed_type = eval("feeds." + feed + ".type")
        bot.say("[" + str(feed_type) + "] " + str(feed_name) + " " + str(feed_url))

    return feeds
