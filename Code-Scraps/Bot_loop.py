"""
Module for getting the bots into an infinite loop
http://sopel.chat
"""

from sopel.module import rule, priority, rate
import random
import time
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('test')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'test')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    human = random.uniform(0, 30)  # Random number with uniform chances across range
    time.sleep(human)  # Wait for random time
    prefix = "!"
    command = "test"
    osd(bot, trigger.sender, 'say', prefix + command)
