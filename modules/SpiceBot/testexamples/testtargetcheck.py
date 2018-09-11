# to be added to spicebot shared after testing

from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)

shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('testtarget')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, '1+')
    isvalid, validmsg = targetcheck(bot, botcom, target, instigator)
    osd(bot, trigger.sender, 'say', validmsg)
