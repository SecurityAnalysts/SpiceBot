#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
# These help parse the info from the webpage
import requests
from lxml import html
from fake_useragent import UserAgent
# new book is Midnight GMT/BST (does not follow UTC)
from datetime import datetime, timedelta
import time
from pytz import timezone
tz = timezone('Europe/London')
packthour = str(0)
packtminute = str(10)
# SpiceBotShared
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

packturl = "https://www.packtpub.com/packt/offers/free-learning"


@sopel.module.commands('packt')
def execute_main(bot, trigger):
    osd(bot, trigger.sender, 'say', packt_osd(bot))


@sopel.module.interval(60)
def getpackt(bot):
    now = datetime.datetime.now(tz)
    if now.hour == int(packthour) and now.minute == int(packtminute):
        dispmsg = packt_osd(bot)
        for channel in bot.channels:
            osd(bot, channel, 'say', dispmsg)


def packt_osd(bot):
    dispmsg = []
    dispmsg.append("[Packt] " + getPacktTitle())
    dispmsg.append("Next Book: " + getpackttimediff(bot))
    dispmsg.append("URL: " + packturl)
    return dispmsg


def getPacktTitle():
    title = ''
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    page = requests.get(packturl, headers=header)
    if page.status_code == 200:
        tree = html.fromstring(page.content)
        title = str(tree.xpath('//*[@id="deal-of-the-day"]/div/div/div[2]/div[2]/h2/text()'))
        title = title.replace("\\t", "")
        title = title.replace("\\n", "")
        title = title.replace("['", "")
        title = title.replace("']", "")
    if title == "[]" or title == '':
        title = "No Book Today"
    return title


def getpackttimediff(bot):
    nowtime = datetime.datetime.now(tz)
    tomorrow = nowtime + timedelta(days=1)
    packtnext = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, int(packthour), int(packtminute), 0, 0)
    timecompare = get_timeuntil(nowtime, packtnext)
    packttimediff = str(timecompare)
    return packttimediff
