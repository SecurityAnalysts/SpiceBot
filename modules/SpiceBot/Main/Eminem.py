import sopel.module
import random
import urllib
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

fra = 'https://raw.githubusercontent.com/SpiceBot/SpiceBot/master/Text-Files/momsspaghetti.txt'


@sopel.module.commands('eminem')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    if not trigger.group(2):
        myline = randomfra()
        osd(bot, trigger.sender, 'say', myline)


# random rule
def randomfra():
    htmlfile = urllib.urlopen(fra)
    lines = htmlfile.read().splitlines()
    myline = random.choice(lines)
    if not myline or myline == '\n':
        myline = randomfra()
    return myline
