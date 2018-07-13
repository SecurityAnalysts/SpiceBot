
# !/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('toodamnhigh','toohigh')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'toodamnhigh')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):
    keyword = trigger.group(2)
    if not keyword:
        keyword = 'rent'
    message = 'The ' + str(keyword) + ' IS TOO DAMN HIGH!'
    onscreentext(bot,['say'],message)
