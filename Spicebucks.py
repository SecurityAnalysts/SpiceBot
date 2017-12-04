import sopel.module
import datetime
from sopel import module, tools
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

## All commands will use .spicebucks [action]
## Actions to include
### payday - Recieve a once a day payday amount (current Thought is 5 / day)
### bank - Check amount in bank
### transfer - Transfer money from one user to another

#db, channel= current channel, 

@sopel.module.commands('spicebucks')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    for c in bot.channels:
        channel = c
    commandused = trigger.group(3)
    inchannel = trigger.sender
    if commandused:
        if commandused.startswith('payday'):
            checkpayday(bot,trigger.nick)
        elif commandused.startswith('reset'): ##to be removed
            reset(bot,trigger.nick)
        elif commandused.startswith('bank'):
            bank(bot, trigger.nick)
        elif commandused.startswith('transfer'):
            bot.say('transfer money to another user')
            
##### Lots to do
def reset(bot, target): ##### to be removed, verify payday
    bot.db.set_nick_value(target, 'spicebucks_payday', 0)

def checkpayday(bot, target):
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    lastpayday = bot.db.get_nick_value(target, 'spicebucks_payday') or 0
    if lastpayday == 0 or lastpayday < datetoday:
        bot.db.set_nick_value(target, 'spicebucks_payday', datetoday)
        spicebucks(bot, target, 'plus', 5)
        bot.say("You haven't been paid yet today. Here's your 5 Spicebucks.") #change to notify
    elif lastpayday == datetoday:
        bot.say("You've already been paid today. Now go do some work.")
        
def spicebucks(bot, target, plusminus, amount):
    if type(amount) == int:
        inbank = bot.db.get_nick_value(target, 'spicebucks_bank') or 0
        if plusminus == 'plus':
            bot.db.set_nick_value(target, inbank + amount)
        elif plusminus == 'minus':
            bot.db.set_nick_value(target, inbank - amount)
    else:
        bot.notify("The amount you entered does not appear to be a number.  Transaction failed.")

def bank(bot, nick):
    spicebucks = bot.db.get_nick_value(nick, 'spicebucks_bank') or 0
    bot.say("You have " + str(spicebucks) + " in the bank.")


