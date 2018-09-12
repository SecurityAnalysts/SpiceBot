#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import re
from num2words import num2words
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('ermahgerd')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'ermahgerd')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    ernpert = spicemanip(bot, triggerargsarray, 0)
    if ernpert:
        spertitert = trernslert(ernpert)
        message = "ERMAHGERD," + str(spertitert)
    else:
        message = "Whert der yer wernt ter trernslert?"
    osd(bot, trigger.sender, 'say', message)


def trernslert(werds):
    terkerns = werds.split()
    er = ''
    for terk in terkerns:

        if terk.endswith(','):
            terk = re.sub(r"[,]+", '', terk)
            cermmer = 'true'
        else:
            cermmer = 'false'

        if terk.startswith('('):
            terk = re.sub(r"[(]+", '', terk)
            lerftperernthersers = 'true'
        else:
            lerftperernthersers = 'false'

        if terk.endswith(')'):
            terk = re.sub(r"[)]+", '', terk)
            rerghtperernthersers = 'true'
        else:
            rerghtperernthersers = 'false'

        if terk.endswith('%'):
            terk = re.sub(r"[%]+", '', terk)
            percernt = 'true'
        else:
            percernt = 'false'

        werd = ermergerd(terk)

        if lerftperernthersers == 'true':
            werd = str('(' + werd)

        if percernt == 'true':
            werd = str(werd + ' PERCERNT')

        if rerghtperernthersers == 'true':
            werd = str(werd + ')')

        if cermmer == 'true':
            werd = str(werd + ',')
        cermmer

        er = er + ' ' + werd
    return er


def ermergerd(w):
    w = w.strip().lower()
    derctshernerer = {'me': 'meh', 'you': 'u', 'are': 'er', "you're": "yer", "i'm": "erm", "i've": "erv", "my": "mah", "the": "da", "omg": "ermahgerd"}
    if w in derctshernerer:
        return derctshernerer[w].upper()
    else:
        w = re.sub(r"[\.,/;:!@#$%^&*\?)(]+", '', w)
        if w[0].isdigit():
            w = num2words(int(w))
        w = re.sub(r"tion", "shun", w)
        pat = r"[aeiouy]+"
        er = re.sub(pat, "er", w)
        if w.startswith('y'):
            er = 'y' + re.sub(pat, "er", w[1:])
        if w.endswith('e') and not w.endswith('ee') and len(w) > 3:
            er = re.sub(pat, "er", w[:-1])
        if w.endswith('ing'):
            er = re.sub(pat, "er", w[:-3]) + 'in'
        er = er[0] + er[1:].replace('y', 'er')
        er = er.replace('rr', 'r')
        return er.upper()
