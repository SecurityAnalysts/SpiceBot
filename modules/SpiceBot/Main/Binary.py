#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('binary')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'binary')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    current_translate = spicemanip(bot, triggerargsarray, 0) or 0
    if not current_translate:
        spititout = randint(0, 1)
    elif not str(current_translate).isdigit():
        spititout = str(string2bits(current_translate)) or 'error'
        spititout = spititout.replace("[", "")
        spititout = spititout.replace("]", "")
        spititout = spititout.replace("'", "")
        spititout = spititout.replace(",", "")
        spititout = spititout.replace(" ", "")
    else:
        spititout = bits2string(current_translate) or 'error'
    osd(bot, trigger.sender, 'action', str(spititout))


def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]


def bits2string(b=None):
    return ''.join(chr(int(b[i*8:i*8+8], 2)) for i in range(len(b)//8))
