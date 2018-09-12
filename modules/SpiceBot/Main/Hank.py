#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('hank')
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
    hank_quotes = [
                    "The only reason why your nails should be black is because you hit them with a hammer.",
                    "He always leaves the TV on the Game Show network. I'm not sure why it bothers me, but it does",
                    "You called in a fake propane emergency? That's a $50 fine after I report it.",
                    "Bobby, from now on when I ask you how your day was, what I mean is 'how was shop'?",
                    "The only woman I'm pimping is sweet lady propane! And I'm tricking her out all over this town.",
                    'Maybe my father is Tom Landry. That would explain my strong chin and my love for the flex defense. I wonder if I would call him "dad" or "coach". Nah who am I kidding? I would call him "sir".',
                    "If Bobby doesn't love football, he won't lead a fulfilling life, and then he'll die.",
                    "I wasn't flirting with her! I didn't even mention that I worked in propane.",
                    "Why are we watching a foreign movie? You'd think if it was any good they would make an American version.",
                    "I'm not saying you're not good at what you do. I'm just saying I'm better.",
                    "You can't just pick and choose which laws to follow. Sure I'd like to tape a baseball game without the express written consent of major league baseball, but that's just not the way it works.",
                    "I can't enjoy a party until I know where the bathroom is. You knew that when you married me.",
                    "Bobby, if you weren't my son, I'd hug you.",
                    "Bobby I'm going to tell you to do two things I hope you never have to do again, tape the Cowboys game and fetch me an apron.",
                    "That boy ain't right.",
                    "Yep"]
    randomhank = spicemanip(bot, hank_quotes, 'random')
    osd(bot, trigger.sender, 'say', randomhank)
