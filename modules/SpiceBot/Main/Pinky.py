#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib
from xml.dom.minidom import parseString
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('pinky')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'pinky')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    item = spicemanip(bot, triggerargsarray, '1+')
    if not item:
        message = "How can you have anything good if you don't eat your meat!?!"
    else:
        message = "How can you have any %s if you don't eat your meat!?!" % item
    osd(bot, instigator, 'say', message)
