import sopel.module
from sopel.module import OP
from sopel.module import ADMIN
from sopel.module import VOICE
import sopel
from sopel import module, tools
import random
from random import randint
import time
import re
import sys
import os
from os.path import exists
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

## Configurables #############
defaultadjust = 1
TIMEOUT = 180
TIMEOUTC = 40
ALLCHAN = 'entirechannel'
OPTTIMEOUT = 1800
CLASSTIMEOUT = 86400
lootitemsarray = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion']
backpackarray = ['coins','healthpotion','manapotion','poisonpotion','timepotion','mysterypotion']
transactiontypesarray = ['buy','sell','trade','use']
challengestatsadminarray = ['shield','classtimeout','class','curse','bestwinstreak','worstlosestreak','opttime','coins','wins','losses','health','mana','healthpotion','mysterypotion','timepotion','respawns','xp','kills','timeout','disenable','poisonpotion','manapotion','lastfought','konami']
challengestatsarray = ['class','health','curse','shield','mana','xp','wins','losses','winlossratio','respawns','kills','backpackitems','lastfought','timeout']
classarray = ['barbarian','mage','scavenger','rogue','ranger']

####################
## Main Operation ##
####################

@sopel.module.commands('challenge','duel')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    
    ## Basic Vars that we will use
    instigator = trigger.nick
    inchannel = trigger.sender
    fullcommandused = get_trigger_arg(triggerargsarray, 0)
    commandortarget = get_trigger_arg(triggerargsarray, 1)
    for c in bot.channels:
        channel = c
    now = time.time()

    ## bot does not need stats or backpack items
    refreshbot(bot)
    
    ## If Not a target or a command used
    if not fullcommandused:
        bot.notice(instigator + ", Who did you want to challenge? Online Docs: https://github.com/deathbybandaid/sopel-modules/wiki/Challenges", instigator)
    
    ## Determine if the arg after .duel is a target or a command
    elif commandortarget.lower() not in bot.privileges[channel.lower()]:
        commandused = commandortarget
        target = get_trigger_arg(triggerargsarray, 2) or instigator
        targettext = get_trigger_arg(triggerargsarray, 2) or "that person"
        targetdisenable = get_database_value(bot, target, 'disenable')
        
        ## Arrays
        nontargetarray = ['info','shield','change','use','curse','list','everyone','reset','add','del','inv','health','attack','instakill','set','reset','lowest','highest','botadmin','random']
        adminonlyarray = ['statsadmin']
        privilegedarray = ['on','off']
        inchannelarray = ['random','everyone']
        
        ## Must clear these challenges to do the below functions
        if target.lower() not in bot.privileges[channel.lower()] and target not in transactiontypesarray and target not in lootitemsarray and target not in nontargetarray and commandused not in ['random','everyone','canifight'] and target != 'random' and not target.isdigit():
            bot.notice(instigator + ", It looks like " + targettext + " is either not here, or not a valid person.", instigator)
        elif not trigger.admin and commandused in adminonlyarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        elif target != instigator and not trigger.admin and commandused in privilegedarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        elif not targetdisenable and target != instigator and target not in lootitemsarray and target not in transactiontypesarray and commandused != 'on' and commandused != 'off' and target not in nontargetarray and commandused != 'random' and commandused != 'everyone' and commandused != 'statsadmin' and target != 'random':
            bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
        elif commandused in inchannelarray and not inchannel.startswith("#"):
            bot.notice(instigator + " Duels must be in channel.", instigator)
        elif target == bot.nick and not trigger.admin:
            bot.notice(instigator + " I cannot do that.", instigator)
            
        ## and, continue
        else:
            
            ## instigator
            lastfought = get_database_value(bot, instigator, 'lastfought')
            instigatortime = get_timesince_duels(bot, instigator, 'timeout')
            
            ## target
            if target not in nontargetarray:
                targetopttime = get_timesince_duels(bot, target, 'opttime')
                targettime = get_timesince_duels(bot, target, 'timeout')
            
            ## Channel
            channeltime = get_timesince_duels(bot, channel, 'timeout')
            channellastinstigator = get_database_value(bot, ALLCHAN, 'lastinstigator')
            lastfullroomassult = get_timesince_duels(bot, ALLCHAN, 'lastfullroomassult')
            lastfullroomassultinstigator = get_database_value(bot, ALLCHAN, 'lastfullroomassultinstigator')
            if not lastfullroomassultinstigator:
                lastfullroomassultinstigator = bot.nick
            if not channellastinstigator:
                channellastinstigator = bot.nick
            if not lastfought:
                lastfought = instigator
            targetarray = []
            displaymsg = ''
            dowedisplay = 0
            
            ## Random Target
            if target == 'random':
                for u in bot.channels[channel].users:
                    cantargetduel = mustpassthesetoduel(bot, trigger, instigator, u, inchannel, channel, dowedisplay)
                    if cantargetduel and target != bot.nick:
                        targetarray.append(u)
                if targetarray == []:
                    bot.notice(instigator + ", It looks like the random target finder has failed.", instigator)
                    target = instigator
                else:
                    randomselected = random.randint(0,len(targetarray) - 1)
                    target = str(targetarray [randomselected])
                    
            ## Docs
            if commandused == 'docs' or commandused == 'help':
                bot.notice("Online Docs: https://github.com/deathbybandaid/sopel-modules/wiki/Challenges", target)
            
            ## On/off
            elif commandused == 'on' or commandused == 'off':
                disenablevalue = ''
                if commandused == 'on':
                    disenablevalue = 1
                if target == 'everyone':
                    for u in bot.channels[channel].users:
                        set_database_value(bot, u, 'disenable', disenablevalue)
                elif targetopttime < OPTTIMEOUT and not bot.nick.endswith('dev'):
                    bot.notice(instigator + " It looks like " + target + " can't enable/disable challenges for %d seconds." % (OPTTIMEOUT - targetopttime), instigator)
                else:
                    if targetdisenable and commandused == 'on':
                        bot.notice(instigator + ", It looks like " + target + " already has duels on.", instigator)
                    elif not targetdisenable and commandused == 'off':
                        bot.notice(instigator + ", It looks like " + target + " already has duels off.", instigator)
                    else:
                        set_database_value(bot, target, 'disenable', disenablevalue)
                        set_database_value(bot, target, 'opttime', now)
                        bot.notice(instigator + ", It looks like Challenges should be " +  commandused + ' for ' + target + '.', instigator)
                        
            ## Random Dueling
            elif commandused == 'random':
                OSDTYPE = 'say'
                for u in bot.channels[channel].users:
                    cantargetduel = mustpassthesetoduel(bot, trigger, instigator, u, inchannel, channel, dowedisplay)
                    if cantargetduel:
                        targetarray.append(u)
                if targetarray == []:
                    targetarray.append(bot.nick)
                    targetarray.append(instigator)
                randomselected = random.randint(0,len(targetarray) - 1)
                target = str(targetarray [randomselected])
                return getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now, triggerargsarray)
                
            ## Duel Everyone
            elif commandused == 'everyone':
                OSDTYPE = 'notice'
                if lastfullroomassult < OPTTIMEOUT and not bot.nick.endswith('dev'):
                    bot.notice("Full Channel Assault can't be used for %d seconds." % (OPTTIMEOUT - lastfullroomassult), instigator)
                elif lastfullroomassultinstigator == instigator and not bot.nick.endswith('dev'):
                    bot.notice("You may not instigate a Full Channel Assault twice in a row.", instigator)
                else:
                    set_database_value(bot, ALLCHAN, 'lastfullroomassult', now)
                    set_database_value(bot, ALLCHAN, 'lastfullroomassultinstigator', instigator)
                    lastfoughtstart = get_database_value(bot, instigator, 'lastfought')
                    for u in bot.channels[channel].users:
                        cantargetduel = mustpassthesetoduel(bot, trigger, instigator, u, inchannel, channel, dowedisplay)
                        if cantargetduel and u != bot.nick:
                            targetarray.append(u)
                    if targetarray == []:
                        dowedisplay = 1
                        cantargetduel = mustpassthesetoduel(bot, trigger, instigator, instigator, inchannel, channel, dowedisplay)
                        if not cantargetduel:
                            bot.notice(instigator + ", It looks like you cannot challenge anybody at the moment.", instigator)
                    else:
                        for x in targetarray:
                            if x != instigator:
                                targetlastfoughtstart = get_database_value(bot, x, 'lastfought')
                                getreadytorumble(bot, trigger, instigator, x, OSDTYPE, channel, fullcommandused, now, triggerargsarray)
                                time.sleep(5)
                                bot.notice("  ", instigator)
                                set_database_value(bot, x, 'lastfought', targetlastfoughtstart)
                    set_database_value(bot, instigator, 'lastfought', lastfoughtstart)

            ## War Room
            elif commandused == 'warroom':
                subcommand = get_trigger_arg(triggerargsarray, 2)
                if not subcommand:
                    dowedisplay = 1
                    inchannel = "#bypass"
                    cantargetduel = mustpassthesetoduel(bot, trigger, instigator, instigator, inchannel, channel, dowedisplay)
                    if cantargetduel:
                        bot.notice(instigator + ", It looks like you can challenge.", instigator)
                elif subcommand == 'everyone':
                    if lastfullroomassultinstigator == instigator and not bot.nick.endswith('dev'):
                        bot.notice("You may not instigate an allchan duel twice in a row.", instigator)
                    elif lastfullroomassult < OPTTIMEOUT and not bot.nick.endswith('dev'):
                        bot.notice(" Full Channel Assault can't be used for %d seconds." % (OPTTIMEOUT - lastfullroomassult), instigator)
                    else:
                        bot.notice(" Full Channel Assault can be used.", instigator)
                elif subcommand == 'list':
                    targets = ''
                    for u in bot.channels[channel.lower()].users:
                        inchannel = "#bypass"
                        cantargetduel = mustpassthesetoduel(bot, trigger, instigator, u, inchannel, channel, dowedisplay)
                        if cantargetduel and u != bot.nick and u != instigator:
                            targetarray.append(u)
                    for x in targetarray:
                        if targets != '':
                            targets = str(targets + ", " + x)
                        else:
                            targets = str(x)
                    chunks = targets.split()
                    per_line = 15
                    targetline = ''
                    for i in range(0, len(chunks), per_line):
                        targetline = " ".join(chunks[i:i + per_line])
                        bot.say(str(targetline))
                    if targetline == '':
                        dowedisplay = 1
                        inchannel = "#bypass"
                        cantargetduel = mustpassthesetoduel(bot, trigger, instigator, instigator, inchannel, channel, dowedisplay)
                        if cantargetduel:
                            bot.notice(instigator + ", It looks like you can challenge.", instigator)
                        else:
                            bot.notice(instigator + ", It looks like you cannot challenge anybody at the moment.", instigator)
                elif target != instigator:
                    dowedisplay = 1
                    inchannel = "#bypass"
                    cantargetduel = mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay)
                    if cantargetduel:
                        bot.notice(instigator + ", It looks like you can challenge " + target + ".", instigator)

            ## Stats Admin
            elif commandused == 'statsadmin' and trigger.admin:
                statsadminarray = ['set','reset']
                if target in statsadminarray:
                    target = instigator
                    settype = get_trigger_arg(triggerargsarray, 2)
                    statset = get_trigger_arg(triggerargsarray, 3)
                    if settype == 'reset':
                        newvalue = ''
                    else:
                        newvalue = get_trigger_arg(triggerargsarray, 4)
                else:
                    settype = get_trigger_arg(triggerargsarray, 3)
                    statset = get_trigger_arg(triggerargsarray, 4)
                    if settype == 'reset':
                        newvalue = ''
                    else:
                        newvalue = get_trigger_arg(triggerargsarray, 5)
                if settype not in statsadminarray:
                    bot.notice(instigator + ", A correct command use is .duel statsadmin target set/reset stat", instigator)
                elif statset not in challengestatsadminarray and statset != 'all':
                    bot.notice(instigator + ", A correct command use is .duel statsadmin target set/reset stat", instigator)
                elif settype == 'set' and not newvalue:
                    bot.notice(instigator + ", A correct command use is .duel statsadmin target set/reset stat", instigator)
                else:
                    if target == 'everyone':
                        for u in bot.channels[channel].users:
                            if statset == 'all':
                                for x in challengestatsadminarray:
                                    set_database_value(bot, u, x, newvalue)
                            else:
                                set_database_value(bot, u, statset, newvalue)
                    else:
                        if statset == 'all':
                            for x in challengestatsadminarray:
                                set_database_value(bot, target, x, newvalue)
                        else:
                            set_database_value(bot, target, statset, newvalue)
                    bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
            
            ## Class
            elif commandused == 'class':
                classes = ''
                for x in classarray:
                    if classes != '':
                        classes = str(classes + ", " + x)
                    else:
                        classes = str(x)
                gethowmanycoins = get_database_value(bot, instigator, 'coins')
                yourclass = get_database_value(bot, instigator, 'class')
                yourclasstime = get_timesince_duels(bot, instigator, 'classtimeout')
                subcommand = get_trigger_arg(triggerargsarray, 2)
                subcommandarray = ['set','change']
                cost = 100
                if not yourclass and not subcommand:
                    bot.say("You don't appear to have a class set. Options are : " + classes +". Run .duel class set    to set your class.")
                elif not subcommand:
                    bot.say("Your class is currently set to " + str(yourclass))
                elif subcommand == 'info':
                    abilities = ''
                    setclass = get_trigger_arg(triggerargsarray, 3) or 'classless'
                    if setclass == 'barbarian':
                        abilities = "has a minimum damage of 40."
                    elif setclass == 'mage':
                        abilities = "has lower mana costs for magic."
                    elif setclass == 'scavenger':
                        abilities = "has a higher chance of finding loot in a duel, and is better at trading, buying, and selling."
                    elif setclass == 'rogue':
                        abilities = "does not take damage in fights against themself or the bot. Additionally, gains an advantage in winner selection."
                    elif setclass == 'ranger':
                        abilities = "gains XP at an accelerated rate and does not lose their backpack items upon death."
                    else:
                        abilities = "do not have any abilities."
                    bot.say('The ' + setclass + " " + abilities)
                elif yourclasstime < CLASSTIMEOUT and not bot.nick.endswith('dev'):
                    bot.say("You may not change your class more than once per day.")
                elif subcommand == 'set':
                    if yourclass:
                        bot.say("You appear to have a class set already. You can change your class for " + str(cost) + " coins. Run .duel class change    to set your class. Options are : " + classes +".")
                    else:
                        setclass = get_trigger_arg(triggerargsarray, 3)
                        if setclass not in classarray:
                            bot.say("Invalid class. Options are: " + classes +".")
                        else:
                            set_database_value(bot, instigator, 'class', setclass)
                            bot.say('Your class is now set to ' +  setclass)
                            set_database_value(bot, instigator, 'classtimeout', now)
                elif subcommand not in subcommandarray:
                    bot.say("Invalid command. Options are set or change.")
                elif subcommand == 'change':
                    if gethowmanycoins < cost:
                        bot.say("Changing class costs " + str(cost) + " coins.")
                    else:
                        setclass = get_trigger_arg(triggerargsarray, 3)
                        if setclass not in classarray:
                            bot.say("Invalid class. Options are: " + classes +".")
                        elif setclass == yourclass:
                            bot.say('Your class is already set to ' +  setclass)
                        else:
                            set_database_value(bot, instigator, 'class', setclass)
                            adjust_database_value(bot, instigator, 'coins', -abs(cost))
                            bot.say('Your class is now set to ' +  setclass)
                            set_database_value(bot, instigator, 'classtimeout', now)
                
            ## Streaks
            elif commandused == 'streaks':
                script = ''
                streak_type = get_database_value(bot, target, 'currentstreaktype')
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
                    script = str(script + "Currently on a " + typeofstreak + " streak of " + str(streak_count) + ".     ")
                if int(best_wins) > 1:
                    script = str(script + "Best Win streak= " + str(best_wins) + ".     ")
                if int(worst_losses) > 1:
                    script = str(script + "Worst Losing streak= " + str(worst_losses) + ".     ")
                if script == '':
                    bot.say(target + " has no streaks.")
                else:
                    bot.say(target + "'s streaks: " + script)
            
            ## Backpack
            elif commandused == 'backpack':
                stats = ''
                arraytoscan = backpackarray
                totalweapons = get_database_array_total(bot, target, 'weaponslocker')
                if totalweapons:
                    addstat = str(" weaponstotal" + "=" + str(totalweapons))
                    stats = str(stats + addstat)
                for x in arraytoscan:
                    gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        addstat = str(' ' + str(x) + "=" + str(gethowmany))
                        stats = str(stats + addstat)
                if stats != '':
                    stats = str(target + "'s " + commandused + ":" + stats)
                    bot.say(stats)
                else:
                    bot.say(instigator + ", It looks like " + target + " has no " +  commandused + ".", instigator)
            
            ## Stats
            elif commandused == 'stats':
                statsbypassarray = ['winlossratio','timeout']
                stats = ''
                arraytoscan = challengestatsarray
                for x in arraytoscan:
                    if x in statsbypassarray:
                        scriptdef = str('get_' + x + '(bot,target)')
                        gethowmany = eval(scriptdef)
                    else:
                        gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        addstat = str(' ' + str(x) + "=" + str(gethowmany))
                        stats = str(stats + addstat)
                if stats != '':
                    pepper = get_pepper(bot, target)
                    targetname = str("(" + str(pepper) + ") " + target)
                    stats = str(targetname + "'s " + commandused + ":" + stats)
                    bot.say(stats)
                else:
                    bot.say(instigator + ", It looks like " + target + " has no " +  commandused + ".", instigator)

            ## Leaderboard
            elif commandused == 'leaderboard':
                leaderboardscript = ''
                currentwlrleader = ''
                currentkillsleader = ''
                currentrespawnsleader = ''
                currenthealthleader = ''
                currentstreaksleader = ''
                currentwlrleadernumber = 0
                currentkillsleadernumber = 0
                currentrespawnsleadernumber = 0
                currenthealthleadernumber = 9999999999
                currentstreaksleadernumber = 0
                for u in bot.channels[channel].users:
                    targetdisenable = get_database_value(bot, u, 'disenable')
                    if targetdisenable and u != bot.nick:
                        winlossratio = get_winlossratio(bot,u)
                        if winlossratio > currentwlrleadernumber:
                            currentwlrleader = u
                            currentwlrleadernumber = winlossratio
                        kills = get_database_value(bot, u, 'kills')
                        if int(kills) > int(currentkillsleadernumber):
                            currentkillsleader = u
                            currentkillsleadernumber = int(kills)
                        respawns = get_database_value(bot, u, 'respawns')
                        if int(respawns) > int(currentrespawnsleadernumber):
                            currentrespawnsleader = u
                            currentrespawnsleadernumber = int(respawns)
                        health = get_database_value(bot, u, 'health')
                        if int(health) < int(currenthealthleadernumber) and int(health) != 0:
                            currenthealthleader = u
                            currenthealthleadernumber = int(health)
                        streaks = get_database_value(bot, u, 'bestwinstreak')
                        if int(streaks) > int(currentstreaksleadernumber):
                            currentstreaksleader = u
                            currentstreaksleadernumber = int(streaks)
                if currentwlrleadernumber > 0:
                    currentwlrleadernumber = format(currentwlrleadernumber, '.3f')
                    leaderboardscript = str(leaderboardscript + "Wins/Losses: " + currentwlrleader + " at " + str(currentwlrleadernumber) + ".     ")
                if currentkillsleadernumber > 0:
                    leaderboardscript = str(leaderboardscript + "Top Killer: " + currentkillsleader + " with " + str(currentkillsleadernumber) + " kills.     ")
                if currentrespawnsleadernumber > 0:
                    leaderboardscript = str(leaderboardscript + "Top Killed: " + currentrespawnsleader + " with " + str(currentrespawnsleadernumber) + " respawns.     ")
                if currenthealthleadernumber > 0:
                    leaderboardscript = str(leaderboardscript + "Closest To Death: " + currenthealthleader + " with " + str(currenthealthleadernumber) + " health.     ")
                if currentstreaksleadernumber > 0:
                    leaderboardscript = str(leaderboardscript + "Best Win Streak: " + currentstreaksleader + " with " + str(currentstreaksleadernumber) + ".     ")
                if leaderboardscript == '':
                    leaderboardscript = str("Leaderboard appears to be empty")
                bot.say(leaderboardscript)

            ## Loot Items
            elif commandused == 'loot':
                yourclass = get_database_value(bot, instigator, 'class') or 'notclassy'
                lootcommand = get_trigger_arg(triggerargsarray, 2)
                lootitem = get_trigger_arg(triggerargsarray, 3)
                lootitemb = get_trigger_arg(triggerargsarray, 4)
                lootitemc = get_trigger_arg(triggerargsarray, 5)
                gethowmanylootitem = get_database_value(bot, instigator, lootitem)
                gethowmanycoins = get_database_value(bot, instigator, 'coins')
                if lootcommand not in transactiontypesarray:
                    bot.notice(instigator + ", Do you want to buy, sell, trade, or use?", instigator)
                elif not lootitem:
                    bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
                elif lootitem not in lootitemsarray:
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif lootcommand == 'use':
                    if lootitemb.isdigit():
                        quantity = int(lootitemb)
                        target = instigator
                    elif lootitemb == 'all':
                        target = instigator
                        quantity = gethowmanylootitem
                    elif not lootitemb:
                        quantity = 1
                        target = instigator
                    else:
                        target = lootitemb
                        if not lootitemc:
                            quantity = 1
                        elif lootitemc == 'all':
                            quantity = gethowmanylootitem
                        else:
                            quantity = int(lootitemc)
                    if gethowmanylootitem < quantity:
                        bot.notice(instigator + ", You do not have enough " +  lootitem + " to use this command!", instigator)
                    elif target.lower() not in bot.privileges[channel.lower()]:
                        bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                    else:   
                        if int(quantity) == 1:
                            saymsg = 'true'
                            use_lootitem(bot, instigator, target, inchannel, lootitem, saymsg)
                        elif lootitem == 'mysterypotion' and int(quantity) > 1 and inchannel.startswith("#"):
                            bot.notice(instigator + ", Multiple mysterypotions must be used in privmsg.", instigator)
                        else:
                            saymsg = 'false'
                            if lootitem == 'mysterypotion' or not inchannel.startswith("#"):
                                saymsg = 'true'
                            while int(quantity) > 0:
                                quantity = int(quantity) - 1
                                use_lootitem(bot, instigator, target, inchannel, lootitem, saymsg)
                            bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)
                elif lootcommand == 'trade':
                    quantity = lootitemc
                    if not quantity:
                        quantity = 1
                    if yourclass == 'scavenger':
                        quantitymath = 2 * int(quantity)
                    else:
                        quantitymath = 3 * int(quantity)
                    if lootitemb not in lootitemsarray:
                        bot.notice(instigator + ", You can't trade for the same type of potion.", instigator)
                    elif lootitemb not in lootitemsarray:
                        bot.notice(instigator + ", Invalid loot item.", instigator)
                    elif lootitemb == lootitem:
                        bot.notice(instigator + ", You can't trade for the same type of potion.", instigator)
                    elif gethowmanylootitem < quantitymath:
                        bot.notice(instigator + ", You don't have enough of this item to trade.", instigator)
                    else:
                        while int(quantity) > 0:
                            quantity = int(quantity) - 1
                            if yourclass == 'scavenger':
                                cost = -2
                            else:
                                cost = -3
                            reward = 1
                            itemtoexchange = lootitem
                            itemexchanged = lootitemb
                            adjust_database_value(bot, instigator, itemtoexchange, cost)
                            adjust_database_value(bot, instigator, itemexchanged, reward)
                        bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)
                elif lootcommand == 'buy':
                    quantity = lootitemb
                    if not quantity:
                        quantity = 1
                    elif quantity == 'all':
                        quantity = 99999999999999999
                    if yourclass == 'scavenger':
                        coinsrequired = 90 * int(quantity)
                    else:
                        coinsrequired = 100 * int(quantity)
                    if gethowmanycoins < coinsrequired:
                        bot.notice(instigator + ", You do not have enough coins for this action.", instigator)
                    else:
                        while int(quantity) > 0:
                            quantity = int(quantity) - 1
                            if yourclass == 'scavenger':
                                cost = -90
                            else:
                                cost = -100
                            reward = 1
                            itemtoexchange = 'coins'
                            itemexchanged = lootitem
                            adjust_database_value(bot, instigator, itemtoexchange, cost)
                            adjust_database_value(bot, instigator, itemexchanged, reward)
                        bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)
                elif lootcommand == 'sell':
                    quantity = lootitemb
                    if not quantity:
                        quantity = 1
                    elif quantity == 'all':
                        quantity = gethowmanylootitem
                    if int(quantity) > gethowmanylootitem:
                        bot.notice(instigator + ", You do not have enough " + lootitem + " for this action.", instigator)
                    else:
                        while int(quantity) > 0:
                            quantity = int(quantity) - 1
                            cost = -1
                            if yourclass == 'scavenger':
                                reward = 30
                            else:
                                reward = 25
                            itemtoexchange = lootitem
                            itemexchanged = 'coins'
                            adjust_database_value(bot, instigator, itemtoexchange, cost)
                            adjust_database_value(bot, instigator, itemexchanged, reward)
                        bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)

            ## Konami
            elif commandused == 'upupdowndownleftrightleftrightba':
                konami = get_database_value(bot, target, 'konami')
                if not konami:
                    set_database_value(bot, instigator, 'konami', 1)
                    bot.notice(instigator + " you have found the cheatcode easter egg!!!", instigator)
                    damage = 600
                    adjust_database_value(bot, target, 'health', damage)
                else:
                    bot.notice(instigator + " you can only cheat once.", instigator)
                
            ## Weaponslocker
            elif commandused == 'weaponslocker':
                validdirectionarray = ['inv','add','del','reset']
                if target in validdirectionarray:
                    target = instigator
                    adjustmentdirection = get_trigger_arg(triggerargsarray, 2)
                    weaponchange = get_trigger_arg(triggerargsarray, '3+')
                else:
                    adjustmentdirection = get_trigger_arg(triggerargsarray, 3)
                    weaponchange = get_trigger_arg(triggerargsarray, '4+')
                weaponslist = get_database_value(bot, target, 'weaponslocker') or []
                if not adjustmentdirection:
                    bot.say('Use .duel weaponslocker add/del to adjust Locker Inventory.')
                elif adjustmentdirection == 'inv':
                    weapons = ''
                    for x in weaponslist:
                        weapon = x
                        if weapons != '':
                            weapons = str(weapons + ", " + weapon)
                        else:
                            weapons = str(weapon)
                    chunks = weapons.split()
                    per_line = 15
                    weaponline = ''
                    for i in range(0, len(chunks), per_line):
                        weaponline = " ".join(chunks[i:i + per_line])
                        bot.notice(str(weaponline), instigator)
                    if weaponline == '':
                        bot.say('There doesnt appear to be anything in the weapons locker! Use .duel weaponslocker add/del to adjust Locker Inventory.')
                elif target != instigator and not trigger.admin:
                    bot.say("You may not adjust somebody elses locker.")
                elif adjustmentdirection == 'reset':
                    set_database_value(bot, target, 'weaponslocker', '')
                    bot.say('Locker Reset.')
                else:
                    if not weaponchange:
                        bot.say("What weapon would you like to add/remove?")
                    else:
                        if weaponchange in weaponslist and adjustmentdirection == 'add':
                            weaponlockerstatus = 'already'
                        elif weaponchange not in weaponslist and adjustmentdirection == 'del':
                            weaponlockerstatus = 'already not'
                        else:
                            if adjustmentdirection == 'add':
                                weaponlockerstatus = 'now'
                            elif adjustmentdirection == 'del':
                                weaponlockerstatus = 'no longer'
                            adjust_database_array(bot, target, weaponchange, 'weaponslocker', adjustmentdirection)
                        message = str(weaponchange + " is " + weaponlockerstatus + " in weapons locker.")
                        bot.say(message)
        
            ## Magic Attack
            elif commandused == 'magic':
                magicoptions = ['attack','instakill','health','curse','shield']
                magicusage = get_trigger_arg(triggerargsarray, 2)
                if magicusage not in magicoptions:
                    bot.say('Magic uses include: attack, instakill, health, curse')
                else:
                    target = get_trigger_arg(triggerargsarray, 3)
                    if not target:
                        target = trigger.nick
                    targetcurse = get_curse_check(bot, target)
                    targetshield = get_curse_check(bot, target)
                    mana = get_database_value(bot, instigator, 'mana')
                    if magicusage == 'attack':
                        manarequired = 250
                        damage = -200
                    elif magicusage == 'shield':
                        manarequired = 500
                        damage = 80
                    elif magicusage == 'curse':
                        manarequired = 500
                        damage = -80
                    elif magicusage == 'health':
                        manarequired = 200
                        damage = 200
                    elif magicusage == 'instakill':
                        targethealthstart = get_database_value(bot, target, 'health')
                        targethealthstart = int(targethealthstart)
                        if int(targethealthstart) < 200:
                            manarequired = 200
                        else:
                            manarequired = targethealthstart / 200
                            manarequired = manarequired * 250
                        damage = -abs(targethealthstart)
                    damagetext = abs(damage)
                    yourclass = get_database_value(bot, instigator, 'class') or 'notclassy'
                    if yourclass == 'mage':
                        manarequired = manarequired * .9
                    manarequired = -abs(manarequired)
                    if not mana:
                        bot.notice(instigator + " you don't have any mana.", instigator)
                    elif mana < manarequired:
                        manamath = int(manarequired - mana)
                        bot.notice(instigator + " you need " + str(manamath) + " more mana to do this attack.", instigator)
                    elif magicusage == 'curse' and targetcurse:
                        bot.notice(instigator + " it looks like " + target + " is already cursed.", instigator)
                    elif magicusage == 'shield' and targetshield:
                        bot.notice(instigator + " it looks like " + target + " is already shielded.", instigator)
                    else:
                        if target.lower() not in bot.privileges[channel.lower()]:
                            bot.say("I'm not sure who that is.")
                        elif target == bot.nick:
                            bot.say("I am immune to that kind of attack.")
                        else:
                            targethealthstart = get_database_value(bot, target, 'health')
                            adjust_database_value(bot, instigator, 'mana', manarequired)
                            adjust_database_value(bot, target, 'health', damage)
                            targethealth = get_database_value(bot, target, 'health')
                            if targethealth <= 0:
                                whokilledwhom(bot, instigator, target)
                                magicsay = str(instigator + ' uses magic on ' + target + ', killing ' + target)
                                magicnotice = str(instigator + " used a magic on you that killed you")
                            elif magicusage == 'curse':
                                curseduration = 4
                                magicsay = str(instigator + " uses magic on " + target + ", dealing " + str(damagetext) + " damage AND forces " + target + " to lose the next " + str(curseduration) + " duels.")
                                magicnotice = str(instigator + " uses magic on " + target + ", dealing " + str(damagetext) + " damage AND forces " + target + " to lose the next " + str(curseduration) + " duels.")
                                set_database_value(bot, target, 'curse', curseduration)
                            elif magicusage == 'shield':
                                shieldduration = 4
                                magicsay = str(instigator + " uses magic on " + target + ", restoring " + str(damagetext) + " health AND allows " + target + " to take no damage for the next " + str(shieldduration) + " duels.")
                                magicnotice = str(instigator + " uses magic on " + target + ", restoring " + str(damagetext) + " health AND allows " + target + " to take no damage for the next " + str(shieldduration) + " duels.")
                                set_database_value(bot, target, 'shield', shieldduration)
                            elif magicusage == 'health':
                                healthmath = int(int(targethealth) - int(targethealthstart))
                                magicsay = str(instigator + ' uses magic on ' + target + ' that increased health by ' + str(healthmath))
                                magicnotice = str(instigator + " used a magic on you that increased health by " + str(healthmath))
                            else:
                                magicsay = str(instigator + ' uses magic on ' + target + ', dealing ' + str(damagetext) + ' damage.')
                                magicnotice = str(instigator + ' uses magic on ' + target + ', dealing ' + str(damagetext) + ' damage.')
                            bot.say(str(magicsay))
                            if not inchannel.startswith("#") and target != instigator:
                                bot.notice(str(magicnotice), target)
                    mana = get_database_value(bot, instigator, 'mana')
                    if mana <= 0:
                        set_database_value(bot, instigator, 'mana', '')
                                
            else:
                bot.notice(instigator + ", It looks like that is either not here, or not a valid person.", instigator)
    else:
        OSDTYPE = 'say'
        target = get_trigger_arg(triggerargsarray, 1)
        dowedisplay = 1
        executedueling = mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay)
        if executedueling:
            return getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now, triggerargsarray)
    
    ## bot does not need stats or backpack items
    refreshbot(bot)
        
def getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now, triggerargsarray):
    
    ## Update Time Of Combat
    set_database_value(bot, instigator, 'timeout', now)
    set_database_value(bot, target, 'timeout', now)
    set_database_value(bot, ALLCHAN, 'timeout', now)
    
    ## Naming and Initial pepper level
    instigatorname, instigatorpepperstart = whatsyourname(bot, trigger, instigator, channel)
    if instigator == target:
        targetname = "themself"
        targetpepperstart = ''
    else:
        targetname, targetpepperstart = whatsyourname(bot, trigger, target, channel)

    ## Announce Combat
    announcecombatmsg = str(instigatorname + " versus " + targetname)
       
    ## Check for new player health
    healthcheck(bot, instigator)
    healthcheck(bot, target)

    ## Manual weapon
    weapon = get_trigger_arg(triggerargsarray, '2+')
    if not weapon:
        manualweapon = 'false'
    else:
        manualweapon = 'true'
        if weapon == 'all':
            weapon = getallchanweaponsrandom(bot, channel)
        elif weapon == 'target':
            weapon = weaponofchoice(bot, target)
            weapon = str(target + "'s " + weapon)
        
    ## Select Winner
    winner, loser = getwinner(bot, instigator, target, manualweapon)
    
    ## Damage Done (random)
    damage = damagedone(bot, winner, loser)
    
    ## Streaks A
    winner_loss_streak, loser_win_streak = get_streaktexta(bot, winner, loser)
    
    ## Weapon Select
    if manualweapon == 'false' or winner == target:
        if winner == bot.nick:
            weapon = ''
        else:
            weapon = weaponofchoice(bot, winner)
    weapon = weaponformatter(bot, weapon)
    if weapon != '':
        weapon = str(" " + weapon)
        
    ## Update Wins and Losses
    if instigator != target:
        adjust_database_value(bot, winner, 'wins', defaultadjust)
        adjust_database_value(bot, loser, 'losses', defaultadjust)
        set_current_streaks(bot, winner, 'win')
        set_current_streaks(bot, loser, 'loss')
            
    ## Update XP points
    yourclasswinner = get_database_value(bot, winner, 'class') or 'notclassy'
    if yourclasswinner == 'ranger':
        XPearnedwinner = '7'
    else:
        XPearnedwinner = '5'
    yourclassloser = get_database_value(bot, loser, 'class') or 'notclassy'
    if yourclassloser == 'ranger':
        XPearnedloser = '5'
    else:
        XPearnedloser = '3'
    if instigator != target:
        adjust_database_value(bot, winner, 'xp', XPearnedwinner)
        adjust_database_value(bot, loser, 'xp', XPearnedloser)
                
    ## Update last fought
    if instigator != target:
        set_database_value(bot, instigator, 'lastfought', target)
        set_database_value(bot, target, 'lastfought', instigator)
    
    ## Same person can't instigate twice in a row
    set_database_value(bot, ALLCHAN, 'lastinstigator', instigator)
            
    ## Update Health Of Loser, respawn, allow winner to loot
    yourclass = get_database_value(bot, loser, 'class') or 'notclassy'
    if yourclass == 'rogue':
        if instigator == target or target == bot.nick:
            damage = 0
    adjust_database_value(bot, loser, 'health', damage)
    damage = abs(damage)
    currenthealth = get_database_value(bot, loser, 'health')
    if currenthealth <= 0:
        whokilledwhom(bot, winner, loser)
        if instigator == target:
            loser = targetname
        winnermsg = str(winner + ' killed ' + loser + weapon + ' forcing a respawn!!')
    else:
        if instigator == target:
            loser = targetname
        winnermsg = str(winner + " hits " + loser + weapon + ', dealing ' + str(damage) + ' damage.')
        
    ## new pepper level?
    pepperstatuschangemsg = ''
    instigatorpeppernow = get_pepper(bot, instigator)
    targetpeppernow = get_pepper(bot, target)
    if instigatorpeppernow != instigatorpepperstart and instigator != target:
        pepperstatuschangemsg = str(pepperstatuschangemsg + instigator + " graduates to " + instigatorpeppernow + "! ")
    if targetpeppernow != targetpepperstart and instigator != target:
        pepperstatuschangemsg = str(pepperstatuschangemsg + target + " graduates to " + targetpeppernow + "! ")
            
    ## Random Inventory gain
    lootwinnermsg = ''
    lootwinnermsgb = ''
    randominventoryfind = randominventory(bot, instigator)
    if randominventoryfind == 'true' and target != bot.nick and instigator != target:
        loot = determineloottype(bot, winner)
        loot_text = get_lootitem_text(bot, winner, loot)
        adjust_database_value(bot, winner, loot, defaultadjust)
        lootwinnermsg = str(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
        if winner == target:
            lootwinnermsgb = str(winner + " gains the " + str(loot))
    
    # Streaks B
    if instigator != target:
        streaktext = get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak) or ''
        if streaktext != '':
            streaktext = str(str(streaktext) + "       ")
    else:
        streaktext = ''
    
    ## On Screen Text
    if OSDTYPE == 'say':
        bot.say(str(announcecombatmsg) + "       " + str(lootwinnermsg))
        bot.say(str(winnermsg)+ "       " + str(lootwinnermsgb))
        if instigatorpeppernow != instigatorpepperstart or targetpeppernow != targetpepperstart or streaktext:
            bot.say(str(streaktext) + str(pepperstatuschangemsg))
    elif OSDTYPE == 'notice':
        bot.notice(str(announcecombatmsg) + "       " + str(lootwinnermsg), winner)
        bot.notice(str(announcecombatmsg) + "       " + str(lootwinnermsg), loser)
        bot.notice(str(winnermsg)+ "       " + str(lootwinnermsgb), winner)
        bot.notice(str(winnermsg)+ "       " + str(lootwinnermsgb), loser)
        if instigatorpeppernow != instigatorpepperstart or targetpeppernow != targetpepperstart or streaktext:
            bot.notice(str(streaktext) + str(pepperstatuschangemsg), winner)
            bot.notice(str(streaktext) + str(pepperstatuschangemsg), loser)
    else:
        bot.say('Looks Like Something went wrong!')
        
        
## 30 minute automation
# health regen
# mysterypotion
# reset last instigator
@sopel.module.interval(1800)
def healthregen(bot):
    
    ## bot does not need stats or backpack items
    for x in challengestatsadminarray:
        statset = x
        if statset != 'disenable':
            set_database_value(bot, bot.nick, x, '')
    
    ## Clear Last Instigator
    set_database_value(bot, ALLCHAN, 'lastinstigator', '')
    
    ## Who gets to win a mysterypotion?
    randomtargetarray = []
    lasttimedlootwinner = get_database_value(bot, ALLCHAN, 'lasttimedlootwinner')
    if not lasttimedlootwinner:
        lasttimedlootwinner = bot.nick
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            target = u
            targetdisenable = get_database_value(bot, target, 'disenable')
            if targetdisenable and target != lasttimedlootwinner and target != bot.nick:
                health = get_database_value(bot, target, 'health')
                if health < 500:
                    adjust_database_value(bot, target, 'health', '50')
                randomtargetarray.append(target)
        if randomtargetarray == []:
            dummyvar = 1
        else:
            randomselected = random.randint(0,len(randomtargetarray) - 1)
            target = str(randomtargetarray [randomselected])
            loot = 'mysterypotion'
            loot_text = get_lootitem_text(bot, target, loot)
            adjust_database_value(bot, target, loot, defaultadjust)
            lootwinnermsg = str(target + ' is awarded a ' + str(loot) + ' ' + str(loot_text))
            bot.notice(lootwinnermsg, target)
            set_database_value(bot, ALLCHAN, 'lasttimedlootwinner', target)
            
        
## Functions######################################################################################################################

######################
## Criteria to duel ##
######################

def mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay):
    executedueling = 0
    lastfought = get_database_value(bot, instigator, 'lastfought') or ''
    targetspicebotdisenable = get_botdatabase_value(bot, target, 'disenable') or ''
    instigatordisenable = get_database_value(bot, instigator, 'disenable') or ''
    targetdisenable = get_database_value(bot, target, 'disenable') or ''
    instigatortime = get_timesince_duels(bot, instigator, 'timeout') or ''
    targettime = get_timesince_duels(bot, target, 'timeout') or ''
    channeltime = get_timesince_duels(bot, ALLCHAN, 'timeout') or ''
    channellastinstigator = get_database_value(bot, ALLCHAN, 'lastinstigator') or ''
    if not channellastinstigator:
        channellastinstigator = bot.nick
    
    if not inchannel.startswith("#"):
        displaymsg = str(instigator + " Duels must be in channel.")
    elif target == bot.nick and not targetdisenable:
        displaymsg = str(instigator + " I refuse to fight a biological entity!")
    elif instigator == channellastinstigator and not bot.nick.endswith('dev'):
        displaymsg = str(instigator + ', You may not instigate fights twice in a row within a half hour.')
    elif target == lastfought and not bot.nick.endswith('dev'):
        displaymsg = str(instigator + ', You may not fight the same person twice in a row.')
    elif not targetspicebotdisenable and target != bot.nick:
        displaymsg = str(instigator + ', It looks like ' + target + ' has disabled ' + bot.nick + "." )
    elif not instigatordisenable:
        displaymsg = str(instigator + ", It looks like you have disabled Challenges. Run .challenge on to re-enable.")
    elif not targetdisenable:
        displaymsg = str(instigator + ', It looks like ' + target + ' has disabled Challenges.')
    elif instigatortime <= TIMEOUT and not bot.nick.endswith('dev'):
        displaymsg = str("You can't challenge for %d seconds." % (TIMEOUT - instigatortime))
    elif targettime <= TIMEOUT and not bot.nick.endswith('dev'):
        displaymsg = str(target + " can't challenge for %d seconds." % (TIMEOUT - targettime))
    elif channeltime <= TIMEOUTC and not bot.nick.endswith('dev'):
        displaymsg = str(channel + " can't challenge for %d seconds." % (TIMEOUTC - channeltime))
    else:
        displaymsg = ''
        executedueling = 1
    if dowedisplay:
        bot.notice(displaymsg, instigator)
    return executedueling

##############
## Database ##
##############

def get_database_value(bot, nick, databasekey):
    databasecolumn = str('challenges_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('challenges_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey)
    databasecolumn = str('challenges_' + databasekey)
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
    set_database_value(bot, nick, databasekey, '')
    adjustarray = []
    if adjustmentdirection == 'add':
        adjustarraynew.append(entry)
    elif adjustmentdirection == 'del':
        adjustarraynew.remove(entry)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        set_database_value(bot, nick, databasekey, '')
    else:
        set_database_value(bot, nick, databasekey, adjustarray)
    
###################
## Living Status ##
###################

def whokilledwhom(bot, winner, loser):
    ## Reset mana and health
    set_database_value(bot, loser, 'mana', '')
    set_database_value(bot, loser, 'health', '1000')
    ## update kills/deaths
    adjust_database_value(bot, winner, 'kills', defaultadjust)
    adjust_database_value(bot, loser, 'respawns', defaultadjust)
    ## Loot Corpse
    yourclass = get_database_value(bot, loser, 'class') or 'notclassy'
    if yourclass != 'ranger':
        for x in lootitemsarray:
            gethowmany = get_database_value(bot, loser, x)
            adjust_database_value(bot, winner, x, gethowmany)
            set_database_value(bot, loser, x, '')

def healthcheck(bot, nick):
    health = get_database_value(bot, nick, 'health')
    if not health and nick != bot.nick:
        set_database_value(bot, nick, 'health', '1000')

def refreshbot(bot):
    set_database_value(bot, bot.nick, 'disenable', '1')
    for x in challengestatsadminarray:
        statset = x
        if statset != 'disenable':
            set_database_value(bot, bot.nick, x, '')
            
##########
## Time ##
##########
    
def get_timesince_duels(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))

def get_timeout(bot, nick):
    time_since = get_timesince_duels(bot, nick, 'timeout')
    if time_since < TIMEOUT:
        timediff = int(TIMEOUT - time_since)
    else:
        timediff = 0
    return timediff

###########
## Names ##
###########

def whatsyourname(bot, trigger, nick, channel):
    nickname = str(nick)
    
    ## Pepper Level
    pepperstart = get_pepper(bot, nick)
    
    ## Is user Special?
    botownerarray = []
    operatorarray = []
    voicearray = []
    adminsarray = []
    for u in bot.channels[channel.lower()].users:
        nametargetdisenable = get_database_value(bot, u, 'disenable')
        if u != bot.nick and nametargetdisenable:
            nametarget = u
            if nametarget.lower() in bot.config.core.owner.lower():
                botownerarray.append(nametarget)
            if bot.privileges[channel.lower()][nametarget] == OP:
                operatorarray.append(nametarget)
            if bot.privileges[channel.lower()][nametarget.lower()] == VOICE:
                voicearray.append(nametarget)
            if nametarget in bot.config.core.admins:
                adminsarray.append(nametarget)
    
    ## Is nick Special?
    if nick in botownerarray:
        nickname = str("The Legendary " + nickname)
    elif nick in operatorarray:
        nickname = str("The Magnificent " + nickname)
    elif nick in voicearray:
        nickname = str("The Incredible " + nickname)
    elif nick in adminsarray:
        nickname = str("The Extraordinary " + nickname)
    else:
        nickname = str(nickname)
        
    ## Pepper Names
    if pepperstart != '':
        nickname = str(nickname + " (" + pepperstart + ")")
    else:
        nickname = str(nickname + " (n00b)")
    
    return nickname, pepperstart
    
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
    set_database_value(bot, nick, oppositestreaktype, '')
    
    
def get_currentstreak(bot, nick):
    streaks = ''
    for x in streaksarray:
        streak = get_database_value(bot, nick, x) or 0
        if streak:
            addstreak = str(str(x) + " = " + str(streak))
            if streaks != '':
                streaks = str(str(streaks) + str(addstreak))
            else:
                streaks = str(str(streaks) + ' ' + str(addstreak))
    return streaks
    
def get_streaktexta(bot, winner, loser):
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

def get_backpackitems(bot, target):
    totalbackpack = 0
    for x in lootitemsarray:
        gethowmany = get_database_value(bot, target, x)
        totalbackpack = int(int(totalbackpack) + int(gethowmany))
    return totalbackpack

def randominventory(bot, instigator):
    yourclass = get_database_value(bot, instigator, 'class') or 'notclassy'
    if yourclass == 'scavenger':
        randomfindchance = randint(40, 120)
    else:
        randomfindchance = diceroll(120)
    randominventoryfind = 'false'
    if randomfindchance >= 90:
        randominventoryfind = 'true'
    return randominventoryfind

def determineloottype(bot, nick):
    loot = random.randint(0,len(lootitemsarray) - 1)
    loot = str(lootitemsarray [loot])
    return loot

def get_lootitem_text(bot, nick, loottype):
    if loottype == 'healthpotion':
        loot_text = ': worth 100 health.'
    elif loottype == 'poisonpotion':
        loot_text = ': worth -50 health.'
    elif loottype == 'manapotion':
        loot_text = ': worth 100 mana.'
    elif loottype == 'timepotion':
        loot_text = ': worth up to ' + str(TIMEOUT) + ' seconds of timeout.'
    elif loottype == 'mysterypotion':
        loot_text = ': With unknown effects!'
    else:
        loot_text = ''
    if loot_text != '':
        loot_text = str(loot_text + " Use .challenge loot use " + str(loottype) + " to consume.")
    return loot_text
        
def use_lootitem(bot, instigator, target, inchannel, loottype, saymsg):
    targethealth = get_database_value(bot, target, 'health')
    if not targethealth:
        set_database_value(bot, target, 'health', '1000')
        targethealth = get_database_value(bot, target, 'health')
    gethowmany = get_database_value(bot, target, 'mana')
    adjust_database_value(bot, instigator, loottype, -1)
    mana = get_database_value(bot, target, 'mana')
    if target == instigator:
        mainlootusemessage = str(instigator + ' uses ' + loottype + '.')
    else:
        mainlootusemessage = str(instigator + ' uses ' + loottype + ' on ' + target + ". ")
    if loottype == 'healthpotion':
        adjust_database_value(bot, target, 'health', '100')
    elif loottype == 'poisonpotion':
        yourclass = get_database_value(bot, target, 'class') or 'notclassy'
        if yourclass != 'rogue':
            adjust_database_value(bot, target, 'health', '-50')
    elif loottype == 'manapotion':
        adjust_database_value(bot, target, 'mana', '100')
    elif loottype == 'timepotion':
        channellastinstigator = get_database_value(bot, ALLCHAN, 'lastinstigator')
        if not channellastinstigator:
            channellastinstigator = bot.nick
        if channellastinstigator == target:
            set_database_value(bot, ALLCHAN, 'lastinstigator', '')
        set_database_value(bot, target, 'timeout', '')
        set_database_value(bot, ALLCHAN, 'timeout', '')
    elif loottype == 'mysterypotion':
        loot = random.randint(0,len(lootitemsarray) - 1)
        loot = str(lootitemsarray [loot])
        if loot != 'mysterypotion':
            adjust_database_value(bot, instigator, loot, defaultadjust)
            saymsg = 'false'
            use_lootitem(bot, instigator, target, inchannel, loot, saymsg)
            saymsg = 'true'
            lootusemsg = str("a " + loot)
        else:
            nulllootitemsarray = ['water','vinegar','mud']
            nullloot = random.randint(0,len(nulllootitemsarray) - 1)
            nullloot = str(nulllootitemsarray [nullloot])
            lootusemsg = str("just " + str(nullloot) + ' after all.')
        mainlootusemessage = str(mainlootusemessage + ' It was ' + str(lootusemsg))
    else:
        mainlootusemessage = str(mainlootusemessage + '')
    targethealth = get_database_value(bot, target, 'health')
    if targethealth <= 0:
        mainlootusemessage = str(mainlootusemessage + "This resulted in death.")
        whokilledwhom(bot, instigator, target)
    if saymsg == 'true':
        bot.say(str(mainlootusemessage))
        if not inchannel.startswith("#") and target != instigator:
            bot.notice(str(mainlootusemessage), target)
    
######################
## Weapon Selection ##
######################

## allchan weapons
def getallchanweaponsrandom(bot, channel):
    allchanweaponsarray = []
    for u in bot.channels[channel].users:
        weaponslist = get_database_value(bot, u, 'weaponslocker') or []
        if weaponslist != []:
            for x in weaponslist:
                allchanweaponsarray.append(x)
    if allchanweaponsarray == []:
        weapon = "fist"
    else:
        weaponselected = random.randint(0,len(allchanweaponsarray) - 1)
        weapon = str(allchanweaponsarray [weaponselected])
    return weapon
        
## Hacky Patch to move weaponslocker to new database setup
def weaponsmigrate(bot, nick):
    weaponslistnew = []
    weaponslist = bot.db.get_nick_value(nick, 'weapons_locker') or []
    if weaponslist or weaponslist != []:
        for x in weaponslist:
            weaponslistnew.append(x)
        set_database_value(bot, nick, 'weaponslocker', weaponslistnew)
        bot.db.set_nick_value(nick, 'weapons_locker', '')

def weaponofchoice(bot, nick):
    weaponslistselect = []
    weaponslist = get_database_value(bot, nick, 'weaponslocker') or []
    lastusedweapon = get_database_value(bot, nick, 'lastweaponused')
    if not lastusedweapon:
        lastusedweapon = "fist"
    if weaponslist == []:
        weapon = "fist"
    else:
        for x in weaponslist:
            if x != lastusedweapon:
                weaponslistselect.append(x)
        if weaponslistselect == []:
            weapon = lastusedweapon
        else:
            weaponselected = random.randint(0,len(weaponslistselect) - 1)
            weapon = str(weaponslistselect [weaponselected])
    set_database_value(bot, nick, 'lastweaponused', weapon)
    return weapon

def weaponformatter(bot, weapon):
    if weapon == '':
        weapon = weapon
    elif weapon.lower().startswith('a ') or weapon.lower().startswith('an ') or weapon.lower().startswith('the '):
        weapon = str('with ' + weapon)
    elif weapon.split(' ', 1)[0].endswith("'s"):
        weapon = str('with ' + weapon)
    elif weapon.lower().startswith('a') or weapon.lower().startswith('e') or weapon.lower().startswith('i') or weapon.lower().startswith('o') or weapon.lower().startswith('u'):
        weapon = str('with an ' + weapon)
    elif weapon.lower().startswith('with'):
        weapon = str(weapon)
    else:
        weapon = str('with a ' + weapon)
    return weapon

#################
## Damage Done ##
#################

def damagedone(bot, winner, loser):
    shieldwinner = get_shield_check(bot, winner)
    shieldloser = get_shield_check(bot, loser)
    yourclass = get_database_value(bot, winner, 'class') or 'notclassy'
    if winner == bot.nick:
        rando = 150
    elif yourclass == 'barbarian':
        rando = randint(40, 120)
    else:
        rando = randint(0, 120)
    if shieldloser:
        damage = 0
    else:
        damage = -abs(rando)
    return damage

##################
## Pepper level ##
##################

def get_pepper(bot, nick):
    xp = get_database_value(bot, nick, 'xp')
    nickcurse = get_database_value(bot, nick, 'curse')
    if nick == bot.nick:
        pepper = 'Dragon Breath Chilli'
    elif nickcurse:
        pepper = 'Cursed'
    elif not xp:
        pepper = ''
    elif xp > 0 and xp < 100:
        pepper = 'Pimiento'
    elif xp >= 100 and xp < 250:
        pepper = 'Sonora'
    elif xp >= 250 and xp < 500:
        pepper = 'Anaheim'
    elif xp >= 500 and xp < 1000:
        pepper = 'Poblano'
    elif xp >= 1000 and xp < 2500:
        pepper = 'Jalapeno'
    elif xp >= 2500 and xp < 5000:
        pepper = 'Serrano'
    elif xp >= 5000 and xp < 7500:
        pepper = 'Chipotle'
    elif xp >= 7500 and xp < 10000:
        pepper = 'Tabasco'
    elif xp >= 10000 and xp < 15000:
        pepper = 'Cayenne'
    elif xp >= 15000 and xp < 25000:
        pepper = 'Thai Pepper'
    elif xp >= 25000 and xp < 45000:
        pepper = 'Datil'
    elif xp >= 45000 and xp < 70000:
        pepper = 'Habanero'
    elif xp >= 70000 and xp < 100000:
        pepper = 'Ghost Chili'
    elif xp >= 100000 and xp < 250000:
        pepper = 'Mace'
    elif xp >= 250000:
        pepper = 'Pure Capsaicin'
    return pepper

###################
## Select Winner ##
###################

def getwinner(bot, instigator, target, manualweapon):
    
    ## each person gets one diceroll
    instigatorfight = 1
    targetfight = 1
    
    instigatoryourclass = get_database_value(bot, instigator, 'class') or ''
    if instigatoryourclass == 'rogue':
        instigatorfight = instigatorfight + 1
    targetyourclass = get_database_value(bot, instigator, 'class') or ''
    if targetyourclass == 'rogue':
        targetfight = targetfight + 1
    
    ## Random Number
    flip = randint(0, 1)
    if flip == 0:
        instigatorfight = instigatorfight + 1
    else:
        targetfight = targetfight + 1
    
    # Most Health Extra roll
    instigatorhealth = get_database_value(bot, instigator, 'health')
    targethealth = get_database_value(bot, target, 'health')
    if int(instigatorhealth) > int(targethealth):
        instigatorfight = instigatorfight + 1
    elif int(instigatorhealth) < int(targethealth):
        targetfight = targetfight + 1
    
    # Most XP gets an extra roll
    instigatorxp = get_database_value(bot, instigator, 'xp')
    targetxp = get_database_value(bot, target, 'xp')
    if int(instigatorxp) > int(targetxp):
        instigatorfight = instigatorfight + 1
    elif int(instigatorxp) < int(targetxp):
        targetfight = targetfight + 1
    
    ## More Kills Gets an extra roll
    instigatorkills = get_database_value(bot, instigator, 'kills')
    targetkills = get_database_value(bot, target, 'kills')
    if int(instigatorkills) > int(targetkills):
        instigatorfight = instigatorfight + 1
    elif int(instigatorkills) < int(targetkills):
        targetfight = targetfight + 1
        
    ## Least Respawns Gets an extra roll
    instigatorrespawns = get_database_value(bot, instigator, 'respawns')
    targetrespawns = get_database_value(bot, target, 'respawns')
    if int(instigatorrespawns) < int(targetrespawns):
        instigatorfight = instigatorfight + 1
    elif int(instigatorrespawns) > int(targetrespawns):
        targetfight = targetfight + 1
    
    # extra roll for using the weaponslocker or manual weapon usage
    instigatorweaponslist = get_database_value(bot, instigator, 'weaponslocker') or []
    targetweaponslist = get_database_value(bot, target, 'weaponslocker') or []
    if instigatorweaponslist != [] or manualweapon == 'true':
        instigatorfight = instigatorfight + 1
    if targetweaponslist != []:
        targetfight = targetfight + 1
    
    ## Dice Roll (instigator d20, target d19)
    instigatorfightarray = []
    targetfightarray = []
    while int(instigatorfight) > 0:
        instigatorfightroll = diceroll(20)
        instigatorfightarray.append(instigatorfightroll)
        instigatorfight = int(instigatorfight) - 1
    instigatorfight = max(instigatorfightarray)
    while int(targetfight) > 0:
        if targetyourclass == 'rogue':
            targetfightroll = diceroll(21)
        else:
            targetfightroll = diceroll(19)
        targetfightarray.append(targetfightroll)
        targetfight = int(targetfight) - 1
    targetfight = max(targetfightarray)

    ## check for curses
    if instigator != target and instigator != bot.nick:
        instigatorcurse = get_curse_check(bot, instigator)
        if instigatorcurse:
            instigatorfight = 0
        targetcurse = get_curse_check(bot, target)
        if targetcurse:
            targetfight = 0

    ## tie breaker
    if instigatorfight == targetfight:
        tiebreaker = randint(0, 1)
        if (tiebreaker == 0):
            instigatorfight = int(instigatorfight) + 1
        else:
            targetfight = int(targetfight) + 1
    
    ## Compare
    if int(instigatorfight) > int(targetfight):
        winner = instigator
    else:
        winner = target
        
    ## LOSER IS NOT WINNER
    if target == bot.nick:
        winner = bot.nick
        loser = instigator
    elif winner == instigator:
        loser = target
    else:
        loser = instigator
    return winner, loser

############
## cursed ##
############

def get_curse_check(bot, nick):
    adjustment = -1
    cursed = 0
    nickcurse = get_database_value(bot, nick, 'curse')
    if nickcurse:
        adjust_database_value(bot, nick, 'curse', adjustment)
        cursed = 1
    return cursed

############
## shield ##
############

def get_shield_check(bot, nick):
    adjustment = -1
    shield = 0
    nickshield = get_database_value(bot, nick, 'shield')
    if nickshield:
        adjust_database_value(bot, nick, 'shield', adjustment)
        shield = 1
    return shield
    
###############
## ScoreCard ##
###############

def get_winlossratio(bot,target):
    wins = get_database_value(bot, target, 'wins')
    wins = int(wins)
    losses = get_database_value(bot, target, 'losses')
    losses = int(losses)
    if not wins or not losses:
        winlossratio = 0
    else:
        winlossratio = float(wins)/losses
    return winlossratio

###########
## Tools ##
###########

def diceroll(howmanysides):
    diceroll = randint(0, howmanysides)
    return diceroll

## Triggerargs

#def create_args_array(fullstring):
#    triggerargsarray = []
#    if fullstring:
#        for word in fullstring.split():
#            triggerargsarray.append(word)
#    return triggerargsarray

#def get_trigger_arg(triggerargsarray, number):
#    number = number - 1
#    try:
#        triggerarg = triggerargsarray[number]
#    except IndexError:
#        triggerarg = ''
#    return triggerarg
