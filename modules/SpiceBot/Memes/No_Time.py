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
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    notimefor = get_trigger_arg(bot, triggerargsarray, 0) or "that"
    message = "Well I woke up to get me a cold pop and then I thought somebody was barbequing. I said oh lord Jesus it's a fire. Then I ran out, I didn't grab no shoes or nothin' Jesus, I ran for my life. And then the smoke got me, I got bronchitis ain't nobody got time for " + str(notimefor) + "."
    osd(bot, trigger.sender, 'say', message)
