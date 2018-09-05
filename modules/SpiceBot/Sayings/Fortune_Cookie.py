import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

defaultoptions = [
    "A conclusion is simply the place where you got tired of thinking.", "A foolish man listens to his heart. A wise man listens to cookies.", "All fortunes are wrong except this one.",
    "Ask your mom instead of a cookie.", "Avoid taking unnecessary gambles. Lucky numbers: 12, 15, 23, 28, 37", "Change is inevitable, except for vending machines.", "Do not mistake temptation for opportunity.",
    "Don't eat the paper.", "Fortune not found? Abort, Retry, Ignore.", "Hard work pays off in the future. Laziness pays off now.", "He who laughs at himself never runs out of things to laugh at.",
    "He who laughs last is laughing at you.", "He who throws dirt is losing ground. ", "Help! I am being held prisoner in a fortune cookie factory.", "It is a good day to have a good day.",
    "It's about time I got out of that cookie.", "Never forget a friend. Especially if he owes you.", "Never trust a fart.", "No snowflake feels responsible in an avalanche.", "The fortune you seek is in another cookie.",
    "This cookie contains 117 calories.", "We don't know the future, but here's a cookie.", "You are not illiterate.", "You can always find happiness at work on Friday.", "You have rice in your teeth.",
    "You think it's a secret, but they know.", "You will be hungry again in one hour.", "Your friends mom is not covered by the Bro code."]


@sopel.module.commands('fortune', 'cookie')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'fortune')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Retrieve a cookie from the database."""
    databasekey = "fortunecookie"
    command = get_trigger_arg(bot, triggerargsarray, 1) or 'get'
    if not sayingscheck(bot, databasekey) and command != "add":
        sayingsmodule(bot, databasekey, defaultoptions, 'initialise')
    message = sayingsmodule(bot, databasekey, triggerargsarray, command)
    osd(bot, trigger.sender, 'say', message)
