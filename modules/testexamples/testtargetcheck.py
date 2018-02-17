##to be added to spicebot shared after testing
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
import Spicebucks
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('testtarget')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    istarget = 0
    istarget,targetmsg =targetcheck(bot,get_trigger_arg(triggerargsarray, 1),trigger.nick)
    if istarget ==1:
        bot.say("Target is valid")  
    else:
        bot.say(str(istarget) + " " +targetmsg)
##copy below this line into spicbotshared when it is working##

####################################
##########Check for target##########
###If target  validtarget =1       #
###if bot is target validtarget=2  #
###if target is instigator         #
###validtarget =2                  #
####################################
def testtargetcheck(bot, target,instigator):
    validtarget = 0
    validtargetmsg = ''
    botusersarray=[]
    botuseron=[]
    for channel in bot.channels:
        botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers')    
    for u in bot.users:
        if u in botusersarray:
            botuseron.append(u)   
    if not target:
        validtargetmsg = str(instigator + ", you must specify a target.")
        validtarget = 0
    else:
        if target.lower() == (bot.nick).lower():
            validtargetmsg = str(instigator + ", can't targetbot.")
            validtarget=2  
        elif target == instigator:       
            validtargetmsg = str(instigator + ", is the target")
            validtarget=3         
            
        elif not target.lower() in [u.lower() for u in botuseron]:
            validtargetmsg = str(instigator + " " + target +  "isn't a valid target")            
        else:
            validtarget = 1
    
    return validtarget, validtargetmsg
