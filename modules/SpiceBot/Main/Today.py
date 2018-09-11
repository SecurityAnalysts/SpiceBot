#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import datetime
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

deities = ['God', 'Cthulhu', 'Landru', 'Odin', 'Satan', 'Developer', 'Frigg', 'Hades', 'Zeus', 'Lord deathbybandaid', 'Ra']


@sopel.module.commands('today', 'whatdayisit')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'today')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    whatistoday, whatdayofweek = whatdayofweeknow()
    daystilfriday = howlonguntilfriday(bot, whatistoday)
    if whatdayofweek == 'Monday':
        specialmsg = "Mondays Suck!"
    if whatdayofweek == 'Tuesday':
        specialmsg = "...but at least it's not Monday."
    if whatdayofweek == 'Wednesday':
        specialmsg = "Today is Wednesday, AKA HUMPDAY!!!!"
    if whatdayofweek == 'Thursday':
        specialmsg = "...but at least it's not Monday."
    if whatdayofweek == 'Friday':
        specialmsg = ""
    if whatdayofweek == 'Saturday':
        specialmsg = ""
    if whatdayofweek == 'Sunday':
        specialmsg = ""
    botmotd = str("Today is " + str(whatdayofweek) + ". " + str(daystilfriday) + " " + str(specialmsg))
    osd(bot, trigger.sender, 'say', botmotd)


def howlonguntilfriday(bot, whatistoday):
    fridaynumber = '4'
    if whatistoday == fridaynumber:
        deityofchoice = spicemanip(bot, deities, 'random')
        daystilfriday = "Thank " + str(deityofchoice) + " It's Friday! It's finally here!!!"
    elif whatistoday == '5' or whatistoday == '6':
        daystilfriday = "It's the Weekend!"
    else:
        daysmath = int(fridaynumber) - int(whatistoday)
        if daysmath == int('1'):
            daystilfriday = "Unfortunately Friday is " + str(daysmath) + " day away. I'm sure we'll make it there!"
        else:
            daystilfriday = "Unfortunately Friday is " + str(daysmath) + " days away. I'm sure we'll make it there!"
    return daystilfriday


def whatdayofweeknow():
    whatistoday = str(datetime.datetime.today().weekday())
    if whatistoday == '0':
        whatdayofweek = "Monday"
    elif whatistoday == '1':
        whatdayofweek = "Tuesday"
    elif whatistoday == '2':
        whatdayofweek = "Wednesday"
    elif whatistoday == '3':
        whatdayofweek = "Thursday"
    elif whatistoday == '4':
        whatdayofweek = "Friday"
    elif whatistoday == '5':
        whatdayofweek = "Saturday"
    elif whatistoday == '6':
        whatdayofweek = "Sunday"
    return whatistoday, whatdayofweek
