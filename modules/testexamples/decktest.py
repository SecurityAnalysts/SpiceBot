#!/usr/bin/env python
# coding=utf-8
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


@sopel.module.commands('decktest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'decktest')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
    myscore=0
    myhand = get_trigger_arg(bot, arg, '1+') or 'A'    
    if len(myhand)>=12:
        bot.say("Player wins for having more then 6 cards.")
    else:        
        myhand =get_trigger_arg(bot,myhand,'list')   
        bot.say("Input: "+ str(myhand))
        myscore= blackjackscore(bot,myhand)    
    bot.say(str(myscore))
    reset_botdatabase_value(bot,'casino','deckscorecount')
    

def blackjackscore(bot,hand):
    myscore = 0
    myhand= []
    for i in range(0,(len(hand))):
        card = hand[i]
        bot.say("Count: "+ str(i) + " Card: " + str(card))
        if card.isdigit():  
                                                     
            myscore=myscore+int(card)            
        elif(card == 'J' or card == 'Q' or card == 'K'):
            myscore = myscore + 10
        elif card=='A':
            myscore = myscore + 11              
    if myscore > 21:
        counter = get_botdatabase_value(bot,'casino','deckscorecount')
        if counter >2:
            return myscore
        elif 'A' in hand:
            myhand = hand.replace('A','1')
            myscore = 0
            blackjackscore(bot,myhand)
            adjust_botdatabase_value(bot, 'casino', 'deckscorecount',1)
        else:
            return myscore
    return myscore

def blackjackreset(bot,player):   
    reset_botdatabase_value(bot,player, 'myhand')
    reset_botdatabase_value(bot,player, 'dealerhand')
    reset_botdatabase_value(bot,player, 'mybet')
