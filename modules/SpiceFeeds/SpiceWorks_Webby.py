#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from lxml import html
import datetime
from time import strptime
from dateutil import parser
import calendar
import arrow
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

url = 'https://community.spiceworks.com/calendar'


@sopel.module.commands('spicewebby')
def execute_main(bot, trigger):
    # webbyauto(bot)
    page = requests.get(url, headers=None)
    if page.status_code == 200:
        dispmsg = []
        dispmsg.append("[Spiceworks Webinar]")
        dispmsg.append("{"+getwebbytimeuntil()+"}")
        dispmsg.append(getwebbytitle())
        dispmsg.append(getwebbylink())
        bonus = getwebbybonus()
        if bonus and bonus != '':
            dispmsg.append('BONUS: ' + getwebbybonus())
        osd(bot, trigger.sender, 'say', dispmsg)


@sopel.module.interval(60)
def webbyauto(bot):
    page = requests.get(url, headers=None)
    if page.status_code == 200:
        now = datetime.datetime.utcnow()
        webbytime = getwebbytime()
        timeuntil = (webbytime - now).total_seconds()
        if int(timeuntil) < 900 and int(timeuntil) > 840:
            dispmsg = []
            dispmsg.append("[Spiceworks Webinar Reminder]")
            dispmsg.append("{"+getwebbytimeuntil()+"}")
            dispmsg.append(getwebbytitle())
            dispmsg.append(getwebbylink())
            bonus = getwebbybonus()
            if bonus and bonus != '':
                dispmsg.append('BONUS: ' + getwebbybonus())
            for channel in bot.channels:
                osd(bot, channel, 'say', dispmsg)


def getwebbytime():
    now = datetime.datetime.utcnow()
    tree = gettree()
    webbytime = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[1]/div[2]/span[@title]/@datetime'))
    for r in (("['", ""), ("']", "")):
        webbytime = webbytime.replace(*r)
    webbytime = str(webbytime.split("+", 1)[0])
    webbytime = parser.parse(webbytime)
    return webbytime


def getwebbytitle():
    tree = gettree()
    webbytitle = str(tree.xpath('//*[@id="primary"]/div[2]/ul/li[1]/div[2]/div[2]/a/text()'))
    for r in (("u'", ""), ("['", ""), ("[", ""), ("']", "")):
        webbytitle = webbytitle.replace(*r)
    webbytitle = unicode_string_cleanup(webbytitle)
    return webbytitle


def getwebbylink():
    tree = gettree()
    # webbylink = str(tree.xpath('//*[@id="primary"]/div[2]/ul/li[1]/div[2]/div[2]/a/@href'))
    webbylink = str(tree.xpath('//*[@id="primary"]/div[2]/ul/li[1]/div[2]/div[4]/div[4]/a/@href'))
    for r in (("['", ""), ("']", "")):
        webbylink = webbylink.replace(*r)
    # webbylink = str(webbylink.split("&", 1)[0])
    webbylink = str("https://community.spiceworks.com" + webbylink)
    return webbylink


def getwebbybonus():
    tree = gettree()
    try:
        webbybonus = str(tree.xpath('//*[@id="primary"]/div[2]/ul/li[1]/div[2]/div[4]/div[1]/p[1]/text()'))
        # webbybonus = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/div[2]/p/text()'))
        webbybonus = str(webbybonus.split("BONUS: ", 1)[1])
        for r in (("\\r", ""), ("\\n", ""), ("']", ""), ("]", ""), ('"', ''), (" '", "")):
            webbybonus = webbybonus.replace(*r)
        webbybonus = unicode_string_cleanup(webbybonus)
    except IndexError:
        webbybonus = ''
    return webbybonus


def getwebbytimeuntil():
    nowtime = datetime.datetime.utcnow()
    webbytime = getwebbytime()
    timecompare = get_timeuntil(nowtime, webbytime)
    return timecompare


def gettree():
    page = requests.get(url, headers=None)
    tree = html.fromstring(page.content)
    return tree
