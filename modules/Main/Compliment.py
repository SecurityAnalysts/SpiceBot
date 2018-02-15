#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import urllib
import sys
import os
from word2number import w2n
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

compliments='https://raw.githubusercontent.com/deathbybandaid/SpiceBot/master/Text-Files/compliments.txt'
devcompliments='https://raw.githubusercontent.com/deathbybandaid/SpiceBot/dev/Text-Files/compliments.txt'
devbot='dev' ## Enables the bot to distinguish if in test

@sopel.module.commands('compliment')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

## work with /me ACTION (does not work with manual weapon)
@module.rule('^(?:feeling|feels.*(sad|upset)).*')
@module.intent('ACTION')
@module.require_chanmsg
def duel_action(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'compliment')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, triggerargsarray):
    requested = get_trigger_arg(triggerargsarray, 0)
    myline = ''
    if not bot.nick.endswith(devbot):
        filetocheck=compliments #Master branch
    else:
        filetocheck=devcompliments #Dev branch
    if not requested:
        myline = randomcompliment(filetocheck)
    else:
        requested.lstrip("-")        
        if (requested == '0' or requested.lower() == 'zero'):
            myline = 'That doesnt appear to be a compliment number.'
        elif requested == 'random':
             myline = randomcompliment(filetocheck)
        else:
            htmlfile=urllib.urlopen(filetocheck)
            lines=htmlfile.readlines() 
            numberoflines = len(lines)
           
            if requested.isdigit():
                complimentnumber = int(requested)
                if complimentnumber > numberoflines:
                    myline ="Please select a compliment number between 1 and " + str(numberoflines) + ""
                else:
                    myline = get_trigger_arg(lines, complimentnumber)
            else:
                try:
                    complimentnumber = w2n.word_to_num(str(requested))
                    myline = get_trigger_arg(lines, complimentnumber)   
                except ValueError:
                    myline = 'That doesnt appear to be a compliment number.'
    if not myline or myline == '\n':
        myline = 'There is no compliment tied to this number.'
    bot.say(myline)
       
# random compliment
def randomcompliment(filetocheck):
    htmlfile=urllib.urlopen(filetocheck)
    lines=htmlfile.read().splitlines()
    myline=random.choice(lines)
    if not myline or myline == '\n':
        myline = randomcompliment(filetocheck)
    return myline
