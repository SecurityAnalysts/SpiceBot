#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from xml.dom import minidom
from fake_useragent import UserAgent
import sys
import os
import ConfigParser
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}


@sopel.module.require_admin
@sopel.module.commands('ytrssreset')
def reset(bot, trigger):
    feedselect = trigger.group(2)
    RSSFEEDSDIR = str("/home/spicebot/.sopel/" + bot.nick + "/RSS-Feeds/youtube/")
    if not feedselect:
        osd(bot, trigger.sender, 'say', "Which Feed are we resetting?")
    elif feedselect == 'all':
        for filename in os.listdir(RSSFEEDSDIR):
            osd(bot, trigger.sender, 'say', 'Resetting LastBuildTime for ' + str(filename))
            bot.db.set_nick_value(bot.nick, filename + '_lastbuildcurrent', None)
    else:
        istherafeed = bot.db.get_nick_value(bot.nick, feedselect + '_lastbuildcurrent') or 0
        if istherafeed:
            osd(bot, trigger.sender, 'say', 'Resetting LastBuildTime for ' + str(feedselect))
            bot.db.set_nick_value(bot.nick, feedselect + '_lastbuildcurrent', None)
        else:
            osd(bot, trigger.sender, 'say', "There doesn't appear to be record of that feed.")


# Automatic Run
@sopel.module.interval(600)
def autorss(bot):
    RSSFEEDSDIR = str("/home/spicebot/.sopel/" + bot.nick + "/RSS-Feeds/youtube/")
    rssarray = []
    for filename in os.listdir(RSSFEEDSDIR):
        rssarray.append(filename)
    for rssfeed in rssarray:
        configfile = os.path.join(RSSFEEDSDIR, rssfeed)
        config = ConfigParser.ConfigParser()
        config.read(configfile)
        feedname = config.get("configuration", "feedname")
        url = str(config.get("configuration", "url"))
        dispmsg = []
        dispmsg.append("["+feedname+"]")
        page = requests.get(url, headers=header)
        if page.status_code == 200:
            xml = page.text
            xml = xml.encode('ascii', 'ignore').decode('ascii')
            xmldoc = minidom.parseString(xml)
            lastBuildXML = xmldoc.getElementsByTagName('published')
            lastBuildXML = lastBuildXML[2].childNodes[0].nodeValue
            lastBuildXML = str(lastBuildXML)
            lastbuildcurrent = bot.db.get_nick_value(bot.nick, rssfeed + '_lastbuildcurrent') or 0
            newcontent = True
            if lastBuildXML.strip() == lastbuildcurrent:
                newcontent = False
            if newcontent:
                titles = xmldoc.getElementsByTagName('title')
                title = titles[1].childNodes[0].nodeValue
                links = xmldoc.getElementsByTagName('link')
                link = links[2].getAttribute('href')
                lastbuildcurrent = lastBuildXML.strip()
                bot.db.set_nick_value(bot.nick, rssfeed + '_lastbuildcurrent', lastbuildcurrent)
                dispmsg.append(title)
                dispmsg.append(link)
                for channel in bot.channels:
                    osd(bot, channel, 'say', dispmsg)
