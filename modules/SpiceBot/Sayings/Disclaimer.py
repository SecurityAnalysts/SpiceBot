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

specifics = ['brightlights','doctor','EULA','IT','legal','law','Cipher-0','Cipher','IT_Sean','parent','pornhub','porn']

@sopel.module.commands('disclaimer')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'disclaimer')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    subdisclaimer = get_trigger_arg(bot,triggerargsarray,1)
    person = get_trigger_arg(bot,triggerargsarray,2) or instigator
    if subdisclaimer == 'options':
        bot.say("Current options for this module are: %s" % get_trigger_arg(bot,specifics,'list'))
    elif subdisclaimer in specifics:
        if subdisclaimer == 'brightlights':
            bot.say("Individuals sensitive to bright lights or with epilepsy may find the quick bright text the bot speaks with to be troublesome. Any epileptic reaction is not the fault of the bot, the channel, or its denizens.")
        elif subdisclaimer == 'doctor':
            bot.say("%s is not a doctor. The views/opinions/information expressed by %s is not intended or implied to be a substitute for professional medical advice, diagnosis or treatment." % (person, person))
        elif subdisclaimer == 'EULA':
            bot.say("Spicebot may occasionally (read 'frequently') use colorful language to carry out its tasks. By remaining in this channel and continuing to use the bot you acknowledge that you are not, in fact, too weak to handle this.")
        elif subdisclaimer == 'IT':
            bot.say("While most members of this channel have some level of technical knowledge, your decision to trust the recommendations of %s are entirely your own risk." % person)
        elif subdisclaimer == 'legal' or subdisclaimer == 'law':
            bot.say("Please note that %s is not a lawyer. Any and all advice given by %s is to be taken with a whole lot of salt. %s, Freenode, Spiceworks, Microsoft, Aperture Science, Black Mesa, and/or Vault-Tec™ cannot be held liable for any injuries resulting from taking aforementioned advice." % (person, person, person))
        elif subdisclaimer == 'parent':
            bot.say(person + " is not your parent. Don't expect them to deal with your shit.")
        elif subdisclaimer.startswith('porn'):
            bot.say("Remember, NOTHING is as common as porn would have you believe.")
        elif subdisclaimer.startswith('Cipher'):
            bot.say("Frivolously pestering Cipher comes with a high risk of termination, %s" % person)
        elif subdisclaimer == 'IT_Sean':
            bot.say("Should you ever encounter gases released by Sean, please be sure to inform your nearest biosafety agency of the incident.")
    else:
        bot.say("%s is not your doctor. The views/opinions/information expressed by %s is not intended or implied to be a substitute for professional medical advice, diagnosis or treatment." % (person,person))
