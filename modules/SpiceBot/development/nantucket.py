#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author yournamehere


@sopel.module.commands('nantucket')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'nantucket')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    command = get_trigger_arg(bot, triggerargsarray, 1)
    if command == dirty:
        osd(bot, trigger.sender, 'say', "There was a young man from Nantucket; Whose dick was so long he could suck it.; He said with a grin; As he wiped off his chin,; If my ear was a cunt I would fuck it.")
    else:
        rand = random.randint(1,3)
        if rand == 1:
            osd(bot, trigger.sender, 'say', "There once was a man from Nantucket; Who kept all his cash in a bucket.; But his daughter, named Nan,; Ran away with a man; And as for the bucket, Nantucket.")
        elif rand == 2:
            osd(bot, trigger.sender, 'say', "But he followed the pair to Pawtucket,; The man and the girl with the bucket; And he said to the man,; He was welcome to Nan,; But as for the bucket, Pawtucket.")
        elif rand == 3:
            osd(bot, trigger.sender, 'say', "Then the pair followed Pa to Manhasset,; Where he still held the cash as an asset,; But Nan and the man; Stole the money and ran,; And as for the bucket, Manhasset.")
