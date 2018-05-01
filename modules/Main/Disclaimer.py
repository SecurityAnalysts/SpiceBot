#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

specifics = ['brightlights','doctor','EULA','IT','Cipher-0','Cipher','IT_Sean']

@sopel.module.commands('disclaimer')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    subdisclaimer = get_trigger_arg(bot,triggerargsarray,1)
    if subdisclaimer in specifics:
        if subdisclaimer == 'brightlights':
            bot.say("Individuals sensitive to bright lights or with epilepsy may find the quick bright text the bot speaks with to be troublesome. Any epileptic reaction is not the fault of the bot, the channel, or its denizens.")
        if subdisclaimer == 'doctor':
            bot.say(instigator + " is not your doctor. The views/opinions/information expressed by " + instigator + " is not intended or implied to be a substitute for professional medical advice, diagnosis or treatment.")
        if subdisclaimer == 'EULA':
            bot.say("Spicebot may occasionally (read 'frequently') use colorful language to carry out its tasks. By remaining in this channel and continuing to use the bot you acknowledge that you are not, in fact, too weak to handle this fact.")
        if subdisclaimer == 'IT':
            bot.say("While most members of this channel have some level of technical knowledge, your decision to trust the recommendations of " + instigator + " are entirely your own risk.")
        if subdisclaimer == 'Cipher-0' or 'Cipher':
            bot.say("Frivolously pestering Cipher-0 comes with a high risk of termination, " + instigator)
        if subdisclaimer == 'IT_Sean':
            bot.say("Should you ever encounter gases released by IT_Sean, please be sure to inform your nearest biosafety agency of the incident.")
    else:
        bot.say(instigator + " is not your doctor. The views/opinions/information expressed by " + instigator + " is not intended or implied to be a substitute for professional medical advice, diagnosis or treatment.")
