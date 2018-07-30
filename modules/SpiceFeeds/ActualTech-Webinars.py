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
import pytz
from dateutil import tz
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

url = 'https://events.actualtechmedia.com'


@sopel.module.commands('atwebby')
def execute_main(bot, trigger):
    # webbyauto(bot)
    page = requests.get(url, headers=None)
    if page.status_code == 200:
        dispmsg = []
        dispmsg.append("[ActualTech Webinar]")
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
        now = now.replace(tzinfo=pytz.UTC)
        webbytime = getwebbytime()
        timeuntil = (webbytime - now).total_seconds()
        if int(timeuntil) < 900 and int(timeuntil) > 840:
            dispmsg = []
            dispmsg.append("[ActualTech Webinar]")
            dispmsg.append("{"+getwebbytimeuntil()+"}")
            dispmsg.append(getwebbytitle())
            dispmsg.append(getwebbylink())
            bonus = getwebbybonus()
            if bonus and bonus != '':
                dispmsg.append('BONUS: ' + getwebbybonus())
            for channel in bot.channels:
                osd(bot, channel, 'say', dispmsg)


def getwebbytitle():
    tree = gettree()
    webbytitle = str(tree.xpath('//*[@id="HeaderUpcoming"]/div/div[1]/h2/a/text()'))
    for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
        webbytitle = webbytitle.replace(*r)
    webbytitle = unicode_string_cleanup(webbytitle)
    return webbytitle


def getwebbytimeuntil():
    nowtime = datetime.datetime.utcnow()
    webbytime = getwebbytime()
    timecompare = get_timeuntil(nowtime, webbytime)
    return timecompare


def getwebbytime():
    now = datetime.datetime.utcnow()
    tree = gettree()
    webbytime = str(tree.xpath('//*[@id="HeaderUpcoming"]/div/div[1]/cite/time/text()'))
    # webbytime = str(tree.xpath('//*[@id="HeaderUpcoming"]/div/div[1]/cite/span[1]/text()'))
    for r in (("['", ""), ("']", ""), ("\\n", ""), ("\\t", ""), ("@ ", "")):
        webbytime = webbytime.replace(*r)
    webbytz = pytz.timezone('US/Eastern')
    webbytime = parser.parse(str(webbytime))
    webbytime = webbytz.localize(webbytime)
    return webbytime


def getwebbylink():
    tree = gettree()
    webbylink = str(tree.xpath('//*[@id="HeaderUpcoming"]/div/div[1]/a/@href'))
    for r in (("['", ""), ("']", "")):
        webbylink = webbylink.replace(*r)
    webbylink = str(url + webbylink.split("&", 1)[0])
    return webbylink


def getwebbybonus():
    tree = gettree()
    try:
        webbybonus = str(tree.xpath('//*[@id="HeaderUpcoming"]/div/div[2]/h3/a/strong/strong/text()'))
        for r in (("\\r", ""), ("\\n", ""), ("']", ""), ("]", ""), ('"', ''), (" '", ""), ("['", "")):
            webbybonus = webbybonus.replace(*r)
        webbybonus = unicode_string_cleanup(webbybonus)
    except IndexError:
        webbybonus = ''
    return webbybonus


def gettree():
    page = requests.get(url, headers=None)
    tree = html.fromstring(page.content)
    return tree
