#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from datetime import datetime
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('sysadmin', 'sysadminday')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'sysadmin')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    today = datetime.datetime.now()
    sysadminday = datetime.datetime.strptime('Jul 27 2018', '%b %d %Y')
    if sysadminday > today:
        daystillsysadminday = sysadminday - today
        message = "There are " + str(daystillsysadminday.days) + " days till SysAdmin day"
    elif sysadminday < today:
        daystillsysadminday = sysadminday - today
        message = "SysAdmin day happened " + str(daystillsysadminday.days) + " ago."
    else:
        message = "Happy Sysadmin day"
    osd(bot, trigger.sender, 'say', message)


# @sopel.module.interval(60)
# def getpackt(bot):
#     now = datetime.datetime.now(tz)
#     if now.hour == int(packthour) and now.minute == int(packtminute):
#         dispmsg = packt_osd(bot)
#         for channel in bot.channels:
#             osd(bot, channel, 'say', dispmsg)
#
#
# def packt_osd(bot):
#     dispmsg = []
#     dispmsg.append("[Packt] " + getPacktTitle())
#     dispmsg.append("Next Book: " + getpackttimediff(bot))
#     dispmsg.append("URL: " + packturl)
#     return dispmsg
#
#
# def getpackttimediff(bot):
#     nowtime = datetime.datetime.now(tz)
#     tomorrow = nowtime + timedelta(days=1)
#     packtnext = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, int(packthour), int(packtminute), 0, 0)
#     timecompare = get_timeuntil(nowtime, packtnext)
#     packttimediff = str(timecompare)
#     return packttimediff
