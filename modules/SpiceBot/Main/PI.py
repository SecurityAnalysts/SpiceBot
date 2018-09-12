from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
from sopel import module, tools
import random
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
import decimal


@sopel.module.commands('pi')
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
    pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679'
    digitcount = spicemanip(bot, triggerargsarray, 1) or ''
    if not digitcount == '':
        if not digitcount.isdigit():
            osd(bot, trigger.sender, 'say', "Please enter the number of digits you want to see.")
        else:
            digits = int(digitcount)+2
            pilength = len(pi)
            if digits >= 1 and digits <= pilength:
                mynumber = pi[0:digits]
                osd(bot, trigger.sender, 'say', str(mynumber))
            else:
                osd(bot, trigger.sender, 'say', "Please select a number of decimal places between 1 and " + str(pilengh))
    else:
        osd(bot, trigger.sender, 'say', str(pi))
