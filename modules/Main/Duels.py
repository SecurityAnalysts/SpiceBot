#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel.module import OP
from sopel.module import ADMIN
from sopel.module import VOICE
import sopel
from sopel import module, tools
import random
from random import randint
import time
import datetime
import re
import sys
import os
from os.path import exists
from num2words import num2words

## not needed if using without spicebot
shareddir = os.path.dirname(os.path.dirname(__file__)) ## not needed if using without spicebot
sys.path.append(shareddir) ## not needed if using without spicebot
from SpicebotShared import * ## not needed if using without spicebot

###################
## Configurables ##
###################

## Timeouts
USERTIMEOUT = 180 ## Time between a users ability to duel - 3 minutes
ROULETTETIMEOUT = 8
CHANTIMEOUT = 40 ## Time between duels in a channel - 40 seconds
OPTTIMEOUT = 1800 ## Time between opting in and out of the game - Half hour
ASSAULTTIMEOUT = 1800 ## Time Between Full Channel Assaults
COLOSSEUMTIMEOUT = 1800 ## Time Between colosseum events
CLASSTIMEOUT = 86400 ## Time between changing class - One Day
INSTIGATORTIMEOUT = 1800
timepotiontargetarray = ['lastinstigator','lastfullroomcolosseuminstigator','lastfullroomassultinstigator']
timepotiontimeoutarray = ['timeout','lastfullroomcolosseum','lastfullroomassult','opttime','classtimeout']
AUTOLOGOUT = 259200

## Half hour timer
scavengercoinaward = 15 ## coin gain per half hour for scavengers
magemanaregen = 50 ## mages regenerate mana: rate
magemanaregenmax = 500 ## mages regenerate mana: limit
healthregen = 50 ## health regen rate
healthregenmax = 500 ## health regen limit

## Potion Potency
healthpotionworthbarbarian = 125 ## health potion worth for barbarians
healthpotionworth = 100 ## normal health potion worth
poisonpotionworth = -50 ## poisonpotion damage
manapotionworthmage = 125 ## manapotion worth for mages
manapotionworth = 100 ##normal mana potion worth

## Buy/sell/trade rates
traderatioscavenger = 2 ## scavengers can trade at a 2:1 ratio
traderatio = 3 ## normal trading ratio 3:1
lootbuycostscavenger = 80 ## cost to buy a loot item for scavengers
lootbuycost = 100 ## normal cost to buy a loot item
lootsellrewardscavenger = 40 ## coin rewarded in selling loot for scavengers
lootsellreward = 25 ## normal coin rewarded in selling loot
changeclasscost = 100 ## ## how many coin to change class

## Magic usage
magemanamagiccut = .9 ## mages only need 90% of the mana requirements below
manarequiredmagicattack = 250 ## mana required for magic attack
magicattackdamage = -200 ## damage caused by a magic attack
manarequiredmagicshield = 300 ## mana required for magic shield
magicshielddamage = 80 ## damage caused by a magic shield usage
shieldduration = 200 ## how long a shield lasts
manarequiredmagiccurse = 500 ## mana required for magic curse
magiccursedamage = -80 ## damage caused by a magic curse
curseduration = 4 ## how long a curse lasts

## XP points awarded
XPearnedwinnerranger = 20 ## xp earned as a winner and ranger
XPearnedloserranger = 15 ## xp earned as a loser and ranger
XPearnedwinnerstock = 15 ## default xp earned as a winner
XPearnedloserstock = 10 ## default xp earned as a loser

## Class advantages
scavegerfindpercent = 60 ## scavengers have a higher percent chance of finding loot
barbarianminimumdamge = 60 ## Barbarians always strike a set value or above
vampiremaximumdamge = 50

## Armor
armormaxdurability = 10
armormaxdurabilityblacksmith = 15
armorhitpercentage = 33 ## has to be converted to decimal later
armorcost = 500
armorchest = 'breastplate'
armorarm = 'gauntlets'
armorhead = 'helmet'
armorleg = 'greaves'

## Bot
botdamage = 150 ## The bot deals a set damage
duelrecorduser = 'duelrecorduser' ## just a database column to store values in
devbot = 'dev' ## If using a development bot and want to bypass commands, this is what the bots name ends in

## other
bugbountycoinaward = 100 ## users that find a bug in the code, get a reward
defaultadjust = 1 ## The default number to increase a stat
GITWIKIURL = "https://github.com/deathbybandaid/SpiceBot/wiki/Duels" ## Wiki URL, change if not using with spicebot
grenadefull = 100
grenadesec = 50
weaponmaxlength = 70
randomcoinaward = 100
speceventreward = 500
stockhealth = 1000

## Tiers
stocktierratio = 1
tierratioone = 1.1
tierratiotwo = 1.2
tierratiothree = 1.3
tierratiofour = 1.4
tierratiofive = 1.5
tierratiosix = 1.6
tierratioseven = 1.7
tierratioeight = 1.8
tierrationine = 1.9
tierratioten = 2
tierratioeleven = 2.1
tierratiotwelve = 2.2
tierratiothirteen = 2.3
tierratiofourteen = 2.4
tierratiofifteen = 2.5
tiercommandarray = ['harakiri','tier','bounty','armor','title','docs','admin','author','on','off','usage','stats','loot','streaks','leaderboard','warroom','weaponslocker','class','magic','random','roulette','assault','colosseum','upupdowndownleftrightleftrightba']
tierunlocktier, tierunlockdocs, tierunlockadmin, tierunlockauthor, tierunlockon, tierunlockoff, tierunlockusage, tierunlockupupdowndownleftrightleftrightba = 1,1,1,1,1,1,1,1
tierunlockstreaks, tierunlockbounty, tierunlockharakiri = 2,2,2
tierunlockweaponslocker, tierunlockclass, tierunlockmagic = 3,3,3
tierunlockleaderboard, tierunlockwarroom = 4,4
tierunlockstats, tierunlockloot,tierunlockrandom = 5,5,5
tierunlockroulette, tierunlockarmor = 6,6
tierunlockassault = 7
tierunlockcolosseum = 8
tierunlocktitle = 9
peppertierarray = ['pimiento','sonora','anaheim','poblano','jalapeno','serrano','chipotle','tabasco','cayenne','thai pepper','datil','habanero','ghost chili','mace','pure capsaicin']

## Potion Display Message
healthpotiondispmsg = str(": worth " + str(healthpotionworth) + " health.")
poisonpotiondispmsg = str(": worth " + str(poisonpotionworth) + " health.")
manapotiondispmsg = str(": worth " + str(manapotionworth) + " mana.")
timepotiondispmsg = str(": Removes multiple timeouts.")
mysterypotiondispmsg = str(": The label fell off. Use at your own risk!")
magicpotiondispmsg = str(": Not consumable, sellable, or purchasable. Trade this for the potion you want!")

############
## Arrays ##
############

botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score'] ## people to recognize
lootitemsarray = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion','magicpotion'] ## types of potions
backpackarray = ['coin','grenade','healthpotion','manapotion','poisonpotion','timepotion','mysterypotion','magicpotion'] ## how to organize backpack
duelstatsarray = ['class','health','curse','shield','mana','xp','wins','losses','winlossratio','respawns','kills','lastfought','timeout','bounty']
statsbypassarray = ['winlossratio','timeout'] ## stats that use their own functions to get a value
transactiontypesarray = ['buy','sell','trade','use'] ## valid commands for loot
classarray = ['blacksmith','barbarian','mage','scavenger','rogue','ranger','fiend','vampire','knight','paladin'] ## Valid Classes
duelstatsadminarray = ['helmet','gauntlets','breastplate','greaves','bounty','levelingtier','weaponslocker','currentlosestreak','magicpotion','currentwinstreak','currentstreaktype','classfreebie','grenade','shield','classtimeout','class','curse','bestwinstreak','worstlosestreak','opttime','coin','wins','losses','health','mana','healthpotion','mysterypotion','timepotion','respawns','xp','kills','timeout','poisonpotion','manapotion','lastfought','konami'] ## admin settings
statsadminchangearray = ['set','reset'] ## valid admin subcommands
magicoptionsarray = ['curse','shield']
nulllootitemsarray = ['water','vinegar','mud']
duelhittypesarray = ['hits','strikes','beats','pummels','bashes','smacks','knocks','bonks','chastises','clashes','clobbers','slugs','socks','swats','thumps','wallops','whops']
duelbodypartsarray = ['chest','arm','leg','head']
armortypesarray = ['helmet','gauntlets','breastplate','greaves']

################################################################################
## Main Operation #### Main Operation #### Main Operation #### Main Operation ##
################################################################################

## work with /me ACTION (does not work with manual weapon)
@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
@module.intent('ACTION')
@module.require_chanmsg
def duel_action(bot, trigger):
    #triggerargsarray = get_trigger_arg(trigger.group(1), 'create') # enable if not using with spicebot
    #execute_main(bot, trigger, triggerargsarray) # enable if not using with spicebot
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'duel') ## not needed if using without spicebot
    if not enablestatus: ## not needed if using without spicebot
        execute_mainactual(bot, trigger, triggerargsarray) ## not needed if using without spicebot

## Base command
@sopel.module.commands('duel','challenge')
def mainfunction(bot, trigger):
    #triggerargsarray = get_trigger_arg(trigger.group(2), 'create') # enable if not using with spicebot
    #execute_main(bot, trigger, triggerargsarray) # enable if not using with spicebot
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'duel') ## not needed if using without spicebot
    if not enablestatus: ## not needed if using without spicebot
        execute_main(bot, trigger, triggerargsarray) ## not needed if using without spicebot

## The Command Process
def execute_main(bot, trigger, triggerargsarray):
    fullcommandusedtotal = get_trigger_arg(triggerargsarray, 0)
    fullcomsplit = fullcommandusedtotal.split("&&")
    for comsplit in fullcomsplit:
        triggerargsarray = get_trigger_arg(comsplit, 'create')
        execute_main(bot, trigger, triggerargsarray)
                    
def execute_mainactual(bot, trigger, triggerargsarray):
    
    ## Initial ARGS of importance
    fullcommandused = get_trigger_arg(triggerargsarray, 0)
    commandortarget = get_trigger_arg(triggerargsarray, 1)
    dowedisplay = 0
    displaymessage = ''
    typeofduel = 'target'
    
    ## User/channel Arrays
    dueloptedinarray = get_database_value(bot, bot.nick, 'duelusers') or []
    canduelarray, targetarray = [], []

    ## Time when Module use started
    now = time.time()

    ## Channel
    inchannel = trigger.sender

    ## bot does not need stats or backpack items
    refreshbot(bot)

    ## Instigator
    instigator = trigger.nick
    
    ## Instigator can't be a command, and can't enable duels
    if instigator.lower() in tiercommandarray:
        bot.notice("It looks like your nick is unable to play duels.",instigator)
        return
    
    ## Instigator last used
    set_database_value(bot, instigator, 'lastcommand', now)
    
    ## Alternative commands
    if commandortarget == 'enable':
        commandortarget = 'on'
    elif commandortarget == 'disable':
        commandortarget = 'off'
    elif commandortarget == 'anyone' or commandortarget == 'somebody' or commandortarget == 'available':
        commandortarget = 'random'
    elif commandortarget == 'everyone':
        commandortarget = 'assault'
    elif commandortarget == 'help':
        commandortarget = 'docs'
    
    ## If Not a target or a command used
    if not fullcommandused:
        bot.notice(instigator + ", Who do you want to duel? Online Docs: " + GITWIKIURL, instigator)

    ## Commands cannot be run if opted out
    elif instigator not in dueloptedinarray and commandortarget.lower() != 'on' and commandortarget.lower() != 'enable' and commandortarget.lower() != 'admin' :
        bot.notice(instigator + ", It looks like you have duels disabled. Run .duel on/enable to enable.", instigator)

    ## Instigator versus Bot
    elif commandortarget == bot.nick:
        bot.say("I refuse to fight a biological entity!")

    ## Instigator versus Instigator
    elif commandortarget == instigator:
        bot.say("If you are feeling self-destructive, there are places you can call.")

    ## Determine if the arg after .duel is a target or a command
    elif commandortarget.lower() in tiercommandarray:
        commandortarget = commandortarget.lower()

        ## Tier unlocks
        tiercommandeval = eval("tierunlock"+ commandortarget) or 0
        tiercommandeval = int(tiercommandeval)
        tierpepperrequired = get_tierpepper(bot, tiercommandeval)
        currenttier = get_database_value(bot, duelrecorduser, 'levelingtier') or 0
        tiermath = int(tiercommandeval) - int(currenttier)
        if int(tiercommandeval) > int(currenttier) and commandortarget != 'admin' and commandortarget != 'on':
            if commandortarget != 'stats' and commandortarget != 'loot':
                bot.say("Duel "+commandortarget+" will be unlocked when somebody reaches " + str(tierpepperrequired) + ". "+str(tiermath) + " tier(s) remaining!")
                if not bot.nick.endswith(devbot):
                    return

        ## usage counter
        adjust_database_value(bot, instigator, 'usage', 1)
        
        ## Stat check
        statreset(bot, instigator)
        healthcheck(bot, instigator)
        
        ## Docs
        if commandortarget == 'docs':
            target = get_trigger_arg(triggerargsarray, 2)
            if not target:
                bot.say("Online Docs: " + GITWIKIURL)
            elif target.lower() not in [u.lower() for u in bot.users]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            else:
                if target.lower() in tiercommandarray:
                    bot.notice("It looks like that nick is unable to play duels.",instigator)
                    return
                bot.notice("Online Docs: " + GITWIKIURL, target)

        ## Author
        elif commandortarget == 'author':
            bot.notice("The author of Duels is deathbybandaid.", instigator)
        
        ## On/off
        elif commandortarget == 'on' or commandortarget == 'off':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            targetopttime = get_timesince_duels(bot, target, 'opttime')
            if target.lower() not in [u.lower() for u in bot.users] and target != 'everyone':
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target != instigator and not trigger.admin:
                bot.notice(instigator + "This is an admin only function.", instigator)
            elif target == 'everyone':
                for u in bot.users:
                    if commandortarget == 'on':
                        adjust_database_array(bot, bot.nick, target, 'duelusers', 'add')
                    else:
                        adjust_database_array(bot, bot.nick, target, 'duelusers', 'del')
                bot.notice(instigator + ", duels should now be " +  commandortarget + ' for ' + target + '.', instigator)
            elif targetopttime < OPTTIMEOUT and not trigger.admin and not bot.nick.endswith(devbot):
                target = actualname(bot, target)
                bot.notice(instigator + " It looks like " + target + " can't enable/disable duels for " + str(hours_minutes_seconds((OPTTIMEOUT - targetopttime))), instigator)
            elif commandortarget == 'on' and target.lower() in [x.lower() for x in dueloptedinarray]:
                target = actualname(bot, target)
                bot.notice(instigator + ", It looks like " + target + " already has duels on.", instigator)
            elif commandortarget == 'off' and target.lower() not in [x.lower() for x in dueloptedinarray]:
                target = actualname(bot, target)
                bot.notice(instigator + ", It looks like " + target + " already has duels off.", instigator)
            else:
                if target.lower() in tiercommandarray:
                    bot.notice("It looks like that nick is unable to play duels.",instigator)
                    return
                target = actualname(bot, target)
                if commandortarget == 'on':
                    adjust_database_array(bot, bot.nick, target, 'duelusers', 'add')
                else:
                    adjust_database_array(bot, bot.nick, target, 'duelusers', 'del')
                set_database_value(bot, target, 'opttime', now)
                bot.notice(instigator + ", duels should now be " +  commandortarget + ' for ' + target + '.', instigator)

        ## Tier
        elif commandortarget == 'tier':
            command = get_trigger_arg(triggerargsarray, "2+")
            if not command:
                dispmsg = str("The current tier is " + str(currenttier)+ ". ")
                currenttierlistarray = []
                futuretierlistarray = []
                for x in tiercommandarray:
                    tiereval = eval("tierunlock"+x)
                    if tiereval <= currenttier and x != 'upupdowndownleftrightleftrightba':
                        currenttierlistarray.append(x)
                    elif tiereval > currenttier and x != 'upupdowndownleftrightleftrightba':
                        futuretierlistarray.append(x)
                if currenttierlistarray != []:
                    currenttierlist = get_trigger_arg(currenttierlistarray, "list")
                    dispmsg = str(dispmsg + " Feature(s) currently available: " + currenttierlist + ". ")
                if futuretierlistarray != []:
                    futuretierlist = get_trigger_arg(futuretierlistarray, "list")
                    dispmsg = str(dispmsg + " Feature(s) not yet unlocked: " + futuretierlist + ". ")
                bot.say(dispmsg)
            elif command.lower() in peppertierarray:
                dispmsg = str("The current tier is " + str(currenttier)+ ". ")
                pepperconvert = get_peppertier(bot,command)
                pickarray = []
                for x in tiercommandarray:
                    tiereval = eval("tierunlock"+x)
                    if tiereval == int(pepperconvert) and x != 'upupdowndownleftrightleftrightba':
                        pickarray.append(x)
                if pickarray != []:
                    tierlist = get_trigger_arg(pickarray, "list")
                    dispmsg =  str(dispmsg + " Feature(s) that are available at tier "+ str(pepperconvert) +": " + tierlist + ". ")
                    tiermath = int(pepperconvert) - currenttier
                    if tiermath > 0:
                        dispmsg = str(dispmsg + str(tiermath) + " tiers to go!")
                bot.say(dispmsg)
            elif command.isdigit():
                dispmsg = str("The current tier is " + str(currenttier)+ ". ")
                pickarray = []
                for x in tiercommandarray:
                    tiereval = eval("tierunlock"+x)
                    if tiereval == int(command) and x != 'upupdowndownleftrightleftrightba':
                        pickarray.append(x)
                if pickarray != []:
                    tierlist = get_trigger_arg(pickarray, "list")
                    dispmsg =  str(dispmsg + " Feature(s) that are available at tier "+ str(command) +": " + tierlist + ". ")
                    tiermath = int(command) - currenttier
                    if tiermath > 0:
                        dispmsg = str(dispmsg + str(tiermath) + " tiers to go!")
                else:
                    dispmsg = str(dispmsg + " No unlocks at tier " + str(command)+ ". ")
                bot.say(dispmsg)
            elif command.lower() not in tiercommandarray or command.lower() == 'upupdowndownleftrightleftrightba':
                bot.notice(instigator + ", that appears to be an invalid command.", instigator)
            else:
                dispmsg = str("The current tier is " + str(currenttier)+ ". ")
                tiereval = eval("tierunlock"+command)
                tiereval = int(tiereval)
                tierpepperrequired = get_tierpepper(bot, tiereval)
                tiermath = tiereval - currenttier
                if tiereval <= currenttier:
                    dispmsg = str(dispmsg+ command+ " is available as of tier " + str(tiereval)+ " "+str(tierpepperrequired)+". ")
                else:
                    dispmsg = str(dispmsg+ command +" will be unlocked when somebody reaches " + str(tierpepperrequired) + ". "+str(tiermath) + " tier(s) remaining!")
                bot.say(dispmsg)
                
        ## Suicide
        elif commandortarget == 'harakiri':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target != instigator and target != 'confirm':
                bot.say("You can't suicide other people. It's called Murder.")
            elif target == instigator:
                bot.say("You must run this command with 'confirm' to kill yourself. No rewards are given in to cowards.")
            else:
                deathmsgb = suicidekill(bot,instigator)
                bot.say(deathmsgb)

        ## Russian Roulette
        elif commandortarget == 'roulette':
            if not inchannel.startswith("#"):
                bot.notice(instigator + " Duels must be in channel.", instigator)
                return
            getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + commandortarget)) or ROULETTETIMEOUT
            if getlastusage < ROULETTETIMEOUT and not bot.nick.endswith(devbot):
                bot.notice(instigator + " Roulette has a small timeout.", instigator)
                return
            set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
            roulettepayoutdefault = 5
            roulettelastplayer = get_database_value(bot, duelrecorduser, 'roulettelastplayer') or bot.nick
            roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1
            if roulettelastplayer == instigator:
                bot.say(instigator + " spins the revolver and pulls the trigger.")
            elif roulettecount == 1:
                bot.say(instigator + " reloads the revolver, spins the cylinder and pulls the trigger.")
            else:
                bot.say(instigator + " spins the cylinder and pulls the trigger.")
            roulettechamber = get_database_value(bot, duelrecorduser, 'roulettechamber')
            if not roulettechamber:
                roulettechamber = randint(1, 6)
                set_database_value(bot, duelrecorduser, 'roulettechamber', roulettechamber)
            roulettespinarray = get_database_value(bot, duelrecorduser, 'roulettespinarray') or [1,2,3,4,5,6]
            if roulettelastplayer == instigator:
                if len(roulettespinarray) > 1:
                    temparray = []
                    for x in roulettespinarray:
                        if x != roulettechamber:
                            temparray.append(x)
                    randomremove = get_trigger_arg(temparray, "random")
                    roulettespinarray.remove(randomremove)
                    currentspin = get_trigger_arg(roulettespinarray, "random")
                    set_database_value(bot, duelrecorduser, 'roulettespinarray', roulettespinarray)
                else:
                    currentspin = roulettechamber
                    reset_database_value(bot, duelrecorduser, 'roulettespinarray')
            else:
                reset_database_value(bot, duelrecorduser, 'roulettespinarray')
            currentspin = get_trigger_arg(roulettespinarray, "random")
            if currentspin == roulettechamber:
                biggestpayout = 0
                biggestpayoutwinner = ''
                statreset(bot, instigator)
                healthcheck(bot, instigator)
                roulettewinners = get_database_value(bot, duelrecorduser, 'roulettewinners') or []
                resultmsg = ''
                deathmsg = ''
                revolvernames = ['.357 Magnum','Colt PeaceMaker','Colt Repeater','Colt Single Action Army 45','Ruger Super Blackhawk','Remington Model 1875','Russian Nagant M1895 revolver','Smith and Wesson Model 27']
                weapon = get_trigger_arg(revolvernames, 'random')
                weapon = str(" with a " + weapon)
                winner, loser = 'duelsroulettegame', instigator
                damage, roulettedamagearray = damagedone(bot, winner, loser, weapon, 1)
                roulettedamage = ''
                for x in roulettedamagearray:
                    roulettedamage = str(roulettedamage+" "+ x)
                currenthealth = get_database_value(bot, loser, 'health')
                if currenthealth <= 0:
                    deathmsg = str(" " +  loser + ' dies forcing a respawn!!')
                    deathmsgb = suicidekill(bot,loser)
                    deathmsg = str(deathmsg+" "+deathmsgb)
                if roulettecount == 1:
                    resultmsg = "First in the chamber. What bad luck. "
                    roulettewinners.append(instigator)
                resultmsg = str(resultmsg + roulettedamage + deathmsg)
                uniqueplayersarray = []
                for x in roulettewinners:
                    if x not in uniqueplayersarray:
                        uniqueplayersarray.append(x)
                for x in uniqueplayersarray:
                    if x != instigator:
                        statreset(bot, x)
                        healthcheck(bot, x)
                        roulettepayoutx = get_database_value(bot, x, 'roulettepayout')
                        if roulettepayoutx > biggestpayout:
                            biggestpayoutwinner = x
                            biggestpayout = roulettepayoutx
                        elif roulettepayoutx == biggestpayout:
                            biggestpayoutwinner = str(biggestpayoutwinner+ " " + x)
                            biggestpayout = roulettepayoutx
                        adjust_database_value(bot, x, 'coin', roulettepayoutx)
                        bot.notice(x + ", your roulette payouts = " + str(roulettepayoutx) + " coins!", x)
                    reset_database_value(bot, x, 'roulettepayout')
                if instigator in roulettewinners:
                    roulettewinners.remove(instigator)
                if roulettewinners != []:
                    displaymessage = get_trigger_arg(roulettewinners, "list")
                    displaymessage = str("Winners: " + displaymessage + " ")
                if biggestpayoutwinner != '':
                    displaymessage = str(displaymessage +"     Biggest Payout: "+ biggestpayoutwinner + " with " + str(biggestpayout) + " coins. ")
                reset_database_value(bot, duelrecorduser, 'roulettelastplayer')
                reset_database_value(bot, duelrecorduser, 'roulettechamber')
                reset_database_value(bot, duelrecorduser, 'roulettewinners')
                roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1
                reset_database_value(bot, duelrecorduser, 'roulettecount')
                reset_database_value(bot, instigator, 'roulettepayout')
                if roulettecount > 1:
                    roulettecount = roulettecount + 1
                    displaymessage = str(displaymessage +"     The chamber spun " + str(roulettecount) + " times. ")
                bot.say(resultmsg + displaymessage)
            else:
                time.sleep(2) # added to build suspense
                bot.say("*click*")
                roulettecount = roulettecount + 1
                roulettepayout = roulettepayoutdefault * roulettecount
                adjust_database_value(bot, instigator, 'roulettepayout', roulettepayout)
                adjust_database_value(bot, duelrecorduser, 'roulettecount', defaultadjust)
                set_database_value(bot, duelrecorduser, 'roulettelastplayer', instigator)
                adjust_database_array(bot, duelrecorduser, instigator, 'roulettewinners', 'add')

        ## Usage
        elif commandortarget == 'usage':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            targetname = target
            if target == 'channel':
                target = duelrecorduser
            totaluses = get_database_value(bot, target, 'usage')
            if target.lower() in tiercommandarray:
                bot.notice("It looks like that nick is unable to play duels.",instigator)
                return
            targetname = actualname(bot, targetname)
            bot.say(targetname + " has used duels " + str(totaluses) + " times.")
            
        ## Colosseum, Assault, and Random
        elif commandortarget == 'colosseum' or commandortarget == 'assault' or commandortarget == 'random':
            if not inchannel.startswith("#"):
                bot.notice(instigator + " Duels must be in channel.", instigator)
                return
            for u in bot.users:
                canduel = mustpassthesetoduel(bot, trigger, u, u, dowedisplay)
                if canduel:
                    canduelarray.append(u)
            if commandortarget != 'random' and bot.nick in canduelarray:
                canduelarray.remove(bot.nick)
            if canduelarray == [] or len(canduelarray) == 1:
                bot.notice(instigator + ", It looks like the full channel " + commandortarget + " event target finder has failed.", instigator)
                return
            if commandortarget == 'random':
                typeofduel == 'random'
                target = get_trigger_arg(canduelarray, 'random')
                OSDTYPE = 'say'
                targetarray.append(target)
                getreadytorumble(bot, trigger, instigator, targetarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, inchannel)
                return
            timeouteval = eval(commandortarget.upper() + "TIMEOUT")
            getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + commandortarget)) or timeouteval
            getlastinstigator = get_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator')) or bot.nick
            if getlastusage < timeouteval and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", full channel " + commandortarget + " event can't be used for "+str(hours_minutes_seconds((timeouteval - getlastusage)))+".", instigator)
            elif getlastinstigator == instigator and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", You may not instigate a full channel " + commandortarget + " event twice in a row.", instigator)
            elif instigator not in canduelarray:
                dowedisplay = 1
                mustpassthesetoduel(bot, trigger, instigator, instigator, dowedisplay)
            else:
                if instigator in canduelarray and commandortarget == 'assault':
                    canduelarray.remove(instigator)
                displaymessage = get_trigger_arg(canduelarray, "list")
                bot.say(instigator + " Initiated a full channel " + commandortarget + " event. Good luck to " + displaymessage)
                set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
                set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator'), instigator)
                if commandortarget == 'assault':
                    OSDTYPE = 'notice'
                    lastfoughtstart = get_database_value(bot, instigator, 'lastfought')
                    typeofduel = 'assault'
                    getreadytorumble(bot, trigger, instigator, canduelarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, inchannel)
                    set_database_value(bot, instigator, 'lastfought', lastfoughtstart)
                elif commandortarget == 'colosseum':
                    statreset(bot, instigator)
                    healthcheck(bot, instigator)
                    totalplayers = len(canduelarray)
                    riskcoins = int(totalplayers) * 30
                    damage = riskcoins
                    winner = selectwinner(bot, canduelarray)
                    bot.say("The Winner is: " + winner + "! Total winnings: " + str(riskcoins) + " coin! Losers took " + str(riskcoins) + " damage.")
                    diedinbattle = []
                    canduelarray.remove(winner)
                    deathmsgb = ''
                    for x in canduelarray:
                        statreset(bot, x)
                        healthcheck(bot, x)
                        shieldloser = get_database_value(bot, x, 'shield') or 0
                        if shieldloser and damage > 0:
                            damagemath = int(shieldloser) - damage
                            if int(damagemath) > 0:
                                adjust_database_value(bot, x, 'shield', -abs(damage))
                                damage = 0
                            else:
                                damage = abs(damagemath)
                                reset_database_value(bot, x, 'shield')
                        if damage > 0:
                            adjust_database_value(bot, x, 'health', -abs(damage))
                            currenthealth = get_database_value(bot, x, 'health')
                        if currenthealth <= 0:
                            deathmsgb = whokilledwhom(bot, winner, x) or ''
                            diedinbattle.append(x)
                    displaymessage = get_trigger_arg(diedinbattle, "list")
                    if displaymessage:
                        bot.say(displaymessage + " died in this event." + " "+ deathmsgb)
                    adjust_database_value(bot, winner, 'coin', riskcoins)

        ## War Room
        elif commandortarget == 'warroom':
            subcommand = get_trigger_arg(triggerargsarray, 2).lower()
            for u in bot.users:
                canduel = mustpassthesetoduel(bot, trigger, u, u, dowedisplay)
                if canduel and u != bot.nick:
                    canduelarray.append(u)
            if not subcommand:
                if instigator in canduelarray:
                    bot.notice(instigator + ", It looks like you can duel.", instigator)
                else:
                    dowedisplay = 1
                    mustpassthesetoduel(bot, trigger, instigator, instigator, dowedisplay)
            elif subcommand == 'colosseum' or subcommand == 'assault':
                if subcommand == 'everyone':
                    subcommand = 'assault'
                timeouteval = eval(subcommand.upper() + "TIMEOUT")
                getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + subcommand)) or timeouteval
                getlastinstigator = get_database_value(bot, duelrecorduser, str('lastfullroom' + subcommand + 'instigator')) or bot.nick
                if getlastinstigator == instigator and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", You may not instigate a full channel " + subcommand + " event twice in a row.", instigator)
                elif getlastusage < timeouteval and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", full channel " + subcommand + " event can't be used for "+str(hours_minutes_seconds((timeouteval - getlastusage)))+".", instigator)
                else:
                    bot.notice(instigator + ", It looks like full channel " + subcommand + " event can be used.", instigator)
            elif subcommand == 'list':
                if instigator in canduelarray:
                    canduelarray.remove(instigator)
                displaymessage = get_trigger_arg(canduelarray, "list")
                bot.say(instigator + ", you may duel the following users: "+ str(displaymessage ))
            elif subcommand.lower() not in [u.lower() for u in bot.users]:
                bot.notice(instigator + ", It looks like " + str(subcommand) + " is either not here, or not a valid person.", instigator)
            else:
                if subcommand.lower() in tiercommandarray:
                    bot.notice("It looks like that nick is unable to play duels.",instigator)
                    return
                subcommand = actualname(bot, subcommand)
                if subcommand in canduelarray and instigator in canduelarray:
                    bot.notice(instigator + ", It looks like you can duel " + subcommand + ".", instigator)
                else:
                    dowedisplay = 1
                    mustpassthesetoduel(bot, trigger, instigator, subcommand, dowedisplay)

        ## Title
        elif commandortarget == 'title':
            instigatortitle = get_database_value(bot, instigator, 'title')
            titletoset = get_trigger_arg(triggerargsarray, 2)
            if not titletoset:
                unsetmsg = ''
                if not instigatortitle:
                    unsetmsg = "You don't have a title! "
                bot.say(unsetmsg + "What do you want your title to be?")
            elif titletoset == 'remove':
                reset_database_value(bot, instigator, 'title')
                bot.say("Your title has been removed")
            else:
                titletoset = str(titletoset)
                instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
                if instigatorcoin < changeclasscost:
                    bot.say("Changing your title costs " + str(changeclasscost) + " coin. You need more funding.")
                elif len(titletoset) > 10:
                    bot.say("Purchased titles can be no longer than 10 characters")
                else:
                    set_database_value(bot, instigator, 'title', titletoset)
                    adjust_database_value(bot, instigator, 'coin', -abs(changeclasscost))
                    bot.say("Your title is now " + titletoset)
            
        ## Class
        elif commandortarget == 'class':
            subcommandarray = ['set','change']
            classes = get_trigger_arg(classarray, "list")
            subcommand = get_trigger_arg(triggerargsarray, 2).lower()
            setclass = get_trigger_arg(triggerargsarray, 3).lower()
            instigatorclass = get_database_value(bot, instigator, 'class')
            instigatorfreebie = get_database_value(bot, instigator, 'classfreebie') or 0
            classtime = get_timesince_duels(bot, instigator, 'classtimeout')
            instigatorclasstime = get_timesince_duels(bot, instigator, 'classtimeout')
            instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
            if not instigatorclass and not subcommand:
                bot.say("You don't appear to have a class set. Options are : " + classes + ". Run .duel class set    to set your class.")
            elif not subcommand:
                bot.say("Your class is currently set to " + str(instigatorclass) + ". Use .duel class change    to change class. Options are : " + classes + ".")
            elif classtime < CLASSTIMEOUT and not bot.nick.endswith(devbot):
                bot.say("You may not change your class more than once per 24 hours. Please wait "+str(hours_minutes_seconds((CLASSTIMEOUT - instigatorclasstime)))+" to change.")
            elif subcommand not in subcommandarray:
                bot.say("Invalid command. Options are set or change.")
            elif not setclass:
                bot.say("Which class would you like to use? Options are: " + classes +".")
            elif instigatorcoin < changeclasscost and instigatorfreebie:
                bot.say("Changing class costs " + str(changeclasscost) + " coin. You need more funding.")
            elif setclass not in classarray:
                bot.say("Invalid class. Options are: " + classes +".")
            elif setclass == instigatorclass:
                bot.say('Your class is already set to ' +  setclass)
            else:
                statreset(bot, instigator)
                healthcheck(bot, instigator)
                set_database_value(bot, instigator, 'class', setclass)
                bot.say('Your class is now set to ' +  setclass)
                set_database_value(bot, instigator, 'classtimeout', now)
                if instigatorfreebie:
                    adjust_database_value(bot, instigator, 'coin', -abs(changeclasscost))
                else:
                    set_database_value(bot, instigator, 'classfreebie', 1)

        ## Streaks
        elif commandortarget == 'streaks':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in [u.lower() for u in bot.users]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            else:
                if target.lower() in tiercommandarray:
                    bot.notice("It looks like that nick is unable to play duels.",instigator)
                    return
                target = actualname(bot, target)
                healthcheck(bot, target)
                statreset(bot, target)
                streak_type = get_database_value(bot, target, 'currentstreaktype') or 'none'
                best_wins = get_database_value(bot, target, 'bestwinstreak') or 0
                worst_losses = get_database_value(bot, target, 'worstlosestreak') or 0
                if streak_type == 'win':
                    streak_count = get_database_value(bot, target, 'currentwinstreak') or 0
                    typeofstreak = 'winning'
                elif streak_type == 'loss':
                    streak_count = get_database_value(bot, target, 'currentlosestreak') or 0
                    typeofstreak = 'losing'
                else:
                    streak_count = 0
                if streak_count > 1 and streak_type != 'none':
                    displaymessage = str(displaymessage + "Currently on a " + typeofstreak + " streak of " + str(streak_count) + ".     ")
                if int(best_wins) > 1:
                    displaymessage = str(displaymessage + "Best Win streak= " + str(best_wins) + ".     ")
                if int(worst_losses) > 1:
                    displaymessage = str(displaymessage + "Worst Losing streak= " + str(worst_losses) + ".     ")
                if displaymessage == '':
                    bot.say(target + " has no streaks.")
                else:
                    bot.say(target + "'s streaks: " + displaymessage)

        ## Stats
        elif commandortarget == 'stats':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in [u.lower() for u in bot.users]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            elif int(tiercommandeval) > int(currenttier) and target != instigator and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", Stats for other players cannot be viewed until somebody reaches " + str(tierpepperrequired) + ". "+str(tiermath) + " tier(s) remaining!", instigator)
            else:
                if target.lower() in tiercommandarray:
                    bot.notice("It looks like that nick is unable to play duels.",instigator)
                    return
                target = actualname(bot, target)
                #healthcheck(bot, target)
                statreset(bot, target)
                for x in duelstatsarray:
                    if x in statsbypassarray:
                        scriptdef = str('get_' + x + '(bot,target)')
                        gethowmany = eval(scriptdef)
                    else:
                        gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        if x == 'winlossratio':
                            gethowmany = format(gethowmany, '.3f')
                        addstat = str(' ' + str(x) + "=" + str(gethowmany))
                        displaymessage = str(displaymessage + addstat)
                if displaymessage != '':
                    pepper = get_pepper(bot, target)
                    if not pepper or pepper == '':
                        targetname = target
                    else:
                        targetname = str("(" + str(pepper) + ") " + target)
                    displaymessage = str(targetname + "'s " + commandortarget + ":" + displaymessage)
                    bot.say(displaymessage)
                else:
                    bot.say(instigator + ", It looks like " + target + " has no " +  commandortarget + ".", instigator)

        ## Leaderboard
        elif commandortarget == 'leaderboard':
            subcommand = get_trigger_arg(triggerargsarray, 2)
            if not subcommand:
                leaderscript = []
                leaderboardarraystats = ['winlossratio','kills','respawns','health','bestwinstreak','worstlosestreak','bounty']
                worstlosestreakdispmsg, worstlosestreakdispmsgb = "Worst Losing Streak:", ""
                winlossratiodispmsg, winlossratiodispmsgb = "Wins/Losses:", ""
                killsdispmsg, killsdispmsgb = "Most Kills:", "kills"
                respawnsdispmsg, respawnsdispmsgb = "Most Deaths:", "respawns"
                healthdispmsg, healthdispmsgb = "Closest To Death:", "health"
                bestwinstreakdispmsg, bestwinstreakdispmsgb = "Best Win Streak:", ""
                bountydispmsg, bountydispmsgb = "Largest Bounty:", "coins"
                for x in leaderboardarraystats:
                    statleadername = ''
                    if x != 'health':
                        statleadernumber = 0
                    else:
                        statleadernumber = 99999999
                    for u in bot.users:
                        #healthcheck(bot, u)
                        statreset(bot, u)
                        if u in dueloptedinarray:
                            if x != 'winlossratio':
                                statamount = get_database_value(bot, u, x)
                            else:
                                scriptdef = str('get_' + x + '(bot,u)')
                                statamount = eval(scriptdef)
                            if statamount == statleadernumber and statamount > 0:
                                statleadername = str(statleadername+ " "+ u)
                            else:
                                if x != 'health':
                                    if statamount > statleadernumber:
                                        statleadernumber = statamount
                                        statleadername = u
                                else:
                                    if statamount < statleadernumber and statamount > 0:
                                        statleadernumber = statamount
                                        statleadername = u
                    if x == 'winlossratio':
                        statleadernumber = format(statleadernumber, '.3f')
                    if statleadername != '':
                        msgtoadd = str(eval(x+"dispmsg") + " "+ statleadername + " at "+ str(statleadernumber)+ " "+ eval(x+"dispmsgb"))
                        leaderscript.append(msgtoadd)
                if leaderscript == []:
                    displaymessage = str("Leaderboard appears to be empty")
                else:
                    for msg in leaderscript:
                        displaymessage = str(displaymessage+ msg+ "  ")
                bot.say(displaymessage)
            if subcommand.lower() == 'highest' or subcommand.lower() == 'lowest':
                subcommand = subcommand.lower()
                subcommanda = get_trigger_arg(triggerargsarray, 3)
                if not subcommanda:
                    bot.say("What stat do you want to check highest/losest?")
                elif subcommanda.lower() not in duelstatsadminarray and subcommanda.lower() != 'class':
                    bot.say("This stat is either not comparable at the moment or invalid.")
                else:
                    subcommanda = subcommanda.lower()
                    statleadername = ''
                    if subcommand == 'highest':
                        statleadernumber = 0
                    else:
                        statleadernumber = 99999999
                    for u in bot.users:
                        if subcommanda != 'winlossratio':
                            statamount = get_database_value(bot, u, subcommanda)
                        else:
                            scriptdef = str('get_' + subcommanda + '(bot,u)')
                            statamount = eval(scriptdef)
                        if statamount == statleadernumber and statamount > 0:
                            statleadername = str(statleadername+ " "+ u)
                        else:
                            if subcommand == 'highest':
                                if statamount > statleadernumber:
                                    statleadernumber = statamount
                                    statleadername = u
                            else:
                                if statamount < statleadernumber and statamount > 0:
                                    statleadernumber = statamount
                                    statleadername = u
                    if statleadername != '':
                        bot.say("The " + subcommand + " amount for "+ subcommanda+ " is " + statleadername+ " with "+ str(statleadernumber))
                    else:
                        bot.say("There doesn't appear to be a "+ subcommand + " amount for "+subcommanda+".")

        ## Armor
        elif commandortarget == 'armor':
            subcommand = get_trigger_arg(triggerargsarray, 2)
            typearmor = get_trigger_arg(triggerargsarray, 3)
            if not subcommand or subcommand.lower() in [x.lower() for x in dueloptedinarray]:
                target = get_trigger_arg(triggerargsarray, 2) or instigator
                if target.lower() not in [u.lower() for u in bot.users]:
                    bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                elif int(tiercommandeval) > int(currenttier) and target != instigator and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", Loot for other players cannot be viewed until somebody reaches " + str(tierpepperrequired) + ". "+str(tiermath) + " tier(s) remaining!", instigator)
                else:
                    if target.lower() in tiercommandarray:
                        bot.notice("It looks like that nick is unable to play duels.",instigator)
                        return
                    target = actualname(bot, target)
                    statreset(bot, target)
                    for x in armortypesarray:
                        gethowmany = get_database_value(bot, target, x)
                        if gethowmany:
                            addstat = str(' ' + str(x) + "=" + str(gethowmany))
                            displaymessage = str(displaymessage + addstat)
                    if displaymessage != '':
                        displaymessage = str(target + "'s " + commandortarget + " durability: " + displaymessage)
                        bot.say(displaymessage)
                    else:
                        bot.say(instigator + ", It looks like " + target + " has no " +  commandortarget + ".", instigator)
            elif subcommand == 'buy':
                instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
                if not typearmor or typearmor not in armortypesarray:
                    armors = get_trigger_arg(armortypesarray, 'list')
                    bot.say("What type of armor do you wish to " + subcommand + "? Options are: " + armors)
                elif instigatorcoin < armorcost:
                    bot.say("Insufficient Funds")
                else:
                    getarmor = get_database_value(bot, instigator, typearmor) or 0
                    if getarmor and getarmor > 0:
                        bot.say("It looks like you already have a " + typearmor + ".")
                    else:
                        bot.say(instigator + " bought " + typearmor + " for " + str(armorcost) + " coins.")
                        adjust_database_value(bot, instigator, 'coin', -abs(armorcost))
                        set_database_value(bot, instigator, typearmor, armormaxdurability)
            elif subcommand == 'sell':
                if not typearmor or typearmor not in armortypesarray:
                    armors = get_trigger_arg(armortypesarray, 'list')
                    bot.say("What type of armor do you wish to " + subcommand + "? Options are: " + armors)
                else:
                    getarmor = get_database_value(bot, instigator, typearmor) or 0
                    if not getarmor:
                        bot.say("You don't have a " + typearmor + " to sell.")
                    elif getarmor < 0:
                        bot.say("Your armor is too damaged to sell.")
                        reset_database_value(bot, instigator, typearmor)
                    else:
                        durabilityremaining = getarmor / armormaxdurability
                        sellingamount = durabilityremaining * armorcost
                        if sellingamount <= 0:
                            bot.say("Your armor is too damaged to sell.")
                        else:
                            bot.say("Selling your "+typearmor +" earned you " + str(sellingamount) + " coins.")
                            adjust_database_value(bot, instigator, 'coin', sellingamount)
                            reset_database_value(bot, instigator, typearmor)
            elif subcommand == 'repair':
                if not typearmor or typearmor not in armortypesarray:
                    armors = get_trigger_arg(armortypesarray, 'list')
                    bot.say("What type of armor do you wish to " + subcommand + "? Options are: " + armors)
                else:
                    getarmor = get_database_value(bot, instigator, typearmor) or 0
                    instigatorclass = get_database_value(bot, instigator, 'class')
                    durabilitycompare = armormaxdurability
                    if instigatorclass == 'armormaxdurability':
                        durabilitycompare = armormaxdurabilityblacksmith
                    if not getarmor:
                        bot.say("You don't have a " + typearmor + " to repair.")
                    elif getarmor >= durabilitycompare:
                        bot.say("It looks like your armor does not need repair.")
                    else:
                        durabilitytorepair = durabilitycompare - getarmor
                        if durabilitytorepair <= 0:
                            bot.say("Looks like you can't repair that right now.")
                        else:
                            instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
                            costinvolved  = durabilitytorepair / durabilitycompare
                            costinvolved = costinvolved * armorcost
                            if instigatorcoin < costinvolved:
                                bot.say("Insufficient Funds.")
                            else:
                                bot.say(typearmor + " repaired  for " + str(costinvolved)+" coins.")
                                adjust_database_value(bot, instigator, 'coin', -abs(costinvolved))
                                set_database_value(bot, instigator, typearmor, durabilitycompare)

        ## Bounty
        elif commandortarget == 'bounty':
            if not inchannel.startswith("#"):
                bot.notice(instigator + " Bounties must be in channel.", instigator)
                return
            instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
            target = get_trigger_arg(triggerargsarray, 2)
            target = actualname(bot, target)
            amount = get_trigger_arg(triggerargsarray, 3)
            if not amount.isdigit():
                bot.say("Invalid Amount.")
                return
            else:
                amount = int(amount)
            if not target:
                bot.say("You must pick a target.")
            elif target.lower() not in [u.lower() for u in bot.users]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif not amount:
                bot.say("How much of a bounty do you wish to place on "+target+".")
            elif int(instigatorcoin) < int(amount):
                bot.say("Insufficient Funds.")
            else:
                if target.lower() in tiercommandarray:
                    bot.notice("It looks like that nick is unable to play duels.",instigator)
                    return
                adjust_database_value(bot, instigator, 'coin', -abs(amount))
                bountyontarget = get_database_value(bot, target, 'bounty') or 0
                if not bountyontarget:
                    bot.say(instigator + " places a bounty of " + str(amount) + " on " + target)
                else:
                    bot.say(instigator + " adds " + str(amount) + " to the bounty on " + target)
                adjust_database_value(bot, target, 'bounty', amount)

        ## Loot Items
        elif commandortarget == 'loot':
            instigatorclass = get_database_value(bot, instigator, 'class')
            instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
            lootcommand = get_trigger_arg(triggerargsarray, 2).lower()
            if not lootcommand or lootcommand.lower() in [x.lower() for x in dueloptedinarray]:
                target = get_trigger_arg(triggerargsarray, 2) or instigator
                if target.lower() not in [u.lower() for u in bot.users]:
                    bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                elif int(tiercommandeval) > int(currenttier) and target != instigator and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", Loot for other players cannot be viewed until somebody reaches " + str(tierpepperrequired) + ". "+str(tiermath) + " tier(s) remaining!", instigator)
                else:
                    if target.lower() in tiercommandarray:
                        bot.notice("It looks like that nick is unable to play duels.",instigator)
                        return
                    target = actualname(bot, target)
                    statreset(bot, target)
                    for x in backpackarray:
                        gethowmany = get_database_value(bot, target, x)
                        if gethowmany:
                            if gethowmany == 1:
                                loottype = str(x)
                            else:
                                loottype = str(str(x)+"s")
                            addstat = str(' ' + str(loottype) + "=" + str(gethowmany))
                            displaymessage = str(displaymessage + addstat)
                    if displaymessage != '':
                        displaymessage = str(target + "'s " + commandortarget + ":" + displaymessage)
                        bot.say(displaymessage)
                    else:
                        bot.say(instigator + ", It looks like " + target + " has no " +  commandortarget + ".", instigator)
            elif lootcommand not in transactiontypesarray:
                transactiontypesarraylist = get_trigger_arg(transactiontypesarray, "list")
                bot.notice(instigator + ", It looks like " + lootcommand + " is either not here, not a valid person, or an invalid command. Valid commands are: " + transactiontypesarraylist, instigator)
            elif lootcommand == 'use':
                lootitem = get_trigger_arg(triggerargsarray, 3).lower()
                gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
                if not lootitem:
                    bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
                elif lootitem not in lootitemsarray and lootitem != 'grenade':
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif not gethowmanylootitem:
                    bot.notice(instigator + ", You do not have any " +  lootitem + "!", instigator)
                elif lootitem == 'magicpotion':
                    bot.notice("Magic Potions are not purchasable, sellable, or usable. They can only be traded.", instigator)
                elif lootitem == 'grenade':
                    if not inchannel.startswith("#"):
                        bot.notice(instigator + ", grenades must be used in channel.", instigator)
                        return
                    instigatorgrenade = get_database_value(bot, instigator, 'grenade') or 0
                    for u in bot.users:
                        if u in dueloptedinarray and u != bot.nick and u != instigator:
                            canduelarray.append(u)
                            statreset(bot, u)
                            healthcheck(bot, u)
                    if canduelarray == []:
                        bot.notice(instigator + ", It looks like using a grenade right now won't hurt anybody.", instigator)
                    else:
                        canduelarrayorig = []
                        for u in canduelarray:
                            canduelarrayorig.append(u)
                            targethealth = get_database_value(bot, u, 'health')
                        adjust_database_value(bot, instigator, lootitem, -1)
                        fulltarget, secondarytarget, thirdtarget = '','',''
                        fulltarget = get_trigger_arg(canduelarray, "random")
                        displaymsg = str(fulltarget + " takes the brunt of the grenade dealing " + str(abs(grenadefull)) + " damage. ")
                        canduelarray.remove(fulltarget)
                        if canduelarray != []:
                            secondarytarget = get_trigger_arg(canduelarray, "random")
                            canduelarray.remove(secondarytarget)
                            if canduelarray != []:
                                thirdtarget = get_trigger_arg(canduelarray, "random")
                                displaymsg = str(displaymsg + secondarytarget + " and " + thirdtarget + " jump away but still take " + str(abs(grenadesec)) + " damage. ")
                                canduelarray.remove(thirdtarget)
                                if canduelarray != []:
                                    remainingarray = get_trigger_arg(canduelarray, "list")
                                    displaymsg = str(displaymsg + remainingarray + " completely jump out of the way")
                            else:
                                displaymsg = str(displaymsg + secondarytarget + " jumps away but still takes " + str(abs(grenadesec)) + " damage. ")
                        painarray = []
                        damagearray = []
                        deatharray = []
                        if fulltarget != '':
                            painarray.append(fulltarget)
                            damagearray.append(grenadefull)
                        if secondarytarget != '':
                            painarray.append(secondarytarget)
                            damagearray.append(grenadesec)
                        if thirdtarget != '':
                            painarray.append(thirdtarget)
                            damagearray.append(grenadesec)
                        deathmsgb = ''
                        for x, damage in zip(painarray, damagearray):
                            damage = int(damage)
                            shieldloser = get_database_value(bot, x, 'shield') or 0
                            if shieldloser and damage > 0:
                                damagemath = int(shieldloser) - damage
                                if int(damagemath) > 0:
                                    adjust_database_value(bot, x, 'shield', -abs(damage))
                                    damage = 0
                                else:
                                    damage = abs(damagemath)
                                    reset_database_value(bot, x, 'shield')
                            if damage > 0:
                                adjust_database_value(bot, x, 'health', -abs(damage))
                            xhealth = get_database_value(bot, x, 'health') or 0
                            if int(xhealth) <= 0:
                                deathmsgb = whokilledwhom(bot, instigator, x) or ''
                                deatharray.append(x)
                        if deatharray != []:
                            deadarray = get_trigger_arg(deatharray, "list")
                            displaymsg = str(displaymsg + "    " + deadarray + " died by this grenade volley. " + deathmsgb)
                        if displaymsg != '':
                            bot.say(displaymsg)
                else:
                    targnum = get_trigger_arg(triggerargsarray, 4).lower()
                    if not targnum:
                        quantity = 1
                        target = instigator
                    elif targnum.isdigit():
                        quantity = int(targnum)
                        target = instigator
                    elif targnum.lower() in [x.lower() for x in dueloptedinarray]:
                        targnumb = get_trigger_arg(triggerargsarray, 5).lower()
                        target = targnum
                        if not targnumb:
                            quantity = 1
                        elif targnumb.isdigit():
                            quantity = int(targnumb)
                        elif targnumb == 'all':
                            quantity = int(gethowmanylootitem)
                        else:
                            bot.say("Invalid command.")
                            return
                    elif targnum == 'all':
                        target = instigator
                        quantity = int(gethowmanylootitem)
                    elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                        bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
                    elif target.lower() not in [u.lower() for u in bot.users]:
                        bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                    else:
                        bot.say("Invalid command.")
                        return
                    targetclass = get_database_value(bot, target, 'class') or 'notclassy'
                    if int(gethowmanylootitem) < int(quantity):
                        bot.notice(instigator + ", You do not have enough " +  lootitem + " to use this command!", instigator)
                    elif target == bot.nick:
                        bot.notice(instigator + ", I am immune to " + lootitem, instigator)
                    elif target.lower() != instigator.lower() and targetclass == 'fiend':
                        bot.notice(instigator + ", It looks like " + target + " is a fiend and can only self-use potions.", instigator)
                        adjust_database_value(bot, instigator, lootitem, -abs(quantity))
                    else:
                        if target.lower() in tiercommandarray:
                            bot.notice("It looks like that nick is unable to play duels.",instigator)
                            return
                        target = actualname(bot, target)
                        uselootarray = []
                        adjust_database_value(bot, instigator, lootitem, -abs(quantity))
                        lootusedeaths = 0
                        if lootitem == 'mysterypotion':
                            while int(quantity) > 0:
                                quantity = quantity - 1
                                loot = get_trigger_arg(lootitemsarray, 'random')
                                if loot == 'mysterypotion' or loot == 'magicpotion':
                                    loot = get_trigger_arg(nulllootitemsarray, 'random')
                                uselootarray.append(loot)
                        else:
                            while int(quantity) > 0:
                                quantity = quantity - 1
                                uselootarray.append(lootitem)
                        uselootarraytotal = len(uselootarray)
                        extramsg = '.'
                        if lootitem == 'healthpotion':
                            if targetclass == 'barbarian':
                                potionmaths = int(uselootarraytotal) * healthpotionworthbarbarian
                            else:
                                potionmaths = int(uselootarraytotal) * healthpotionworth
                            extramsg = str(" restoring " + str(potionmaths) + " health.")
                        elif lootitem == 'poisonpotion':
                            poisonpotionworthb = abs(poisonpotionworth)
                            potionmaths = int(uselootarraytotal) * int(poisonpotionworthb)
                            extramsg = str(" draining " + str(potionmaths) + " health.")
                        elif lootitem == 'manapotion':
                            if targetclass == 'mage':
                                potionmaths = int(uselootarraytotal) * manapotionworthmage
                            else:
                                potionmaths = int(uselootarraytotal) * manapotionworth
                            extramsg = str(" restoring " + str(potionmaths) + " mana.")
                        elif lootitem == 'timepotion':
                            extramsg = str(" removing timeouts.")        
                        if target == instigator:
                            if int(uselootarraytotal) == 1:
                                mainlootusemessage = str(instigator + ' uses ' + lootitem + extramsg)
                            else:
                                mainlootusemessage = str(instigator + ' uses ' + str(uselootarraytotal) + " " + lootitem + 's' + extramsg)
                        else:
                            if int(uselootarraytotal) == 1:
                                mainlootusemessage = str(instigator + ' uses ' + lootitem + ' on ' + target + extramsg)
                            else:
                                mainlootusemessage = str(instigator + " used " + str(uselootarraytotal) + " " + lootitem + "s on " + target +extramsg)
                        for x in uselootarray:
                            if x == 'healthpotion':
                                if targetclass == 'barbarian':
                                    adjust_database_value(bot, target, 'health', healthpotionworthbarbarian)
                                else:
                                    adjust_database_value(bot, target, 'health', healthpotionworth)
                            elif x == 'poisonpotion':
                                adjust_database_value(bot, target, 'health', poisonpotionworth)
                            elif x == 'manapotion':
                                if targetclass == 'mage':
                                    adjust_database_value(bot, target, 'mana', manapotionworthmage)
                                else:
                                    adjust_database_value(bot, target, 'mana', manapotionworth)
                            elif x == 'timepotion':
                                reset_database_value(bot, target, 'lastfought')
                                for k in timepotiontargetarray:
                                    targetequalcheck = get_database_value(bot, duelrecorduser, k) or bot.nick
                                    if targetequalcheck == target:
                                        reset_database_value(bot, duelrecorduser, k)
                                for j in timepotiontimeoutarray:
                                    reset_database_value(bot, target, j)
                                reset_database_value(bot, duelrecorduser, 'timeout')
                            targethealth = get_database_value(bot, target, 'health')
                            if targethealth <= 0:
                                lootusedeaths = lootusedeaths + 1
                                if target == instigator:
                                    deathmsgb = suicidekill(bot,loser)
                                else:
                                    deathmsgb = whokilledwhom(bot, instigator, target) or ''
                                mainlootusemessage = str(mainlootusemessage + " "+ deathmsgb)
                        if lootitem == 'mysterypotion':
                            actualpotionmathedarray = []
                            alreadyprocessedarray = []
                            for fluid in uselootarray:
                                if fluid not in alreadyprocessedarray:
                                    alreadyprocessedarray.append(fluid)
                                    countedeval = uselootarray.count(fluid)
                                    if countedeval > 1:
                                        actualpotionmathedarray.append(str(str(countedeval) + " "+fluid + "s"))
                                    else:
                                        actualpotionmathedarray.append(fluid)
                            postionsusedarray = get_trigger_arg(actualpotionmathedarray, "list")
                            mainlootusemessage = str(mainlootusemessage + " Potion(s) used: " + postionsusedarray)
                        if lootusedeaths > 0:
                            if lootusedeaths == 1:
                                mainlootusemessage = str(mainlootusemessage + " This resulted in death.")
                            else:
                                mainlootusemessage = str(mainlootusemessage + " This resulted in "+str(lootusedeaths)+" deaths.")
                        bot.say(mainlootusemessage)
                        if target != instigator and not inchannel.startswith("#"):
                            bot.notice(mainlootusemessage, target)
            elif lootcommand == 'buy':
                lootitem = get_trigger_arg(triggerargsarray, 3).lower()
                if not lootitem:
                    bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
                elif lootitem not in lootitemsarray and lootitem != 'grenade':
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif lootitem == 'magicpotion':
                    bot.say("Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
                else:
                    quantity = get_trigger_arg(triggerargsarray, 4).lower() or 1
                    if quantity == 'all':
                        if instigatorclass == 'scavenger':
                            quantity = int(instigatorcoin) / lootbuycostscavenger
                        else:
                            quantity = int(instigatorcoin) / lootbuycostscavenger
                        if not quantity > 1:
                            bot.notice(instigator + ", You do not have enough coin for this action.", instigator)
                            return
                    quantity = int(quantity)
                    if instigatorclass == 'scavenger':
                        coinrequired = lootbuycostscavenger * int(quantity)
                    else:
                        coinrequired = lootbuycost * int(quantity)
                    if instigatorcoin < coinrequired:
                        bot.notice(instigator + ", You do not have enough coin for this action.", instigator)
                    else:
                        adjust_database_value(bot, instigator, 'coin', -abs(coinrequired))
                        adjust_database_value(bot, instigator, lootitem, quantity)
                        bot.say(instigator + " bought " + str(quantity) +  " "+lootitem + "s for " +str(coinrequired)+ " coins.")
            elif lootcommand == 'sell':
                lootitem = get_trigger_arg(triggerargsarray, 3).lower()
                gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
                if not lootitem:
                    bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
                elif lootitem not in lootitemsarray and lootitem != 'grenade':
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif not gethowmanylootitem:
                    bot.notice(instigator + ", You do not have any " +  lootitem + "!", instigator)
                elif lootitem == 'magicpotion':
                    bot.say("Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
                else:
                    quantity = get_trigger_arg(triggerargsarray, 4).lower() or 1
                    if quantity == 'all':
                        quantity = gethowmanylootitem
                    if int(quantity) > gethowmanylootitem:
                        bot.notice(instigator + ", You do not have enough " + lootitem + " for this action.", instigator)
                    else:
                        quantity = int(quantity)
                        if instigatorclass == 'scavenger':
                            reward = lootsellrewardscavenger * int(quantity)
                        else:
                            reward = lootsellreward * int(quantity)
                        adjust_database_value(bot, instigator, 'coin', reward)
                        adjust_database_value(bot, instigator, lootitem, -abs(quantity))
                        bot.say(instigator + " sold " + str(quantity) + " "+ lootitem + "s for " +str(reward)+ " coins.")
            elif lootcommand == 'trade':
                lootitem = get_trigger_arg(triggerargsarray, 3).lower()
                lootitemb = get_trigger_arg(triggerargsarray, 4).lower()
                if not lootitem or not lootitemb:
                    bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
                elif lootitem not in lootitemsarray or lootitemb not in lootitemsarray:
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif lootitem == 'grenade' or lootitemb == 'grenade':
                    bot.notice(instigator + ", You can't trade for grenades.", instigator)
                elif lootitemb == lootitem:
                    bot.notice(instigator + ", You can't trade for the same type of potion.", instigator)
                else:
                    gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
                    quantity = get_trigger_arg(triggerargsarray, 5).lower() or 1
                    if lootitem == 'magicpotion':
                        tradingratio = 1
                    elif instigatorclass == 'scavenger':
                        tradingratio = traderatioscavenger
                    else:
                        tradingratio = traderatio
                    if quantity == 'all':
                        quantity = gethowmanylootitem / tradingratio
                    if quantity < 0:
                        bot.notice(instigator + ", You do not have enough "+lootitem+" for this action.", instigator)
                        return
                    quantitymath = tradingratio * int(quantity)
                    if gethowmanylootitem < quantitymath:
                        bot.notice(instigator + ", You don't have enough of this item to trade.", instigator)
                    else:
                        adjust_database_value(bot, instigator, lootitem, -abs(quantitymath))
                        adjust_database_value(bot, instigator, lootitemb, quantity)
                        quantity = int(quantity)
                        bot.say(instigator + " traded " + str(quantitymath) + " "+ lootitem + "s for " +str(quantity) + " "+ lootitemb+ "s.")
                    
        ## Weaponslocker
        elif commandortarget == 'weaponslocker':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            validdirectionarray = ['total','inv','add','del','reset']
            if target in validdirectionarray:
                target = instigator
                adjustmentdirection = get_trigger_arg(triggerargsarray, 2).lower()
                weaponchange = get_trigger_arg(triggerargsarray, '3+')
            else:
                adjustmentdirection = get_trigger_arg(triggerargsarray, 3).lower()
                weaponchange = get_trigger_arg(triggerargsarray, '4+')
            weaponslist = get_database_value(bot, target, 'weaponslocker') or []
            statreset(bot, target)
            if target.lower() in tiercommandarray:
                bot.notice("It looks like that nick is unable to play duels.",instigator)
                return
            target = actualname(bot, target)
            if not adjustmentdirection:
                bot.notice(instigator + ", Use .duel weaponslocker add/del to adjust Locker Inventory.", instigator)
            elif adjustmentdirection == 'total':
                gethowmany = get_database_array_total(bot, target, 'weaponslocker')
                bot.say(target + ' has ' + str(gethowmany) + " weapons in their locker. They Can be viewed in privmsg by running .duel weaponslocker inv")
            elif adjustmentdirection == 'inv':
                weapons = get_trigger_arg(weaponslist, 'list')
                chunks = weapons.split()
                per_line = 20
                weaponline = ''
                for i in range(0, len(chunks), per_line):
                    weaponline = " ".join(chunks[i:i + per_line])
                    bot.notice(str(weaponline), instigator)
                if weaponline == '':
                    bot.notice(instigator + ", There doesnt appear to be anything in the weapons locker! Use .duel weaponslocker add/del to adjust Locker Inventory.", instigator)
            elif target != instigator and not trigger.admin:
                bot.notice(instigator + ", You may not adjust somebody elses locker.", instigator)
            elif adjustmentdirection == 'reset':
                reset_database_value(bot, target, 'weaponslocker')
                bot.notice(instigator + ", Locker Reset.", instigator)
            else:
                if not weaponchange:
                    bot.notice(instigator + ", What weapon would you like to add/remove?", instigator)
                elif adjustmentdirection != 'add' and adjustmentdirection != 'del':
                    bot.say('Invalid Command.')
                elif adjustmentdirection == 'add' and weaponchange in weaponslist:
                    bot.notice(weaponchange + " is already in weapons locker.", instigator)
                elif adjustmentdirection == 'del' and weaponchange not in weaponslist:
                    bot.notice(weaponchange + " is already not in weapons locker.", instigator)
                elif adjustmentdirection == 'add' and len(weaponchange) > weaponmaxlength:
                    bot.notice("That weapon exceeds the character limit of "+str(weaponmaxlength)+".", instigator)
                else:
                    if adjustmentdirection == 'add':
                        weaponlockerstatus = 'now'
                    else:
                        weaponlockerstatus = 'no longer'
                    adjust_database_array(bot, target, weaponchange, 'weaponslocker', adjustmentdirection)
                    message = str(weaponchange + " is " + weaponlockerstatus + " in weapons locker.")
                    bot.notice(instigator + ", " + message, instigator)

        ## Magic
        elif commandortarget == 'magic':
            instigatorclass = get_database_value(bot, instigator, 'class')
            instigatormana = get_database_value(bot, instigator, 'mana')
            magicusage = get_trigger_arg(triggerargsarray, 2)
            if not magicusage or magicusage not in magicoptionsarray:
                magicoptions = get_trigger_arg(magicoptionsarray, 'list')
                bot.say('Magic uses include: '+ magicoptions)
            else:
                targnum = get_trigger_arg(triggerargsarray, 3).lower()
                if not targnum:
                    quantity = 1
                    target = instigator
                elif targnum.isdigit():
                    quantity = int(targnum)
                    target = instigator
                elif targnum.lower() in [x.lower() for x in dueloptedinarray]:
                    targnumb = get_trigger_arg(triggerargsarray, 4).lower()
                    target = targnum
                    if not targnumb:
                        quantity = 1
                    elif targnumb.isdigit():
                        quantity = int(targnumb)
                    elif targnumb == 'all':
                        quantity = int(gethowmanylootitem)
                    else:
                        bot.say("Invalid command.")
                        return
                elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                    bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
                elif target.lower() not in [u.lower() for u in bot.users]:
                    bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                elif target == bot.nick:
                    bot.notice(instigator + ", I am immune to magic " + magicusage, instigator)
                elif not instigatormana:
                    bot.notice(instigator + " you don't have any mana.", instigator)
                else:
                    bot.say("Invalid command.")
                    return
                if target.lower() in tiercommandarray:
                    bot.notice("It looks like that nick is unable to play duels.",instigator)
                    return
                target = actualname(bot, target)
                statreset(bot, target)
                healthcheck(bot, target)
                targetcurse = get_database_value(bot, target, 'curse') or 0
                targetclass = get_database_value(bot, target, 'class') or 'notclassy'
                if target.lower() != instigator.lower() and targetclass == 'fiend':
                    bot.notice(instigator + ", It looks like " + target + " is a fiend and can only self-use magic.", instigator)
                    manarequired = -abs(manarequired)
                    adjust_database_value(bot, instigator, 'mana', manarequired)
                elif magicusage == 'curse' and targetcurse:
                    bot.notice(instigator + " it looks like " + target + " is already cursed.", instigator)
                    return
                elif magicusage == 'curse':
                    manarequired = manarequiredmagiccurse
                elif magicusage == 'shield':
                    manarequired = manarequiredmagicshield
                else:
                    return
                if instigatorclass == 'mage':
                    manarequired = manarequired * magemanamagiccut
                actualmanarequired = int(manarequired) * int(quantity)
                if int(actualmanarequired) > int(instigatormana):
                    manamath = int(int(actualmanarequired) - int(instigatormana))
                    bot.notice(instigator + " you need " + str(manamath) + " more mana to use magic " + magicusage + ".", instigator)
                else:
                    specialtext = ''
                    manarequired = -abs(actualmanarequired)
                    adjust_database_value(bot, instigator, 'mana', manarequired)
                    if magicusage == 'curse':
                        damagedealt = magiccursedamage * int(quantity)
                        set_database_value(bot, target, 'curse', curseduration)
                        specialtext = str("which forces " + target + " to lose the next " + str(curseduration) + " duels AND deals " + str(abs(damagedealt))+ " damage.")
                        adjust_database_value(bot, target, 'health', int(damagedealt))
                    elif magicusage == 'shield':
                        damagedealt = magicshielddamage * int(quantity)
                        actualshieldduration = int(quantity) * int(shieldduration)
                        adjust_database_value(bot, target, 'shield', actualshieldduration)
                        specialtext = str("which allows " + target + " to take no damage for the duration of " + str(actualshieldduration) + " damage AND restoring " +str(abs(damagedealt)) + " health.")
                        adjust_database_value(bot, target, 'health', int(damagedealt))
                    if instigator == target:
                        displaymsg = str(instigator + " uses magic " + magicusage + " " + specialtext + ".")
                    else:
                        displaymsg = str(instigator + " uses magic " + magicusage + " on " + target + " " + specialtext + ".")
                    bot.say(str(displaymsg))
                    if not inchannel.startswith("#") and target != instigator:
                        bot.notice(str(displaymsg), target)
                    instigatormana = get_database_value(bot, instigator, 'mana')
                    if instigatormana <= 0:
                        reset_database_value(bot, instigator, 'mana')

        ## Admin Commands
        elif commandortarget == 'admin' and not trigger.admin:
            bot.notice(instigator + ", This is an admin only functionality.", instigator)
        elif commandortarget == 'admin':
            subcommand = get_trigger_arg(triggerargsarray, 2).lower()
            settingchange = get_trigger_arg(triggerargsarray, 3).lower()
            if not subcommand:
                bot.notice(instigator + ", What Admin change do you want to make?", instigator)
            elif subcommand == 'channel':
                if not settingchange:
                    bot.notice(instigator + ", What channel setting do you want to change?", instigator)
                elif settingchange == 'lastassault':
                    reset_database_value(bot, duelrecorduser, 'lastfullroomassultinstigator')
                    bot.notice("Last Assault Instigator removed.", instigator)
                    reset_database_value(bot, duelrecorduser, 'lastfullroomassult')
                elif settingchange == 'lastroman':
                    reset_database_value(bot, duelrecorduser, 'lastfullroomcolosseuminstigator')
                    bot.notice("Last Colosseum Instigator removed.", instigator)
                    reset_database_value(bot, duelrecorduser, 'lastfullroomcolosseum')
                elif settingchange == 'lastinstigator':
                    reset_database_value(bot, duelrecorduser, 'lastinstigator')
                    bot.notice("Last Fought Instigator removed.", instigator)
                elif settingchange == 'halfhoursim':
                    bot.notice("Simulating the half hour automated events.", instigator)
                    halfhourtimer(bot)
                else:
                    bot.notice("Must be an invalid command.", instigator)
            elif subcommand == 'stats':
                incorrectdisplay = "A correct command use is .duel admin stats target set/reset stat"
                target = get_trigger_arg(triggerargsarray, 3)
                subcommand = get_trigger_arg(triggerargsarray, 4)
                statset = get_trigger_arg(triggerargsarray, 5)
                newvalue = get_trigger_arg(triggerargsarray, 6)
                if not target:
                    bot.notice(instigator + ", Target Missing. " + incorrectdisplay, instigator)
                elif target.lower() not in [u.lower() for u in bot.users] and target != 'everyone':
                    bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
                elif not subcommand:
                    bot.notice(instigator + ", Subcommand Missing. " + incorrectdisplay, instigator)
                elif subcommand not in statsadminchangearray:
                    bot.notice(instigator + ", Invalid subcommand. " + incorrectdisplay, instigator)
                elif not statset:
                    bot.notice(instigator + ", Stat Missing. " + incorrectdisplay, instigator)
                elif statset not in duelstatsadminarray and statset != 'all':
                    bot.notice(instigator + ", Invalid stat. " + incorrectdisplay, instigator)
                elif not trigger.admin:
                    bot.notice(instigator + "This is an admin only function.", instigator)
                else:
                    if target.lower() in tiercommandarray:
                        bot.notice("It looks like that nick is unable to play duels.",instigator)
                        return
                    target = actualname(bot, target)
                    if subcommand == 'reset':
                        newvalue = None
                    if subcommand == 'set' and newvalue == None:
                        bot.notice(instigator + ", When using set, you must specify a value. " + incorrectdisplay, instigator)
                    elif target == 'everyone':
                        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
                        reset_database_value(bot, duelrecorduser, 'levelingtier')
                        reset_database_value(bot, duelrecorduser, 'specevent')
                        for u in bot.users:
                            statreset(bot, target)
                            if statset == 'all':
                                for x in duelstatsadminarray:
                                    set_database_value(bot, u, x, newvalue)
                            else:
                                set_database_value(bot, u, statset, newvalue)
                        bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
                    else:
                        statreset(bot, target)
                        try:
                            if newvalue.isdigit():
                                newvalue = int(newvalue)
                        except AttributeError:
                            newvalue = newvalue
                        if statset == 'all':
                            for x in duelstatsadminarray:
                                set_database_value(bot, target, x, newvalue)
                        else:
                            set_database_value(bot, target, statset, newvalue)
                        bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
            elif subcommand == 'resettier':
                reset_database_value(bot, duelrecorduser, 'levelingtier')
            elif subcommand == 'bugbounty':
                target = get_trigger_arg(triggerargsarray, 3)
                statreset(bot, target)
                if not target:
                    bot.notice(instigator + ", Target Missing. ", instigator)
                elif target.lower() not in [u.lower() for u in bot.users]:
                    bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
                elif not trigger.admin:
                    bot.notice(instigator + "This is an admin only function.", instigator)
                else:
                    target = actualname(bot, target)
                    bot.say(target + ' is awarded ' + str(bugbountycoinaward) + " coin for finding a bug in duels.")
                    adjust_database_value(bot, target, 'coin', bugbountycoinaward)
                    
        ## Konami
        elif commandortarget == 'upupdowndownleftrightleftrightba':
            konami = get_database_value(bot, instigator, 'konami')
            if not konami:
                set_database_value(bot, instigator, 'konami', 1)
                bot.notice(instigator + " you have found the cheatcode easter egg!!!", instigator)
                konamiset = 600
                adjust_database_value(bot, instigator, 'health', konamiset)
            else:
                bot.notice(instigator + " you can only cheat once.", instigator)
        
        ## Command Valid, but not coded yet
        else:
            bot.notice(instigator + " This command is a Work In Progress.", instigator)
             
    ## not in the room
    elif commandortarget.lower() not in [u.lower() for u in bot.users]:
        bot.notice(instigator + ", It looks like " + str(commandortarget) + " is either not here, or not a valid person.", instigator)

    ## warning if user doesn't have duels enabled
    elif commandortarget.lower() not in [x.lower() for x in dueloptedinarray] and commandortarget != bot.nick:
        commandortarget = actualname(bot, commandortarget)
        bot.notice(instigator + ", It looks like " + commandortarget + " has duels off.", instigator)
    
    ## Duels must be in a channel
    elif not inchannel.startswith("#"):
        bot.notice(instigator + ", Duels must be in a channel.", instigator)

    else:
        OSDTYPE = 'say'
        target = get_trigger_arg(triggerargsarray, 1)
        if target.lower() in tiercommandarray:
            bot.notice("It looks like that nick is unable to play duels.",instigator)
            return
        dowedisplay = 1
        executedueling = mustpassthesetoduel(bot, trigger, instigator, target, dowedisplay)
        if executedueling:
            target = actualname(bot, target)
            healthcheck(bot, target)
            targetarray.append(target)
            getreadytorumble(bot, trigger, instigator, targetarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, inchannel)

    ## bot does not need stats or backpack items
    refreshbot(bot)

def getreadytorumble(bot, trigger, instigator, targetarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, channel):
    
    healthcheck(bot, instigator)
    assaultstatsarray = ['wins','losses','potionswon','potionslost','kills','deaths','damagetaken','damagedealt','levelups','xp']
    getreadytorumblenamearray = ['nicktitles','nickpepper','nickmagicattributes','nickarmor']
    ## clean empty stats
    assaultdisplay = ''
    assault_xp, assault_wins, assault_losses, assault_potionswon, assault_potionslost, assault_deaths, assault_kills, assault_damagetaken, assault_damagedealt, assault_levelups = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    targetarraytotal = len(targetarray)
    for target in targetarray:
        targetarraytotal = targetarraytotal - 1
        
        ## Cleanup
        combattextarraycomplete = []
        texttargetarray = []
        
        ## Check for new player health
        healthcheck(bot, target)
        ## verify stats aren't old
        statreset(bot, target)
        
        ## Assault does not touch lastfought
        if typeofduel == 'assault':
            targetlastfoughtstart = get_database_value(bot, target, 'lastfought')
        
        ## Same person can't instigate twice in a row
        set_database_value(bot, duelrecorduser, 'lastinstigator', instigator)
        
        ## Update last fought
        if instigator != target:
            set_database_value(bot, instigator, 'lastfought', target)
            set_database_value(bot, target, 'lastfought', instigator)
        
        ## Update Time Of Combat
        set_database_value(bot, instigator, 'timeout', now)
        set_database_value(bot, target, 'timeout', now)
        set_database_value(bot, duelrecorduser, 'timeout', now)
        
        ## Starting Tier
        currenttierstart = get_database_value(bot, duelrecorduser, 'levelingtier') or 0

        ## Magic Attributes Start
        instigatorshieldstart, targetshieldstart, instigatorcursestart, targetcursestart = get_current_magic_attributes(bot, instigator, target)

        ## Display Naming
        instigatorname = ''
        targetname = ''
        instigatorpepperstart = get_pepper(bot, instigator)
        for q in getreadytorumblenamearray:
            instigatorscriptdef = str(q + "(bot, instigator, channel)")
            instigatornameadd = eval(instigatorscriptdef)
            instigatornameadd = str(instigatornameadd)
            if instigatorname == '':
                instigatorname = str(instigatornameadd)
            else:
                instigatorname = str(instigatorname + " " + instigatornameadd)
        if instigator == target:
            targetname = "themself"
            targetpepperstart = ''
        else:
            targetpepperstart = get_pepper(bot, target)
            for q in getreadytorumblenamearray:
                targetscriptdef = str(q + "(bot, target, channel)")
                targetnameadd = eval(targetscriptdef)
                targetnameadd = str(targetnameadd)
                if targetname == '':
                    targetname = str(targetnameadd)
                else:
                    targetname = str(targetname + " " + targetnameadd)

        ## Announce Combat
        announcecombatmsg = str(instigatorname + " versus " + targetname)
        combattextarraycomplete.append(announcecombatmsg)
            
        ## Chance of Instigator finding loot
        lootwinnermsg = ''
        randominventoryfind = randominventory(bot, instigator)
        if randominventoryfind == 'true' and target != bot.nick and instigator != target:
            loot = get_trigger_arg(lootitemsarray, 'random')
            loot_text = eval(loot+"dispmsg")
            lootwinnermsg = str(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
            combattextarraycomplete.append(lootwinnermsg)
        
        ## Select Winner
        if target == bot.nick:
            winner = bot.nick
            loser = instigator
        else:
            nickarray = [instigator, target]
            winner = selectwinner(bot, nickarray)
            if winner == instigator:
                loser = target
            else:
                loser = instigator
        
        ## classes
        yourclasswinner = get_database_value(bot, winner, 'class') or 'notclassy'
        yourclassloser = get_database_value(bot, loser, 'class') or 'notclassy'
        
        ## Current Streaks
        winner_loss_streak, loser_win_streak = get_current_streaks(bot, winner, loser)

        ## Update Wins and Losses
        if instigator != target:
            adjust_database_value(bot, winner, 'wins', defaultadjust)
            adjust_database_value(bot, loser, 'losses', defaultadjust)
            set_current_streaks(bot, winner, 'win')
            set_current_streaks(bot, loser, 'loss')
        
        ## Manual weapon
        weapon = get_trigger_arg(triggerargsarray, '2+')
        if winner == instigator and weapon and currenttierstart >= tierunlockweaponslocker:
            if weapon == 'all':
                weapon = getallchanweaponsrandom(bot)
            elif weapon == 'target':
                weapon = weaponofchoice(bot, target)
                weapon = str(target + "'s " + weapon)
        elif winner == bot.nick:
            weapon = ''
        else:
            weapon = weaponofchoice(bot, winner)
        weapon = weaponformatter(bot, weapon)
        if weapon != '':
            weapon = str(" " + weapon)
        
        ## Combat Process
        damage, winnermsgarray = damagedone(bot, winner, loser, weapon, 1)
        for x in winnermsgarray:
            combattextarraycomplete.append(x)
            
        ## Update Health Of Loser, respawn, allow winner to loot
        currenthealth = get_database_value(bot, loser, 'health')
        if instigator == target:
            loser = targetname
        if currenthealth <= 0:
            if winner == loser:
                deathmsgb = suicidekill(bot,loser)
            else:
                deathmsgb = whokilledwhom(bot, winner, loser) or ''
            winnermsg = str(loser + ' dies forcing a respawn!!')
            if winner == instigator:
                assault_kills = assault_kills + 1
            else:
                assault_deaths = assault_deaths + 1
            combattextarraycomplete.append(winnermsg)
            if deathmsgb != '':
                combattextarraycomplete.append(deathmsgb)
        
        ## Chance that Instigator looses found loot
        if randominventoryfind == 'true' and target != bot.nick and instigator != target:
            lootwinnermsgb = ''
            ## Barbarians get a 50/50 chance of getting loot even if they lose
            loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
            barbarianstealroll = randint(0, 100)
            if loserclass == 'barbarian' and barbarianstealroll >= 50:
                lootwinnermsgb = str(loser + " steals the " + str(loot))
                lootwinner = loser
            elif winner == target:
                lootwinnermsgb = str(winner + " gains the " + str(loot))
                lootwinner = winner
            else:
                lootwinner = winner
            adjust_database_value(bot, lootwinner, loot, defaultadjust)
            if lootwinner == instigator:
                assault_potionswon = assault_potionswon + 1
            else:
                assault_potionslost = assault_potionslost + 1
            if lootwinnermsgb != '':
                combattextarraycomplete.append(lootwinnermsgb)

        ## Update XP points
        if yourclasswinner == 'ranger':
            XPearnedwinner = XPearnedwinnerranger
        else:
            XPearnedwinner = XPearnedwinnerstock
        if yourclassloser == 'ranger':
            XPearnedloser = XPearnedloserranger
        else:
            XPearnedloser = XPearnedloserstock
        if instigator != target:
            winnertier = get_database_value(bot, winner, 'levelingtier')
            losertier = get_database_value(bot, loser, 'levelingtier')
            xptier = tierratio_level(bot)
            if winnertier < currenttierstart:
                XPearnedwinner = XPearnedwinner * xptier
            if losertier < currenttierstart:
                XPearnedloser = XPearnedloser * xptier
            adjust_database_value(bot, winner, 'xp', XPearnedwinner)
            adjust_database_value(bot, loser, 'xp', XPearnedloser)
        
        ## new pepper level?
        instigatorpeppernow = get_pepper(bot, instigator)
        if instigatorpeppernow != instigatorpepperstart and instigator != target:
            pepperstatuschangemsg = str(instigator + " graduates to " + instigatorpeppernow + "! ")
            assault_levelups = assault_levelups + 1
            combattextarraycomplete.append(pepperstatuschangemsg)
        targetpeppernow = get_pepper(bot, target)
        if targetpeppernow != targetpepperstart and instigator != target:
            pepperstatuschangemsg = str(target + " graduates to " + targetpeppernow + "! ")
            combattextarraycomplete.append(pepperstatuschangemsg)
        
        ## Tier update
        tierchangemsg = ''
        currenttierend = get_database_value(bot, duelrecorduser, 'levelingtier') or 1
        if int(currenttierend) > int(currenttierstart):
            tierchangemsg = str("New Tier Unlocked!")
            if currenttierend != 1:
                newtierlistarray = []
                for x in tiercommandarray:
                    newtiereval = eval("tierunlock"+x)
                    if newtiereval == currenttierend:
                        newtierlistarray.append(x)
                if newtierlistarray != []:
                    newtierlist = get_trigger_arg(newtierlistarray, "list")
                    tierchangemsg = str(tierchangemsg + " Feature(s) now available: " + newtierlist)
                combattextarraycomplete.append(tierchangemsg)

        ## Magic Attributes text
        if instigator != target:
            magicattributestext = get_magic_attributes_text(bot, instigator, target, instigatorshieldstart, targetshieldstart, instigatorcursestart, targetcursestart)
            if magicattributestext and magicattributestext != '':
                combattextarraycomplete.append(magicattributestext)
                
        ## Special Event
        speceventtext = ''
        speceventtotal = get_database_value(bot, duelrecorduser, 'specevent') or 0
        if speceventtotal >= 49:
            set_database_value(bot, duelrecorduser, 'specevent', 1)
            speceventtext = str(instigator + " triggered the special event! Winnings are "+str(speceventreward)+" Coins!")
            adjust_database_value(bot, instigator, 'coin', speceventreward)
            combattextarraycomplete.append(speceventtext)
        else:
            adjust_database_value(bot, duelrecorduser, 'specevent', defaultadjust)

        ## Streaks Text
        streaktext = ''
        if instigator != target:
            streaktext = get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak) or ''
            if streaktext != '':
                combattextarraycomplete.append(streaktext)

        ## On Screen Text
        texttargetarray = []
        if OSDTYPE == 'say':
            texttargetarray.append(channel)
        elif OSDTYPE == 'notice':
            texttargetarray.append(instigator)
            texttargetarray.append(target)
        else:
            texttargetarray.append(instigator)
        onscreentext(bot, texttargetarray, combattextarraycomplete)
        
        ## update assault stats
        if winner == instigator:
            assault_wins = assault_wins + 1
            assault_damagedealt = assault_damagedealt + int(damage)
            assault_xp = assault_xp + XPearnedwinner
            if yourclasswinner == 'vampire':
                assault_damagetaken = assault_damagetaken - int(damage)
        if loser == instigator:
            assault_losses = assault_losses + 1
            assault_damagetaken = assault_damagetaken + int(damage)
            assault_xp = assault_xp + XPearnedloser

        ## Pause Between duels
        if typeofduel == 'assault':
            bot.notice("  ", instigator)
            time.sleep(5)
        
        ## Random Bonus
        if typeofduel == 'random' and winner == instigator:
            adjust_database_value(bot, winner, 'coin', randomcoinaward)
            
        ## End Of assault
        if typeofduel == 'assault':
            set_database_value(bot, target, 'lastfought', targetlastfoughtstart)
            if targetarraytotal == 0:
                bot.notice(instigator + ", It looks like the Full Channel Assault has completed.", instigator)
                for x in assaultstatsarray:
                    workingvar = eval("assault_"+x)
                    if workingvar > 0:
                        newline = str(x + " = " + str(workingvar))
                        if assaultdisplay != '':
                            assaultdisplay = str(assaultdisplay + " " + newline)
                        else:
                            assaultdisplay = str(newline)
                bot.say(instigator + "'s Full Channel Assault results: " + assaultdisplay)
                
## End Of Duels ###################################################################################################################

## 30 minute automation
@sopel.module.interval(1800)
def halfhourtimer(bot):
    now = time.time()
    
    ## Tier the stats
    tierratio = tierratio_level(bot)
    healthregencurrent = tierratio * healthregenmax
    magemanaregencurrent = tierratio * magemanaregenmax
    
    ## bot does not need stats or backpack items
    refreshbot(bot)
    
    ## Who gets to win a mysterypotion?
    randomuarray = []
    duelusersarray = get_database_value(bot, bot.nick, 'duelusers')
    
    for u in bot.users:
        ## must have duels enabled, but has to use the game every so often
        if u in duelusersarray and u != bot.nick:
            
            ## Log out users that aren't playing
            lastcommandusedtime = get_timesince_duels(bot, u, 'lastcommand') or 0
            lastping = get_timesince_duels(bot, u, 'lastping') or 0
            if AUTOLOGOUT < lastcommandusedtime and lastping < AUTOLOGOUT:
                adjust_database_array(bot, bot.nick, u, 'duelusers', 'del')
                reset_database_value(bot, u, 'lastping')
            else:  
                set_database_value(bot, u, 'lastping', now)
                
                healthcheck(bot, u)
                uclass = get_database_value(bot, u, 'class') or 'notclassy'
                mana = get_database_value(bot, u, 'mana') or 0
                health = get_database_value(bot, u, 'health') or 0
    
                ## Random user gets a mysterypotion
                lasttimedlootwinner = get_database_value(bot, duelrecorduser, 'lasttimedlootwinner') or bot.nick
                if u != lasttimedlootwinner:
                    randomuarray.append(u)

                ## award coin to all
                adjust_database_value(bot, u, 'coin', scavengercoinaward)

                ## health regenerates for all
                if int(health) < healthregencurrent:
                    adjust_database_value(bot, u, 'health', healthregen)
                    health = get_database_value(bot, u, 'health')
                    if int(health) > healthregencurrent:
                        set_database_value(bot, u, 'health', healthregencurrent)

                ## mages regen mana
                if uclass == 'mage':
                    if int(mana) < magemanaregencurrent:
                        adjust_database_value(bot, u, 'mana', magemanaregen)
                        mana = get_database_value(bot, u, 'mana')
                        if int(mana) > magemanaregencurrent:
                            set_database_value(bot, u, 'mana', magemanaregencurrent)

    if randomuarray != []:
        lootwinner = halfhourpotionwinner(bot, randomuarray)
        loot_text = str(mysterypotiondispmsg + " Use .duel loot use mysterypotion to consume.")
        adjust_database_value(bot, lootwinner, 'mysterypotion', defaultadjust)
        lootwinnermsg = str(lootwinner + ' is awarded a mysterypotion ' + str(loot_text))
        bot.notice(lootwinnermsg, lootwinner)

    ## bot does not need stats or backpack items
    refreshbot(bot)

## Functions ######################################################################################################################

######################
## Criteria to duel ##
######################

def mustpassthesetoduel(bot, trigger, instigator, target, dowedisplay):
    displaymsg = ''
    executedueling = 0
    instigatorclass = get_database_value(bot, instigator, 'class') or 'notclassy'
    if instigatorclass != 'knight':
        instigatorlastfought = get_database_value(bot, instigator, 'lastfought') or ''
    else:
        instigatorlastfought = bot.nick
    instigatortime = get_timesince_duels(bot, instigator, 'timeout') or ''
    targettime = get_timesince_duels(bot, target, 'timeout') or ''
    duelrecordusertime = get_timesince_duels(bot, duelrecorduser, 'timeout') or ''
    duelrecorduserlastinstigator = get_database_value(bot, duelrecorduser, 'lastinstigator') or bot.nick
    dueloptedinarray = get_database_value(bot, bot.nick, 'duelusers') or []
    totalduelusersarray = []
    for u in bot.users:
        if u in dueloptedinarray and u != bot.nick:
            totalduelusersarray.append(u)
    howmanyduelsers = len(totalduelusersarray)
    target = actualname(bot, target)
    if instigator == duelrecorduserlastinstigator and instigatortime <= INSTIGATORTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str("You may not instigate fights twice in a row within a half hour. You must wait for somebody else to instigate, or "+str(hours_minutes_seconds((INSTIGATORTIMEOUT - instigatortime)))+" .")
    elif target == instigatorlastfought and not bot.nick.endswith(devbot) and howmanyduelsers > 2:
        displaymsg = str(instigator + ', You may not fight the same person twice in a row.')
    elif instigator.lower() not in [x.lower() for x in dueloptedinarray]:
        displaymsg = str(instigator + ", It looks like you have disabled duels. Run .duel on to re-enable.")
    elif target.lower() not in [x.lower() for x in dueloptedinarray]:
        displaymsg = str(instigator + ', It looks like ' + target + ' has disabled duels.')
    elif instigatortime <= USERTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str("You can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - instigatortime)))+".")
    elif targettime <= USERTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str(target + " can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - targettime)))+".")
    elif duelrecordusertime <= CHANTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str("Channel can't duel for "+str(hours_minutes_seconds((CHANTIMEOUT - duelrecordusertime)))+".")
    else:
        displaymsg = ''
        executedueling = 1
    if dowedisplay:
        bot.notice(displaymsg, instigator)
    return executedueling

###########
## Names ##
###########

def nicktitles(bot, nick, channel):
    nickname = actualname(bot,nick)
    ## custom title
    nicktitle = get_database_value(bot, nick, 'title')
    ## bot.owner
    try:
        if nicktitle:
            nickname = str(nicktitle+" " + nickname)
        elif nick.lower() in bot.config.core.owner.lower():
            nickname = str("The Legendary " + nickname)
    ## botdevteam
        elif nick in botdevteam:
            nickname = str("The Extraordinary " + nickname)
    ## OP
        elif bot.privileges[channel.lower()][nick.lower()] == OP:
            nickname = str("The Magnificent " + nickname)
    ## VOICE
        elif bot.privileges[channel.lower()][nick.lower()] == VOICE:
            nickname = str("The Incredible " + nickname)
    ## bot.admin
        elif nick in bot.config.core.admins:
            nickname = str("The Spectacular " + nickname)
    ## else
        else:
            nickname = str(nickname)
    except KeyError:
        nickname = str(nickname)
    return nickname

def nickpepper(bot, nick, channel):
    pepperstart = get_pepper(bot, nick)
    if not pepperstart or pepperstart == '':
        nickname = "(n00b)"
    else:
        nickname = str("(" + pepperstart + ")")
    return nickname

def nickmagicattributes(bot, nick, channel):
    nickname = ''
    nickcurse = get_database_value(bot, nick, 'curse')
    nickshield = get_database_value(bot, nick, 'shield')
    magicattrarray = []
    if nickcurse:
        magicattrarray.append("[Cursed]")
    if nickshield:
        magicattrarray.append("[Shielded]")
    if nickname != []:
        for x in magicattrarray:
            if nickname != '':
                nickname = str(nickname + x)
            else:
                nickname = x
    return nickname

def nickarmor(bot, nick, channel):
    nickname = ''
    for x in armortypesarray:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            nickname = "{Armored}"
    return nickname

def actualname(bot,nick):
    actualnick = nick
    for u in bot.users:
        if u.lower() == nick.lower():
            actualnick = u
    return actualnick

##################
## Pepper level ##
##################

def get_pepper(bot, nick):
    tiernumber = 0
    nicktier = get_database_value(bot, nick, 'levelingtier')
    nickpepper = get_database_value(bot, nick, 'levelingpepper')
    currenttier = get_database_value(bot, duelrecorduser, 'levelingtier')
    xp = get_database_value(bot, nick, 'xp')
    if nick == bot.nick:
        pepper = 'Dragon Breath Chilli'
    elif not xp:
        pepper = ''
    elif xp > 0 and xp < 100:
        pepper = 'Pimiento'
        tiernumber = 1
    elif xp >= 100 and xp < 250:
        pepper = 'Sonora'
        tiernumber = 2
    elif xp >= 250 and xp < 500:
        pepper = 'Anaheim'
        tiernumber = 3
    elif xp >= 500 and xp < 1000:
        pepper = 'Poblano'
        tiernumber = 4
    elif xp >= 1000 and xp < 2500:
        pepper = 'Jalapeno'
        tiernumber = 5
    elif xp >= 2500 and xp < 5000:
        pepper = 'Serrano'
        tiernumber = 6
    elif xp >= 5000 and xp < 7500:
        pepper = 'Chipotle'
        tiernumber = 7
    elif xp >= 7500 and xp < 10000:
        pepper = 'Tabasco'
        tiernumber = 8
    elif xp >= 10000 and xp < 15000:
        pepper = 'Cayenne'
        tiernumber = 9
    elif xp >= 15000 and xp < 25000:
        pepper = 'Thai Pepper'
        tiernumber = 10
    elif xp >= 25000 and xp < 45000:
        pepper = 'Datil'
        tiernumber = 11
    elif xp >= 45000 and xp < 70000:
        pepper = 'Habanero'
        tiernumber = 12
    elif xp >= 70000 and xp < 100000:
        pepper = 'Ghost Chili'
        tiernumber = 13
    elif xp >= 100000 and xp < 250000:
        pepper = 'Mace'
        tiernumber = 14
    elif xp >= 250000:
        pepper = 'Pure Capsaicin'
        tiernumber = 15
    ## advance respawn tier
    if tiernumber > currenttier:
        set_database_value(bot, duelrecorduser, 'levelingtier', tiernumber)
    if tiernumber != nicktier:
        set_database_value(bot, nick, 'levelingtier', tiernumber)
    return pepper

def get_tierpepper(bot, tiernumber):
    if not tiernumber:
        pepper = ''
    elif tiernumber == 1:
        pepper = 'Pimiento'
    elif tiernumber == 2:
        pepper = 'Sonora'
    elif tiernumber == 3:
        pepper = 'Anaheim'
    elif tiernumber == 4:
        pepper = 'Poblano'
    elif tiernumber == 5:
        pepper = 'Jalapeno'
    elif tiernumber == 6:
        pepper = 'Serrano'
    elif tiernumber == 7:
        pepper = 'Chipotle'
    elif tiernumber == 8:
        pepper = 'Tabasco'
    elif tiernumber == 9:
        pepper = 'Cayenne'
    elif tiernumber == 10:
        pepper = 'Thai Pepper'
    elif tiernumber == 11:
        pepper = 'Datil'
    elif tiernumber == 12:
        pepper = 'Habanero'
    elif tiernumber == 13:
        pepper = 'Ghost Chili'
    elif tiernumber == 14:
        pepper = 'Mace'
    elif tiernumber == 15:
        pepper = 'Pure Capsaicin'
    else:
        pepper = ''
    return pepper

def get_peppertier(bot, pepper):
    if not pepper:
        tiernumber = 1
    elif pepper == 'pimiento':
        tiernumber = 1
    elif pepper == 'sonora':
        tiernumber = 2
    elif pepper == 'anaheim':
        tiernumber = 3
    elif pepper == 'poblano':
        tiernumber = 4
    elif pepper == 'jalapeno':
        tiernumber = 5
    elif pepper == 'serrano':
        tiernumber = 6
    elif pepper == 'chipotle':
        tiernumber = 7
    elif pepper == 'tabasco':
        tiernumber = 8
    elif pepper == 'cayenne':
        tiernumber = 9
    elif pepper == 'thai pepper':
        tiernumber = 10
    elif pepper == 'datil':
        tiernumber = 11
    elif pepper == 'habanero':
        tiernumber = 12
    elif pepper == 'ghost chili':
        tiernumber = 13
    elif pepper == 'mace':
        tiernumber = 14
    elif pepper == 'pure capsaicin':
        tiernumber = 15
    else:
        tiernumber = 1
    return tiernumber

######################
## On Screen Text ##
######################

def onscreentext(bot, texttargetarray, textarraycomplete):
    lastarray = 2
    textarraya = []
    textarrayb = []
    for x in textarraycomplete:
        if lastarray == 2:
            textarraya.append(x)
            lastarray = 1
        else:
            textarrayb.append(x)
            lastarray = 2
    if len(textarraya) > len(textarrayb):
        textarrayb.append("dummytext")
    for j, k in zip(textarraya, textarrayb):
        if k == "dummytext":
            k = ''
        combinedline = str(j + "   " + k)
        for user in texttargetarray:
            if user.startswith("#"):
                bot.msg(user, combinedline)
            else:
                bot.notice(combinedline, user)

###################
## Living Status ##
###################

def suicidekill(bot,loser):
    returntext = str(loser + " committed suicide ")
    ## Reset mana and health
    reset_database_value(bot, loser, 'mana')
    set_database_value(bot, loser, 'health', stockhealth)
    ## update deaths
    adjust_database_value(bot, loser, 'respawns', defaultadjust)
    loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
    ## bounty
    bountyonloser = get_database_value(bot, loser, 'bounty')
    if bountyonloser:
        returntext = str(returntext + "and wastes the bounty of " + str(bountyonloser) + " coin.")
    reset_database_value(bot, loser, 'bounty')
    ## rangers don't lose their stuff
    if loserclass != 'ranger':
        for x in lootitemsarray:
            reset_database_value(bot, loser, x)
    return returntext

def whokilledwhom(bot, winner, loser):
    returntext = ''
    ## Reset mana and health
    reset_database_value(bot, loser, 'mana')
    healthcheck(bot, loser)
    ## update kills/deaths
    adjust_database_value(bot, winner, 'kills', defaultadjust)
    adjust_database_value(bot, loser, 'respawns', defaultadjust)
    ## Loot Corpse
    loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
    bountyonloser = get_database_value(bot, loser, 'bounty')
    if bountyonloser:
        adjust_database_value(bot, winner, 'coin', bountyonloser)
        reset_database_value(bot, loser, 'bounty')
        returntext = str(winner + " wins a bounty of " + str(bountyonloser) + " that was placed on " + loser + ".")
    ## rangers don't lose their stuff
    if loserclass != 'ranger':
        for x in lootitemsarray:
            gethowmany = get_database_value(bot, loser, x)
            adjust_database_value(bot, winner, x, gethowmany)
            reset_database_value(bot, loser, x)
    return returntext

def healthcheck(bot, nick):
    health = get_database_value(bot, nick, 'health')
    if not health or health < 0:
        if nick != bot.nick:
            currenthealthtier = tierratio_level(bot)
            currenthealthtier = currenthealthtier * stockhealth
            set_database_value(bot, nick, 'health', currenthealthtier)
    ## no mana at respawn
    mana = get_database_value(bot, nick, 'mana')
    if int(mana) <= 0:
        reset_database_value(bot, nick, 'mana')
        
def refreshbot(bot):
    for x in duelstatsadminarray:
        statset = x
        reset_database_value(bot, bot.nick, x)
 
##########
## Time ##
##########

def get_timesince_duels(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))

def get_timeout(bot, nick):
    time_since = get_timesince_duels(bot, nick, 'timeout')
    if time_since < USERTIMEOUT:
        timediff = str(hours_minutes_seconds((USERTIMEOUT - time_since)))
    else:
        timediff = 0
    return timediff

def hours_minutes_seconds(countdownseconds):
    time = float(countdownseconds)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = ''
    timearray = ['hour','minute','second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg

#############
## Streaks ##
#############

def set_current_streaks(bot, nick, winlose):
    if winlose == 'win':
        beststreaktype = 'bestwinstreak'
        currentstreaktype = 'currentwinstreak'
        oppositestreaktype = 'currentlosestreak'
    elif winlose == 'loss':
        beststreaktype = 'worstlosestreak'
        currentstreaktype = 'currentlosestreak'
        oppositestreaktype = 'currentwinstreak'

    ## Update Current streak
    adjust_database_value(bot, nick, currentstreaktype, defaultadjust)
    set_database_value(bot, nick, 'currentstreaktype', winlose)

    ## Update Best Streak
    beststreak = get_database_value(bot, nick, beststreaktype) or 0
    currentstreak = get_database_value(bot, nick, currentstreaktype) or 0
    if int(currentstreak) > int(beststreak):
        set_database_value(bot, nick, beststreaktype, int(currentstreak))

    ## Clear current opposite streak
    reset_database_value(bot, nick, oppositestreaktype)

def get_current_streaks(bot, winner, loser):
    winner_loss_streak = get_database_value(bot, winner, 'currentlosestreak') or 0
    loser_win_streak = get_database_value(bot, loser, 'currentwinstreak') or 0
    return winner_loss_streak, loser_win_streak

def get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak):
    win_streak = get_database_value(bot, winner, 'currentwinstreak') or 0
    streak = ' (Streak: %d)' % win_streak if win_streak > 1 else ''
    broken_streak = ', recovering from a streak of %d losses' % winner_loss_streak if winner_loss_streak > 1 else ''
    broken_streak += ', ending %s\'s streak of %d wins' % (loser, loser_win_streak) if loser_win_streak > 1 else ''
    if broken_streak:
        streaktext = str("%s wins%s!%s" % (winner, broken_streak, streak))
    else:
        streaktext = ''
    return streaktext

###############
## Inventory ##
###############

def randominventory(bot, instigator):
    yourclass = get_database_value(bot, instigator, 'class') or 'notclassy'
    if yourclass == 'scavenger':
        randomfindchance = randint(scavegerfindpercent, 100)
    else:
        randomfindchance = randint(0, 120)
    randominventoryfind = 'false'
    if randomfindchance >= 90:
        randominventoryfind = 'true'
    return randominventoryfind

def halfhourpotionwinner(bot, randomuarray):
    winnerselectarray = []
    recentwinnersarray = get_database_value(bot, duelrecorduser, 'lasttimedlootwinners') or []
    lasttimedlootwinner = get_database_value(bot, duelrecorduser, 'lasttimedlootwinner') or bot.nick
    howmanyusers = len(randomuarray)
    if not howmanyusers > 1:
        reset_database_value(bot, duelrecorduser, 'lasttimedlootwinner')
    for x in randomuarray:
        if x not in recentwinnersarray and x != lasttimedlootwinner:
            winnerselectarray.append(x)
    if winnerselectarray == [] and randomuarray != []:
        reset_database_value(bot, duelrecorduser, 'lasttimedlootwinners')
        return halfhourpotionwinner(bot, randomuarray)
    lootwinner = get_trigger_arg(winnerselectarray, 'random') or bot.nick
    adjust_database_array(bot, duelrecorduser, lootwinner, 'lasttimedlootwinners', 'add')
    set_database_value(bot, duelrecorduser, 'lasttimedlootwinner', lootwinner)
    return lootwinner

######################
## Weapon Selection ##
######################

## allchan weapons
def getallchanweaponsrandom(bot):
    allchanweaponsarray = []
    for u in bot.users:
        weaponslist = get_database_value(bot, u, 'weaponslocker') or ['fist']
        for x in weaponslist:
            allchanweaponsarray.append(x)
    weapon = get_trigger_arg(allchanweaponsarray, 'random')
    return weapon

def weaponofchoice(bot, nick):
    weaponslistselect = []
    weaponslist = get_database_value(bot, nick, 'weaponslocker') or []
    lastusedweaponarry = get_database_value(bot, nick, 'lastweaponusedarray') or []
    lastusedweapon = get_database_value(bot, nick, 'lastweaponused') or 'fist'
    howmanyweapons = get_database_array_total(bot, nick, 'weaponslocker') or 0
    if not howmanyweapons > 1:
        reset_database_value(bot, nick, 'lastweaponused')
    for x in weaponslist:
        if len(x) > weaponmaxlength:
            adjust_database_array(bot, nick, x, 'weaponslocker', 'del')
        if x not in lastusedweaponarry and x != lastusedweapon and len(x) <= weaponmaxlength:
            weaponslistselect.append(x)
    if weaponslistselect == [] and weaponslist != []:
        reset_database_value(bot, nick, 'lastweaponusedarray')
        return weaponofchoice(bot, nick)
    weapon = get_trigger_arg(weaponslistselect, 'random') or 'fist'
    adjust_database_array(bot, nick, weapon, 'lastweaponusedarray', 'add')
    set_database_value(bot, nick, 'lastweaponused', weapon)
    return weapon

def weaponformatter(bot, weapon):
    if weapon == '':
        weapon = weapon
    elif weapon.lower().startswith(('a ', 'an ', 'the ')):
        weapon = str('with ' + weapon)
    elif weapon.split(' ', 1)[0].endswith("'s"):
        weapon = str('with ' + weapon)
    elif weapon.lower().startswith(('a', 'e', 'i', 'o', 'u')):
        weapon = str('with an ' + weapon)
    elif weapon.lower().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        if weapon.endswith('s'):
            weapon = str("with " + weapon)
        else:
            weapon = str("with " + weapon + "s")
    elif weapon.lower().startswith('with'):
        weapon = str(weapon)
    else:
        weapon = str('with a ' + weapon)
    return weapon

################
## Stat Reset ##
################

def statreset(bot, nick):
    now = time.time()
    getlastchanstatreset = get_database_value(bot, duelrecorduser, 'chanstatsreset')
    if not getlastchanstatreset:
        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
    getnicklastreset = get_database_value(bot, nick, 'chanstatsreset')
    if getnicklastreset < getlastchanstatreset:
        for x in duelstatsadminarray:
            reset_database_value(bot, nick, x)
        set_database_value(bot, nick, 'chanstatsreset', now)

################
## Tier ratio ##
################

def tierratio_level(bot):
    currenttier = get_database_value(bot, duelrecorduser, 'levelingtier')
    if not currenttier:
        tierratio = stocktierratio
    else:
        wordconvert = num2words(int(currenttier))
        tierratio = eval("tierratio"+ wordconvert)
    return tierratio

#################
## Damage Done ##
#################

def damagedone(bot, winner, loser, weapon, diaglevel):

    damagetextarray = []
    damagescale = tierratio_level(bot)
    winnerclass = get_database_value(bot, winner, 'class') or 'notclassy'
    loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
    shieldloser = get_database_value(bot, loser, 'shield') or 0
    shieldwinner = get_database_value(bot, winner, 'shield') or 0
    damagetext = ''
    
    ## names
    if winner == 'duelsroulettegame':
        winnername = loser
        losername = "themself"
        striketype = "shoots"
        bodypart = "head"
    elif winnerclass == 'knight' and diaglevel == 2:
        winnername = winner
        losername = loser
        striketype = "retaliates against"
        bodypart = get_trigger_arg(duelbodypartsarray, 'random')
    elif winner == loser:
        winnername = loser
        losername = "themself"
        striketype = get_trigger_arg(duelhittypesarray, 'random')
        bodypart = get_trigger_arg(duelbodypartsarray, 'random')
    else:
        winnername = winner
        losername = loser
        striketype = get_trigger_arg(duelhittypesarray, 'random')
        bodypart = get_trigger_arg(duelbodypartsarray, 'random')

    ## Armortype to check
    armortype = eval("armor"+bodypart)
    
    ## Rogue can't be hurt by themselves or bot
    roguearraynodamage = [bot.nick,loser]
    if loserclass == 'rogue' and winner in roguearraynodamage:
        damage = 0
    
    elif winner == 'duelsroulettegame':
        damage = randint(50, 120)
    
    ## Bot deals a set amount
    elif winner == bot.nick:
        damage = botdamage

    ## Barbarians get extra damage (minimum)
    elif winnerclass == 'barbarian':
        damage = randint(barbarianminimumdamge, 120)
    
    ## vampires have a minimum damage
    elif winnerclass == 'vampire' and winner != loser:
        damage = randint(0, vampiremaximumdamge)
    
    ## All Other Players
    else:
        damage = randint(0, 120)
       
    ## Damage Tiers
    if damage > 0:
        damage = damagescale * damage
        damage = int(damage)

    if damage == 0:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypart + weapon + ', but deals no damage. ')
    elif winnerclass == 'vampire' and winner != loser:
        damagetext = str(winnername + " drains " + str(damage)+ " health from " + losername + weapon + " in the " + bodypart + ". ")
    else:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypart + weapon + ", dealing " + str(damage) + " damage. ")
    damagetextarray.append(damagetext)
    
    ## Vampires gain health from wins
    if winnerclass == 'vampire' and winner != loser:
        adjust_database_value(bot, winner, 'health', damage)
        
    ## Berserker Rage
    if winnerclass == 'barbarian' and winner != loser:
        rageodds = randint(1, 12)
        if rageodds == 1:
            extradamage = randint(1, 25)
            damagetext = str(winner + " goes into Berserker Rage for an extra " + str(extradamage) + " damage.")
            damage = damage + extradamage
            damagetextarray.append(damagetext)
    
    ## Paladin deflect
    if loserclass == 'paladin' and damage > 0 and winner != 'duelsroulettegame' and winner != loser:
        deflectodds = randint(1, 12)
        if deflectodds == 1:
            damageb = damage
            damage = 0
            damagetext = str(damagetext + " "+ loser + " deflects the damage back on " + winner + ". ")
            damagemathb = int(shieldwinner) - damageb
            if int(damagemathb) > 0:
                adjust_database_value(bot, winner, 'shield', -abs(damageb))
                damageb = 0
                absorbedb = 'all'
            else:
                absorbedb = damagemathb + damageb
                damage = abs(damagemathb)
                reset_database_value(bot, loser, 'shield')
            damagetext = str(winner + " absorbs " + str(absorbedb) + " of the damage. ")
            damagetextarray.append(damagetext)
    
    ## Shield resistance
    if shieldloser and damage > 0 and winner != loser:
        damagemath = int(shieldloser) - damage
        if int(damagemath) > 0:
            adjust_database_value(bot, loser, 'shield', -abs(damage))
            damage = 0
            absorbed = 'all'
        else:
            absorbed = damagemath + damage
            damage = abs(damagemath)
            reset_database_value(bot, loser, 'shield')
        damagetext = str(loser + " absorbs " + str(absorbed) + " of the damage. ")
        damagetextarray.append(damagetext)

    ## Armor usage
    armorloser = get_database_value(bot, loser, armortype) or 0
    if armorloser and damage > 0 and winner != loser:
        adjust_database_value(bot, loser, armortype, -1)
        damagepercent = randint(1, armorhitpercentage) / 100
        damagereduced = damage * damagepercent
        damagereduced = int(damagereduced)
        damage = damage - damagereduced
        damagetext = str(loser + "s "+ armortype + " aleviated "+str(damagereduced)+" of the damage ")
        armorloser = get_database_value(bot, loser, armortype) or 0
        if armorloser <= 0:
            reset_database_value(bot, loser, armortype)
            damagetext = str(damagetext + ", causing the armor to break!")
        elif armorloser <= 5:
            damagetext = str(damagetext + ", causing the armor to be in need of repair!")
        else:
            damagetext = str(damagetext + ".")
        damagetextarray.append(damagetext)
    
    ## Knight
    if loserclass == 'knight' and diaglevel != 2 and winner != 'duelsroulettegame' and winner != loser:
        retaliateodds = randint(1, 12)
        if retaliateodds == 1:
            weaponb = weaponofchoice(bot, loser)
            weaponb = weaponformatter(bot, weaponb)
            weaponb = str(" "+ weaponb)
            damageb, damagetextb = damagedone(bot, loser, winner, weaponb, 2)
            for x in damagetextb:
                damagetextarray.append(x)
            
    ## dish it out
    if damage > 0:
        adjust_database_value(bot, loser, 'health', -abs(damage))
    
    return damage, damagetextarray

###################
## Select Winner ##
###################

def selectwinner(bot, nickarray):
    statcheckarray = ['health','xp','kills','respawns','currentwinstreak']

    ## empty var to start
    for user in nickarray:
        reset_database_value(bot, user, 'winnerselection')

    ## everyone gets a roll
    for user in nickarray:
        adjust_database_value(bot, user, 'winnerselection', 1)

    ## random roll
    randomrollwinner = get_trigger_arg(nickarray, 'random')
    adjust_database_value(bot, randomrollwinner, 'winnerselection', 1)

    ## Stats
    for x in statcheckarray:
        statscore = 0
        if x == 'respawns' or x == 'currentwinstreak':
            statscore = 99999999
        statleader = ''
        for u in nickarray:
            value = get_database_value(bot, u, x) or 0
            if x == 'respawns' or x == 'currentwinstreak':
                if int(value) < statscore:
                    statleader = u
                    statscore = int(value)
            else:
                if int(value) > statscore:
                    statleader = u
                    statscore = int(value)
        adjust_database_value(bot, statleader, 'winnerselection', 1)

    ## weaponslocker not empty
    for user in nickarray:
        weaponslist = get_database_value(bot, user, 'weaponslocker') or []
        if weaponslist != []:
            adjust_database_value(bot, user, 'winnerselection', 1)

    ## anybody rogue?
    for user in nickarray:
        nickclass = get_database_value(bot, user, 'class') or ''
        if nickclass == 'rogue':
            adjust_database_value(bot, user, 'winnerselection', 1)

    ## Dice rolling occurs now
    for user in nickarray:
        rolls = get_database_value(bot, user, 'winnerselection') or 0
        maxroll = winnerdicerolling(bot, user, rolls)
        set_database_value(bot, user, 'winnerselection', maxroll)

    ## curse check
    for user in nickarray:
        cursed = get_database_value(bot, user, 'curse') or 0
        if cursed:
            reset_database_value(bot, user, 'winnerselection')
            adjust_database_value(bot, user, 'curse', -1)

    ## who wins
    winnermax = 0
    winner = ''
    for u in nickarray:
        maxstat = get_database_value(bot, u, 'winnerselection') or 0
        if int(maxstat) > winnermax:
            winner = u
            winnermax = maxstat

    ## Clear value
    for user in nickarray:
        reset_database_value(bot, user, 'winnerselection')
    
    if not winner:
        for u in nickarray:
            maxroll = winnerdicerolling(bot, u, 2)
            set_database_value(bot, u, 'winnerselection', maxroll)
        winnermax = 0
        winner = ''
        for u in nickarray:
            maxstat = get_database_value(bot, u, 'winnerselection') or 0
            if int(maxstat) > winnermax:
                winner = u
                winnermax = maxstat
    
    return winner

def winnerdicerolling(bot, nick, rolls):
    nickclass = get_database_value(bot, nick, 'class') or ''
    rolla = 0
    rollb = 20
    if nickclass == 'rogue':
        rolla = 8
    fightarray = []
    while int(rolls) > 0:
        fightroll = randint(rolla, rollb)
        fightarray.append(fightroll)
        rolls = int(rolls) - 1
    try:
        fight = max(fightarray)
    except ValueError:
        fight = 0
    return fight

#####################
## Magic attributes ##
######################

def get_current_magic_attributes(bot, instigator, target):
    instigatorshield = get_database_value(bot, instigator, 'shield') or 0
    instigatorcurse = get_database_value(bot, instigator, 'curse') or 0
    targetshield = get_database_value(bot, target, 'shield') or 0
    targetcurse = get_database_value(bot, target, 'curse') or 0
    return instigatorshield, targetshield, instigatorcurse, targetcurse

def get_magic_attributes_text(bot, instigator, target, instigatorshieldstart, targetshieldstart, instigatorcursestart, targetcursestart):
    instigatorshieldnow, targetshieldnow, instigatorcursenow, targetcursenow = get_current_magic_attributes(bot, instigator, target)
    magicattributesarray = ['shield','curse']
    nickarray = ['instigator','target']
    attributetext = ''
    for j in nickarray:
        if j == 'instigator':
            scanningperson = instigator
        else:
            scanningperson = target
        for x in magicattributesarray:
            workingvarnow = eval(j+x+"now")
            workingvarstart = eval(j+x+"start")
            if workingvarnow == 0 and workingvarnow != workingvarstart:
                newline = str(scanningperson + " is no longer affected by " + x + ".")
                if attributetext != '':
                    attributetext = str(attributetext + " " + newline)
                else:
                    attributetext = str(newline)
    return attributetext

###############
## ScoreCard ##
###############

def get_winlossratio(bot,target):
    wins = get_database_value(bot, target, 'wins')
    wins = int(wins)
    losses = get_database_value(bot, target, 'losses')
    losses = int(losses)
    if not losses:
        if not wins:
            winlossratio = 0
        else:
            winlossratio = wins
    elif not wins:
        if not losses:
            winlossratio = 0
        else:
            winlossratio = int(losses) * -1
    else:
        winlossratio = float(wins)/losses
    return winlossratio

##############
## Database ##
##############

def get_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
def reset_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)

def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))

def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal

def adjust_database_array(bot, nick, entry, databasekey, adjustmentdirection):
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    reset_database_value(bot, nick, databasekey)
    adjustarray = []
    if adjustmentdirection == 'add':
        if entry not in adjustarraynew:
            adjustarraynew.append(entry)
    elif adjustmentdirection == 'del':
        if entry in adjustarraynew:
            adjustarraynew.remove(entry)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        reset_database_value(bot, nick, databasekey)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)

##########
## ARGS ##
##########

def get_trigger_arg(triggerargsarray, number):
    if number == 'create':
        triggerargsarraynew = []
        if triggerargsarray:
            for word in triggerargsarray.split():
                triggerargsarraynew.append(word)
        return triggerargsarraynew
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    triggerarg = ''
    if "^" in str(number) or number == 0 or str(number).endswith("+") or str(number).endswith("-") or str(number).endswith("<") or str(number).endswith(">"):
        if str(number).endswith("+"):
            rangea = re.sub(r"\+", '', str(number))
            rangea = int(rangea)
            rangeb = totalarray
        elif str(number).endswith("-"):
            rangea = 1
            rangeb = re.sub(r"-", '', str(number))
            rangeb = int(rangeb) + 1
        elif str(number).endswith(">"):
            rangea = re.sub(r">", '', str(number))
            rangea = int(rangea) + 1
            rangeb = totalarray
        elif str(number).endswith("<"):
            rangea = 1
            rangeb = re.sub(r"<", '', str(number))
            rangeb = int(rangeb)
        elif "^" in str(number):
            rangea = number.split("^", 1)[0]
            rangeb = number.split("^", 1)[1]
            rangea = int(rangea)
            rangeb = int(rangeb) + 1
        elif number == 0:
            rangea = 1
            rangeb = totalarray
        if rangea <= totalarray:
            for i in range(rangea,rangeb):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif number == 'last':
        if totalarray > 1:
            totalarray = totalarray -2
            triggerarg = str(triggerargsarray[totalarray])
    elif str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
        for i in range(1,totalarray):
            if int(i) != int(number):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif number == 'random':
        if totalarray > 1:
            try:
                shuffledarray = random.shuffle(triggerargsarray)
                randomselected = random.randint(0,len(shuffledarray) - 1)
                triggerarg = str(shuffledarray [randomselected])
            except TypeError:
                triggerarg = get_trigger_arg(triggerargsarray, 1)
        else:
            triggerarg = get_trigger_arg(triggerargsarray, 1)
    elif number == 'list':
        for x in triggerargsarray:
            if triggerarg != '':
                triggerarg  = str(triggerarg  + ", " + x)
            else:
                triggerarg  = str(x)
    else:
        number = int(number) - 1
        try:
            triggerarg = triggerargsarray[number]
        except IndexError:
            triggerarg = ''
    return triggerarg
