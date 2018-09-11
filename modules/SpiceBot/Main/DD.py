#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

insultnames = ['motherfucker','prick','wanker']
usernames = ['user','LUser','Luser','bitch']


@sopel.module.commands('dd','doubled')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'dd')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 1)
    insult = spicemanip(bot, insultnames, 'random')
    isvalid, validmsg = targetcheck(bot, botcom, target, instigator)
    if not target:
        osd(bot, trigger.sender, 'say', "Who are you pissed at now?")
    elif target == 'cert':
        osd(bot, trigger.sender, 'say', "Here is the link to DD link for the noobs who have never seen it before. https://ibb.co/ibxD2n")
    elif target == 'certification':
        osd(bot, trigger.sender, 'say', "Here is the link to DD link for the noobs who have never seen it before. https://ibb.co/ibxD2n")
    elif isvalid == 1:
        osd(bot, trigger.sender, 'action', 'punches ' + target + ', who is clearly a ' + str(insult) + ', in the mouth.')
    elif isvalid == 0:
        osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
    elif isvalid == 3:
        osd(bot, trigger.sender, 'say', "Ummm, no. Dumbass.")
    else:
        osd(bot, trigger.sender, 'action', 'punches ' + target + ', who is clearly a ' + str(insult) + ', in the mouth.')
