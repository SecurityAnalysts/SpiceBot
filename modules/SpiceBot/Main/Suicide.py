from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('suicide', 'savealife')
def mainfunction(bot, trigger):
    """Check to see if the module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'suicide')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Respond with suicide prevention agency details."""
    url = "https://suicidepreventionlifeline.org/"
    phonenumber = "1-800-273-8255"
    message = "If you or someone you know is having a crisis and needs someone to talk to call " + phonenumber + " or visit: " + url
    osd(bot, trigger.sender, 'say', message)
