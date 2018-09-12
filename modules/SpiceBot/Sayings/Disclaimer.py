# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author = dysonparkes

# Dictionary for looking up disclaimers.
# Use dictionaryname[key] to get the value from a single-layer dictionary.
# Be sure to run a .replace function on the placeholder text in the values (including the curly brackets - they're to make it easy to spot),
# To list all the options in a dictionary, call dictionaryname.keys(). To make it into a comma-separated list, use ', '.join(dictionaryname.keys()).
specific_disclaimer = {
    'brightlights': "Individuals sensitive to bright lights or with epilepsy may find the quick bright text the bot speaks with to be troublesome. Any epileptic reaction is not the fault of the bot, the channel, or its denizens.",
    'doctor': "{disclaimer_target} is not your doctor. The views/opinions/information expressed by {disclaimer_target} are not intended or implied to be a substitute for professional medical advice, diagnosis or treatment.",
    'EULA': "Spicebot may occasionally (read 'frequently') use colorful language to carry out its tasks. By remaining in this channel and continuing to use the bot you acknowledge that you are not, in fact, too weak to handle this.",
    'IT': "While most members of this channel have some level of technical knowledge, your decision to trust the recommendations of {disclaimer_target} are entirely your own risk.",
    'legal': "Please note that {disclaimer_target} is not a lawyer. Any and all advice given by {disclaimer_target} is to be taken with a whole lot of salt. {disclaimer_target}, Freenode, Spiceworks, Microsoft, Aperture Science, Black Mesa, and/or Vault-Tec™ cannot be held liable for any injuries resulting from taking aforementioned advice.",
    'law': "Please note that {disclaimer_target} is not a lawyer. Any and all advice given by {disclaimer_target} is to be taken with a whole lot of salt. {disclaimer_target}, Freenode, Spiceworks, Microsoft, Aperture Science, Black Mesa, and/or Vault-Tec™ cannot be held liable for any injuries resulting from taking aforementioned advice.",
    'parent': "{disclaimer_target} is not your parent. Don't expect them to deal with your shit.",
    'porn': "Remember, NOTHING is as common as porn would have you believe.",
    'pornhub': "Remember, NOTHING is as common as porn would have you believe.",
    'Cipher': "Frivolously pestering Cipher comes with a high risk of termination, {disclaimer_target}",
    'Cipher-0': "Frivolously pestering Cipher comes with a high risk of termination, {disclaimer_target}",
    'IT_Sean': "Should you ever encounter gases released by Sean, please be sure to inform your nearest biosafety agency of the incident.",
    'penis': "Please note that {disclaimer_target} is not a penis enlarger manufacturer. {disclaimer_target} is, however, not only their best tester but also their largest purchaser. Any views on penis enlargers given by {disclaimer_target} should be taken as if it is a Michelin Star review, as they are seen as the utmost living expert on the subject of phallic enlargement devices.",
    'penispump': "Please note that {disclaimer_target} is not a penis enlarger manufacturer. {disclaimer_target} is, however, not only their best tester but also their largest purchaser. Any views on penis enlargers given by {disclaimer_target} should be taken as if it is a Michelin Star review, as they are seen as the utmost living expert on the subject of phallic enlargement devices.",
    'prop56': "{disclaimer_target} can expose you to chemicals which are known to the State of California to cause cancer or birth defects or other reproductive harm.",
}


@sopel.module.commands('disclaimer')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'disclaimer')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Display specific disclaimers (if they exist) or a generic one if not."""
    instigator = trigger.nick
    person = spicemanip(bot, [x for x in triggerargsarray if x in botcom.users_all], 1) or instigator
    if person in triggerargsarray:
        triggerargsarray.remove(person)
    subdisclaimer = spicemanip(bot, triggerargsarray, 1) or 'doctor'

    if subdisclaimer in specific_disclaimer.keys():
        message = specific_disclaimer[subdisclaimer].replace("{disclaimer_target}", person)
    elif subdisclaimer == 'options':
        validoptions = spicemanip(bot, specific_disclaimer.keys(), 'andlist')
        message = "Current options for this module are: " + validoptions
    else:
        message = "I hate to tell you this, but either I don't have a warning for that, or something is very borked right now."

    osd(bot, trigger.sender, 'say', message)
