import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('notime')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'notime')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    notimefor = spicemanip(bot, triggerargsarray, 0) or "that"
    message = "Well I woke up to get me a cold pop and then I thought somebody was barbequing. I said oh lord Jesus it's a fire. Then I ran out, I didn't grab no shoes or nothin' Jesus, I ran for my life. And then the smoke got me, I got bronchitis ain't nobody got time for " + str(notimefor) + "."
    osd(bot, trigger.sender, 'say', message)
