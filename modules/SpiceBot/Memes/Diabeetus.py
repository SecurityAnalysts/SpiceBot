import sopel.module
import random
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('diabeetus')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'diabeetus')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    messages = [
                "Good morning. I'm Wilford Brimley and I'd like to talk to you about Diabeetus.",
                "If you have type 2 Diabeetus, you can get your testing supplies free..."]
    message = spicemanip(bot, messages, 'random')
    osd(bot, trigger.sender, 'say', message)
