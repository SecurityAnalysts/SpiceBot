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
from difflib import SequenceMatcher

## not needed if using without spicebot
#shareddir = os.path.dirname(os.path.dirname(__file__)) ## not needed if using without spicebot
#sys.path.append(shareddir) ## not needed if using without spicebot
#from SpicebotShared import * ## not needed if using without spicebot

###################
## Configurables ##
###################

## Command Structure
commandarray_instigator_bypass = ['on','admin','devmode','game'] ## bypass for Opt status
commandarray_admin = ['admin','devmode','game'] ## Admin Functions
commandarray_inchannel = ['roulette','assault','colosseum','bounty','hungergames','devmode'] ## Must Be inchannel
### Alternative Commands
commandarray_alt_on = ['enable','activate']
commandarray_alt_off = ['disable','deactivate']
commandarray_alt_random = ['anyone','somebody','available','someone']
commandarray_alt_assault = ['everyone','everybody']
commandarray_alt_author = ['credit']
commandarray_alt_docs = ['help','man']
### Command Tiers
commandarray_tier_self = ['stats', 'loot', 'streaks']
commandarray_tier_unlocks_0 = ['tier','game', 'docs', 'admin', 'author', 'on', 'off','health','devmode','version'] ## move health to self later
commandarray_tier_unlocks_1 = ['usage']
commandarray_tier_unlocks_2 = ['streaks', 'bounty', 'harakiri']
commandarray_tier_unlocks_3 = ['weaponslocker', 'class']
commandarray_tier_unlocks_4 = ['leaderboard', 'warroom']
commandarray_tier_unlocks_5 = ['stats', 'loot']
commandarray_tier_unlocks_6 = ['magic', 'armor']
commandarray_tier_unlocks_7 = ['assault']
commandarray_tier_unlocks_8 = ['roulette']
commandarray_tier_unlocks_9 = ['random']
commandarray_tier_unlocks_10 = ['colosseum']
commandarray_tier_unlocks_11 = ['title']
commandarray_tier_unlocks_12 = ['mayhem']
commandarray_tier_unlocks_13 = ['hungergames']
commandarray_tier_unlocks_14 = []
commandarray_tier_unlocks_15 = []

## Tiers, XP, Pepper levels
commandarray_xp_levels = [0,1,100,250,500,1000,2500,5000,7500,10000,15000,25000,45000,70000,100000,250000] ## XP
commandarray_tier_ratio = [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.1,2.2,2.3,2.4,2.5] ## Tier Ratios
commandarray_pepper_levels = ['n00b','pimiento','sonora','anaheim','poblano','jalapeno','serrano','chipotle','tabasco','cayenne','thai pepper','datil','habanero','ghost chili','mace','pure capsaicin'] ## Pepper Levels
commandarray_tier_display_exclude = ['admin','game','devmode','version'] ## Do NOT display

## more stuff
bodyparts_required = ['torso','head']

## Admin Stats Cycling
stats_admin_types = ['healthbodyparts','armor','loot','record','magic','streak','timeout','class','title','bounty','weaponslocker','leveling','other']
## Health Stats
stats_healthbodyparts = ['head','chest','health_left_arm','right_arm','left_leg','right_leg','junk']
## Armor Stats
stats_armor = ['helmet','breastplate','left_gauntlet','right_gauntlet','left_greave','right_greave','codpiece']
## Loot Stats
stats_loot = ['magicpotion','healthpotion','mysterypotion','timepotion','poisonpotion','manapotion','grenade','coin']
## Record Stats
stats_record = ['wins','losses','xp','respawns','kills','lastfought']
## Streak Stats
stats_streak = ['streak_loss_current','streak_win_current','streak_type_current','streak_win_best','streak_loss_best']
## Magic Stats
stats_magic = ['mana','curse','shield']
## Timeout Stats
stats_timeout = ['timeout_class','timeout_opttime','timeout_timeout']
## Class Stats
stats_class = ['class_setting','class_freebie','class_timeout']
## Title Stats
stats_title = ['title_setting']
## Bounty Stats
stats_bounty = ['bounty']
## Weaponslocker Stats
stats_weaponslocker = ['weaponslocker_complete','weaponslocker_lastweaponusedarray','weaponslocker_lastweaponused']
## Leveling Stats
stats_leveling = ['tier']
## Other
stats_other = ['chanstatsreset']

## Documentation and Development
GITWIKIURL = "https://github.com/deathbybandaid/SpiceBot/wiki/Duels" ## Wiki URL, change if not using with spicebot
development_team = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score'] ## Dev Team

## On/off
timeout_opt = 1800 ## Time between opting in and out of the game - Half hour

## Roulette
roulette_death_timeout = 86400
timeout_roulette = 5
roulette_payout_default = 5
roulette_revolver_list = ['.357 Magnum','Colt PeaceMaker','Colt Repeater','Colt Single Action Army 45','Ruger Super Blackhawk','Remington Model 1875','Russian Nagant M1895 revolver','Smith and Wesson Model 27']

## Assault
timeout_assault = 1800 ## Time Between Full Channel Assaults
assault_results = ['wins','losses','potionswon','potionslost','kills','deaths','damagetaken','damagedealt','levelups','xp']

## Colosseum
timeout_colosseum = 1800 ## Time Between colosseum events

## hungergames
timeout_hungergames = 1800

## mayhem
timeout_mayhem = 1800

## Random Target
random_payout = 100

## Class
class_array = ['blacksmith','barbarian','mage','scavenger','rogue','ranger','fiend','vampire','knight','paladin'] ## Valid Classes
timeout_class = 86400 ## Time between changing class - One Day
class_cost = 100 ## ## how many coin to change class

## Title
title_cost = 100 ## ## how many coin to change title

## Bug Bounty
bugbounty_reward = 100 ## users that find a bug in the code, get a reward

## Loot
loot_view = ['coin','grenade','healthpotion','manapotion','poisonpotion','timepotion','mysterypotion','magicpotion'] ## how to organize backpack
potion_types = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion','magicpotion'] ## types of potions
loot_transaction_types = ['buy','sell','trade','use'] ## valid commands for loot
### Buy
loot_buy = 100 ## normal cost to buy a loot item
loot_buy_scavenger = 80 ## cost to buy a loot item for scavengers
### Sell
loot_sell = 25 ## normal coin rewarded in selling loot
loot_sell_scavenger = 40 ## coin rewarded in selling loot for scavengers
### Trade
loot_trade = 3 ## normal trading ratio 3:1
loot_trade_scavenger = 2 ## scavengers can trade at a 2:1 ratio
### Grenades
grenade_full_damage = 100
grenade_secondary_damage = 50
### Health Potions
healthpotion_worth = 100 ## normal health potion worth
healthpotion_worth_barbarian = 125 ## health potion worth for barbarians
healthpotiondispmsg = str(": worth " + str(healthpotion_worth) + " health.")
### Mana Potions
manapotion_worth = 100 ##normal mana potion worth
manapotion_worth_mage = 125 ## manapotion worth for mages
manapotiondispmsg = str(": worth " + str(manapotion_worth) + " mana.")
### Poison Potions
poisonpotion_worth = -50 ## poisonpotion damage
poisonpotiondispmsg = str(": worth " + str(poisonpotion_worth) + " health.")
### Mystery Potions
mysterypotiondispmsg = str(": The label fell off. Use at your own risk!")
loot_null = ['water','vinegar','mud']
### Time Potions
timepotiondispmsg = str(": Removes multiple timeouts.")
timepotiontargetarray = ['lastinstigator','lastfullroomcolosseuminstigator','lastfullroomassultinstigator']
timepotiontimeoutarray = ['timeout_timeout','lastfullroomcolosseum','lastfullroomassult','timeout_opttime','class_timeout']
## Magic Potions
magicpotiondispmsg = str(": Not consumable, sellable, or purchasable. Trade this for the potion you want!")

## Weapons Locker
weapon_name_length = 70 ## prevents text that destroys OSD

## Magic
magic_types = ['curse','shield']
magic_usage_mage = .9 ## mages only need 90% of the mana requirements below
magic_mana_required_shield = 300 ## mana required for magic shield
magic_mana_required_curse = 500 ## mana required for magic curse
magic_shield_health = 80 ## health restored by a magic shield usage
magic_shield_duration = 200 ## how long a shield lasts
magic_curse_damage = -80 ## damage caused by a magic curse
magic_curse_duration = 4 ## how long a curse lasts

## Body/Armor
armor_cost = 500
armor_repair_cost = .5
armor_cost_blacksmith_cut = .8
armor_sell_blacksmith_cut = 1.5
armor_durability = 10
armor_durability_blacksmith = 15
armor_relief_percentage = 33 ## has to be converted to decimal later
health_bodypart_max = [330,1000,250,250,500,500,40]
## Bodypart damage modifiers

## Half Hour Timer
timeout_auto_opt_out = 259200 ## Opt out users after 3 days of inactivity
halfhour_regen_health, halfhour_regen_health_max = 50,500 ## health regen rate
halfhour_regen_mage_mana, halfhour_regen_mage_mana_max = 50, 500 ## mages regenerate mana: rate
halfhour_coin = 15 ## coin gain per half hour

## Main Duel Runs
duel_lockout_timer = 300
duel_nick_order = ['nicktitles','nickpepper','nickmagicattributes','nickarmor']
duel_hit_types = ['hits','strikes','beats','pummels','bashes','smacks','knocks','bonks','chastises','clashes','clobbers','slugs','socks','swats','thumps','wallops','whops']
bot_damage = 150 ## The bot deals a set damage
USERTIMEOUT = 180 ## Time between a users ability to duel - 3 minutes
CHANTIMEOUT = 40 ## Time between duels in a channel - 40 seconds
INSTIGATORTIMEOUT = 1800 ## Time between instigation, unless another user plays
duel_special_event = 500 ## Every 50 duels, instigator wins 500 coins
### Class (dis)advantages
duel_advantage_scavenger_loot_find = 60 ## scavengers have a higher percent chance of finding loot
duel_advantage_barbarian_min_damage = 60 ## Barbarians always strike a set value or above
duel_disadvantage_vampire_max_damage = 50 ## Vampires have a max damage, but drain that amount from enemy into their own health
duel_advantage_barbarian_rage_chance = 12
duel_advantage_barbarian_rage_max = 25
duel_advantage_paladin_deflect_chance = 12
duel_advantage_knight_retaliate_chance = 12

### XP points awarded
xp_winner = 15 ## default xp earned as a winner
xp_winner_ranger = 20 ## xp earned as a winner and ranger
xp_loser = 10 ## default xp earned as a loser
xp_loser_ranger = 15 ## xp earned as a loser and ranger

## Records
duelrecorduser = 'duelrecorduser'
stat_admin_commands = ['set','reset','view'] ## valid admin subcommands
stats_view = ['class_setting','curse','shield','mana','xp','wins','losses','winlossratio','respawns','kills','lastfought','timeout_timeout','bounty']
stats_view_functions = ['winlossratio','timeout_timeout'] ## stats that use their own functions to get a value


########################
## Main Command Usage ##
########################

## work with /me ACTION (does not work with manual weapon)
@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
@module.intent('ACTION')
@module.require_chanmsg
def duel_action(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(1), 'create') # enable if not using with spicebot
    execute_main(bot, trigger, triggerargsarray, 'actionduel') # enable if not using with spicebot
    #enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'duel') ## not needed if using without spicebot
    #if not enablestatus: ## not needed if using without spicebot
    #    execute_main(bot, trigger, triggerargsarray, 'actionduel') ## not needed if using without spicebot

## Base command
@sopel.module.commands('duel','challenge')
def mainfunction(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create') # enable if not using with spicebot
    execute_main(bot, trigger, triggerargsarray, 'normalcom') # enable if not using with spicebot
    #enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'duel') ## not needed if using without spicebot
    #if not enablestatus: ## not needed if using without spicebot
    #    execute_main(bot, trigger, triggerargsarray, 'normalcom') ## not needed if using without spicebot

####################################
## Seperate Targets from Commands ##
####################################

def execute_main(bot, trigger, triggerargsarray, commandtype):

    ## Instigator
    instigator = trigger.nick
    statreset(bot, instigator)

    ## Check command was issued
    fullcommandusedtotal = get_trigger_arg(bot, triggerargsarray, 0)
    commandortarget = get_trigger_arg(bot, triggerargsarray, 1)
    if not fullcommandusedtotal:
        osd_notice(bot, instigator, "You must specify either a target, or a subcommand. Online Docs: " + GITWIKIURL)
        return

    ## Game Enabled in what channels
    inchannel = trigger.sender
    ## Game Enabled in what channels
    gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    if gameenabledchannels == []:
        if not trigger.admin:
            osd_notice(bot, instigator, "Duels has not been enabled in any channels. Talk to a bot admin.")
            return
    if inchannel not in gameenabledchannels and inchannel.startswith("#"):
        if not trigger.admin:
            osd_notice(bot, instigator, "Duels has not been enabled in " + inchannel + ". Talk to a bot admin.")
            return

    ## dev bypass
    devenabledchannels = get_database_value(bot, duelrecorduser, 'devenabled') or []

    ## Valid Commands
    validcommands = duels_valid_commands(bot)

    ## user lists
    botvisibleusers = get_database_value(bot, duelrecorduser, 'botvisibleusers') or []
    currentuserlistarray = []
    botvisibleusersappendarray = []
    for user in bot.users:
        if user not in validcommands:
            currentuserlistarray.append(user)
            if user not in botvisibleusers:
                botvisibleusersappendarray.append(user)
    adjust_database_array(bot, duelrecorduser, botvisibleusersappendarray, 'botvisibleusers', 'add')
    botvisibleusers = get_database_value(bot, duelrecorduser, 'botvisibleusers') or []

    ## Instigator can't be a command, and can't enable duels
    if instigator.lower() in validcommands:
        osd_notice(bot, instigator, "Your nick is the same as a valid command for duels.")
        return

    ## Instigator can't duelrecorduser
    if instigator.lower() == duelrecorduser:
        osd_notice(bot, instigator, "Your nick is not able to play duels.")
        return

    ## Check if Instigator is Opted in
    dueloptedinarray = get_database_value(bot, duelrecorduser, 'duelusers') or []
    if instigator not in dueloptedinarray and commandortarget.lower() not in commandarray_instigator_bypass:
        osd_notice(bot, instigator, "You are not opted into duels. Run `.duel on` to enable duels.")
        return

    ## Current Duelable Players
    currentduelplayersarray = []
    canduelarray = []
    dowedisplay = 0
    for player in currentuserlistarray:
        if player in dueloptedinarray:
            currentduelplayersarray.append(player)
    for player in currentduelplayersarray:
        executedueling = duelcriteriashort(bot, instigator, player, currentduelplayersarray, inchannel)
        if executedueling == 1:
            canduelarray.append(player)
            #statreset(bot, player)
            #healthcheck(bot, player)

    ## Time when Module use started
    now = time.time()

    ## Instigator last used
    set_database_value(bot, instigator, 'lastcommand', now)

    ## Multiple Commands
    fullcommandarray = []
    daisychaincount = 0
    if "&&" not in fullcommandusedtotal:
        fullcommandarray.append(fullcommandusedtotal)
    else:
        fullcomsplit = fullcommandusedtotal.split("&&")
        for comsplit in fullcomsplit:
            fullcommandarray.append(comsplit)
    for minicom in fullcommandarray:
        daisychaincount = daisychaincount + 1
        if daisychaincount <= 5:
            time.sleep(randint(1, 3))
            daisychaincount = 1
        triggerargsarraypart = get_trigger_arg(bot, minicom, 'create')
        fullcommandused = get_trigger_arg(bot, triggerargsarraypart, 0)
        commandortarget = get_trigger_arg(bot, triggerargsarraypart, 1)
        commandortargetsplit(bot, trigger, triggerargsarraypart, instigator, botvisibleusers, currentuserlistarray, dueloptedinarray, now, currentduelplayersarray, canduelarray, commandtype, devenabledchannels, validcommands, fullcommandused, commandortarget)

    ## bot does not need stats or backpack items
    refreshbot(bot)

    ## reset the game
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 0
    if currenttier >= 15:
        dispmsgarray = []
        dispmsgarray.append("Somebody has Triggered the Endgame! Stats will be reset.")
        gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
        onscreentext(bot, gameenabledchannels, dispmsgarray)
        chanstatreset(bot)
        duelrecordwipe(bot)
        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)

def commandortargetsplit(bot, trigger, triggerargsarray, instigator, botvisibleusers, currentuserlistarray, dueloptedinarray, now, currentduelplayersarray, canduelarray, commandtype, devenabledchannels, validcommands, fullcommandused, commandortarget):

    ## Cheap error handling for people that like to find issues
    if commandortarget.isdigit():
        osd_notice(bot, instigator, "Commands can't be numbers.")
        return

    ## Alternative commands
    altcoms = []
    for subcom in validcommands:
        try:
            commandarray_alt_eval = eval("commandarray_alt_"+subcom)
            for x in commandarray_alt_eval:
                altcoms.append(x)
            if commandortarget.lower() in commandarray_alt_eval:
                commandortarget = subcom
                continue
        except NameError:
            continue

    ## Inchannel Block
    inchannel = trigger.sender
    if commandortarget.lower() in commandarray_inchannel and not inchannel.startswith("#"):
        osd_notice(bot, instigator, "Duel " + commandortarget + " must be in channel.")
        return

    ## Subcommand Versus Target
    if commandortarget.lower() in validcommands:
        ## If command was issued as an action
        if commandtype != 'actionduel':
            subcommands(bot, trigger, triggerargsarray, instigator, fullcommandused, commandortarget, dueloptedinarray, botvisibleusers, now, currentuserlistarray, inchannel, currentduelplayersarray, canduelarray, devenabledchannels, validcommands)
        else:
            osd_notice(bot, instigator, "Action duels should not be able to run commands. Targets Only")
        return

    ## Instigator versus Bot
    if commandortarget.lower() == bot.nick.lower():
        onscreentext(bot, inchannel, "I refuse to fight a biological entity! If I did, you'd be sure to lose!")
        return

    ## Instigator versus Instigator
    if commandortarget.lower() == instigator.lower():
        onscreentext(bot, inchannel, "If you are feeling self-destructive, there are places you can call. Alternatively, you can run the harakiri command.")
        return

    ## Targets must be dueled in channel
    if not inchannel.startswith("#"):
        osd_notice(bot, instigator, "Duels must be in channel.")
        return

    ## Check if target is valid
    comorig = commandortarget
    validtarget, validtargetmsg = targetcheck(bot, commandortarget, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
    if not validtarget:
        ## Mis-spellings ## TODO add alternative commands
        ## Check Commands
        for com in validcommands:
            similarlevel = similar(commandortarget.lower(),com)
            if similarlevel >= .75:
                commandortarget = com
        ## Check alt commands
        if commandortarget == comorig:
            for com in altcoms:
                similarlevel = similar(commandortarget.lower(),com)
                if similarlevel >= .75:
                    commandortarget = com
        ## Check players, but only if we didn't alreayd match a command
        if commandortarget == comorig:
            for player in botvisibleusers:
                similarlevel = similar(commandortarget.lower(),player)
                if similarlevel >= .75:
                    commandortarget = player
        ## Did we match?
        if commandortarget != comorig:
            commandortargetsplit(bot, trigger, triggerargsarray, instigator, botvisibleusers, currentuserlistarray, dueloptedinarray, now, currentduelplayersarray, canduelarray, commandtype, devenabledchannels, validcommands, fullcommandused, commandortarget)
        else:
            onscreentext(bot, [instigator], validtargetmsg)
        return

    ## Run the duel
    duel_valid(bot, instigator, commandortarget, currentduelplayersarray, inchannel, triggerargsarray, now, devenabledchannels)

    ## Usage Counter
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)

#######################
## Subcommands Usage ##
#######################

## Subcommands
def subcommands(bot, trigger, triggerargsarray, instigator, fullcommandused, commandortarget, dueloptedinarray, botvisibleusers, now, currentuserlistarray, inchannel, currentduelplayersarray, canduelarray, devenabledchannels,validcommands):

    ## Admin Command Blocker
    if commandortarget.lower() in commandarray_admin and not trigger.admin:
        osd_notice(bot, instigator, "This admin function is only available to bot admins.")
        return

    ## Is the Tier Unlocked?
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 0
    tiercommandeval = tier_command(bot, commandortarget)
    tierpepperrequired = pepper_tier(bot, tiercommandeval)
    tiermath = int(tiercommandeval) - int(currenttier)
    if int(tiercommandeval) > int(currenttier):
        if commandortarget.lower() not in commandarray_tier_self and not inchannel in devenabledchannels:
            onscreentext(bot, inchannel, "Duel " + commandortarget + " will be unlocked when somebody reaches " + str(tierpepperrequired) + ". " + str(tiermath) + " tier(s) remaining!")
            return

    ## usage counter
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, instigator, 'usage_'+commandortarget.lower(), 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_'+commandortarget.lower(), 1)

    ## If the above passes all above checks
    subcommand_run = str('subcommand_' + commandortarget.lower() + '(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands)')
    eval(subcommand_run)

    ## reset the game
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 0
    if currenttier >= 15:
        dispmsgarray = []
        dispmsgarray.append("Somebody has Triggered the Endgame! Stats will be reset.")
        gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
        onscreentext(bot, gameenabledchannels, dispmsgarray)
        chanstatreset(bot)
        duelrecordwipe(bot)
        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)

#####################
## Main Duel Usage ##
#####################

def duel_valid(bot, instigator, commandortarget, currentduelplayersarray, inchannel, triggerargsarray, now, devenabledchannels):
    ## Lockout Check, don't allow multiple duels simultaneously
    duelslockout = get_database_value(bot, duelrecorduser, 'duelslockout') or 0
    if duelslockout:
        lockoutsince = get_timesince_duels(bot, instigator, 'duelslockout')
        if lockoutsince < duel_lockout_timer:
            osd_notice(bot, instigator, "Duel(s) is/are currently in progress. You must wait. If this is an error, it should clear itself in 5 minutes.")
            return
        reset_database_value(bot, duelrecorduser, 'duelslockout')

    ## Check that the target doesn't have a timeout preventing them from playing
    executedueling, executeduelingmsg = duelcriteria(bot, instigator, commandortarget, currentduelplayersarray, inchannel)
    if not executedueling:
        osd_notice(bot, instigator, executeduelingmsg)
        return

    ## Perform Lockout, run target duel, then unlock
    set_database_value(bot, duelrecorduser, 'duelslockout', now)
    duel_combat(bot, instigator, instigator, [commandortarget], triggerargsarray, now, inchannel, 'target', devenabledchannels)
    reset_database_value(bot, duelrecorduser, 'duelslockout')

    ## usage counter
    adjust_database_value(bot, instigator, 'usage_combat', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_combat', 1)

def duel_combat(bot, instigator, maindueler, targetarray, triggerargsarray, now, inchannel, typeofduel, devenabledchannels):


    ## Same person can't instigate twice in a row
    set_database_value(bot, duelrecorduser, 'lastinstigator', maindueler)

    ## Starting Tier
    currenttierstart = get_database_value(bot, duelrecorduser, 'tier') or 0
    tierunlockweaponslocker = tier_command(bot, 'weaponslocker_complete')
    tierscaling = tierratio_level(bot)

    ## Targetarray Start
    targetarraytotal = len(targetarray)
    for target in targetarray:

        ## target actual
        target = actualname(bot,target)

        ## Cleanup from Previous runs
        combattextarraycomplete = []
        texttargetarray = []

        ## Update last fought
        if maindueler != target and typeofduel != 'assault' and typeofduel != 'colosseum':
            set_database_value(bot, maindueler, 'lastfought', target)
            set_database_value(bot, target, 'lastfought', maindueler)

        ## Assault does not touch lastfought
        if typeofduel == 'assault':
            targetlastfoughtstart = get_database_value(bot, target, 'lastfought')

        ## Update Time Of Combat
        set_database_value(bot, maindueler, 'timeout_timeout', now)
        set_database_value(bot, target, 'timeout_timeout', now)
        set_database_value(bot, duelrecorduser, 'timeout_timeout', now)

        ## Display Naming
        mainduelername = duel_names(bot, maindueler, inchannel)
        mainduelerpepperstart = get_pepper(bot, maindueler)
        if target == maindueler:
            targetname = "themself"
            targetpepperstart = mainduelerpepperstart
        elif target == bot.nick:
            targetname = target
            targetpepperstart = get_pepper(bot, target)
        else:
            targetname = duel_names(bot, target, inchannel)
            targetpepperstart = get_pepper(bot, target)

        ## Announce Combat
        combattextarraycomplete.append(mainduelername + " versus " + targetname)

        ## Chance of maindueler finding loot
        if target != bot.nick and maindueler != target:
            randominventoryfind = randominventory(bot, maindueler)
            if randominventoryfind == 'true':
                loot = get_trigger_arg(bot, potion_types, 'random')
                loot_text = eval(loot+"dispmsg")
                combattextarraycomplete.append(maindueler + ' found a ' + str(loot) + ' ' + str(loot_text))

        ## Select winner Based on Stats
        if target == bot.nick:
            winner = bot.nick
            loser = maindueler
            losername = maindueler
        elif target == maindueler:
            winner = maindueler
            loser = maindueler
            losername = targetname
        else:
            winner = selectwinner(bot, [maindueler, target])
            if winner == maindueler:
                loser = target
                losername = targetname
            else:
                loser = maindueler
                losername = maindueler
        if winner == maindueler:
            adjust_database_value(bot, maindueler, 'assault_wins', 1)
            adjust_database_value(bot, target, 'assault_losses', 1)
        else:
            adjust_database_value(bot, maindueler, 'assault_losses', 1)
            adjust_database_value(bot, target, 'assault_wins', 1)

        ## Classes
        classwinner = get_database_value(bot, winner, 'class_setting') or 'notclassy'
        classloser = get_database_value(bot, loser, 'class_setting') or 'notclassy'

        ## Current Streaks
        winner_loss_streak, loser_win_streak = get_current_streaks(bot, winner, loser)

        ## Update Wins and Losses
        if maindueler != target:
            adjust_database_value(bot, winner, 'wins', 1)
            adjust_database_value(bot, loser, 'losses', 1)
            set_current_streaks(bot, winner, 'win')
            set_current_streaks(bot, loser, 'loss')

        ## Manual weapon
        weapon = get_trigger_arg(bot, triggerargsarray, '2+')
        if winner == maindueler and weapon and currenttierstart >= tierunlockweaponslocker:
            if weapon == 'all':
                weapon = getallchanweaponsrandom(bot)
            elif weapon == 'target' or weapon == target:
                weapon = weaponofchoice(bot, target)
                weapon = str(target + "'s " + weapon)
        elif winner == bot.nick:
            weapon = ''
        else:
            weapon = weaponofchoice(bot, winner)
        weapon = weaponformatter(bot, weapon)
        if weapon != '':
            weapon = str(" " + weapon)

        ## Magic Attributes Start
        winnershieldstart, winnercursestart = get_current_magic_attributes(bot, winner)
        losershieldstart, losercursestart = get_current_magic_attributes(bot, loser)

        ## Body Part Hit
        bodypart, bodypartname = bodypart_select(bot, loser)

        ## Strike Type
        striketype = get_trigger_arg(bot, duel_hit_types, 'random')

        ## Damage
        if classloser == 'rogue':
            if winner == loser or winner == bot.nick:
                damage = 0
                damagetext = str(loser + " takes no damage in this encounter")
            else:
                damage = duels_damage(bot, tierscaling, classwinner, classloser, winner, loser)
                damage = int(damage)
                damagetext = duels_damage_text(bot, damage, winner, loser, bodypart, striketype, weapon, classwinner, bodypartname)
        else:
            damage = duels_damage(bot, tierscaling, classwinner, classloser, winner, loser)
            damage = int(damage)
            damagetext = duels_damage_text(bot, damage, winner, loser, bodypart, striketype, weapon, classwinner, bodypartname)
        combattextarraycomplete.append(damagetext)

        ## Vampires gain health from wins
        if classwinner == 'vampire' and winner != loser:
            splitdamage = int(damage) / 6
            for part in stats_healthbodyparts:
                adjust_database_value(bot, winner, part, splitdamage)

        ## Berserker Rage
        if classwinner == 'barbarian' and winner != loser:
            rageodds = randint(1, duel_advantage_barbarian_rage_chance)
            if rageodds == 1:
                extradamage = randint(1, duel_advantage_barbarian_rage_max)
                combattextarraycomplete.append(winner + " goes into Berserker Rage for an extra " + str(extradamage) + " damage.")
                extradamage = extradamage * tierscaling
                damage = damage + extradamage

        ## Paladin deflect
        persontotakedamage = loser
        if classloser == 'paladin' and damage > 0 and winner != loser:
            deflectodds = randint(1, duel_advantage_paladin_deflect_chance)
            if deflectodds == 1:
                persontotakedamage = winner
                combattextarraycomplete.append(loser + " deflects the damage back on " + winner + ". ")
                damage, damagetextarray = damage_resistance(bot, winner, damage, bodypart)
                for x in damagetextarray:
                    combattextarraycomplete.append(x)
                if damage > 0:
                    if winner == maindueler:
                        adjust_database_value(bot, target, 'assault_damagetaken', damage)
                        adjust_database_value(bot, target, 'assault_damagedealt', damage)
                    else:
                        adjust_database_value(bot, maindueler, 'assault_damagedealt', damage)
                        adjust_database_value(bot, target, 'assault_damagetaken', damage)
                    adjust_database_value(bot, loser, bodypart, -abs(damage))
                    ## Update Health Of winner, respawn, allow loser to loot
                    winnerheadhealth = get_database_value(bot, winner, 'head')
                    winnertorsohealth = get_database_value(bot, winner, 'health_torso')
                    if winnerheadhealth  <= 0 or winnertorsohealth <= 0:
                        if winner == maindueler:
                            adjust_database_value(bot, maindueler, 'assault_deaths', 1)
                            adjust_database_value(bot, target, 'assault_kills', 1)
                        else:
                            adjust_database_value(bot, maindueler, 'assault_kills', 1)
                            adjust_database_value(bot, target, 'assault_deaths', 1)
                        loserkilledwinner = whokilledwhom(bot, loser, winner) or ''
                        for x in loserkilledwinner:
                            combattextarraycomplete.append(x)
                    else:
                        winnercurrenthealthbody  = get_database_value(bot, winner, bodypart)
                        if winnercurrenthealthbody  <= 0:
                            combattextarraycomplete.append(winner + "'s " + bodypartname + " has become crippled!")
                damage = 0

        ## Damage Resist
        if damage > 0:
            damage, damagetextarray = damage_resistance(bot, loser, damage, bodypart)
            for x in damagetextarray:
                combattextarraycomplete.append(x)
            if damage > 0:
                if winner == maindueler:
                    adjust_database_value(bot, maindueler, 'assault_damagedealt', damage)
                    adjust_database_value(bot, target, 'assault_damagetaken', damage)
                else:
                    adjust_database_value(bot, maindueler, 'assault_damagetaken', damage)
                    adjust_database_value(bot, target, 'assault_damagedealt', damage)
                adjust_database_value(bot, loser, bodypart, -abs(damage))
                ## Update Health Of loser, respawn, allow winner to loot
                loserheadhealth = get_database_value(bot, loser, 'head')
                losertorsohealth = get_database_value(bot, loser, 'health_torso')
                if loserheadhealth  <= 0 or losertorsohealth <= 0:
                    if winner == maindueler:
                        adjust_database_value(bot, maindueler, 'assault_kills', 1)
                        adjust_database_value(bot, target, 'assault_deaths', 1)
                    else:
                        adjust_database_value(bot, maindueler, 'assault_deaths', 1)
                        adjust_database_value(bot, target, 'assault_kills', 1)
                    winnerkilledloser = whokilledwhom(bot, winner, loser) or ''
                    for x in winnerkilledloser:
                        combattextarraycomplete.append(x)
                else:
                    losercurrenthealthbody  = get_database_value(bot, loser, bodypart)
                    if losercurrenthealthbody  <= 0:
                        combattextarraycomplete.append(loser + "'s " + bodypartname + " has become crippled!")

        ## Knight Retaliation
        if classloser == 'knight' and winner != loser:
            retaliateodds = randint(1, duel_advantage_knight_retaliate_chance)
            if retaliateodds == 1:
                ## Weapon
                weaponb = weaponofchoice(bot, loser)
                weaponb = weaponformatter(bot, weaponb)
                weaponb = str(" "+ weaponb)
                ## Body Part Hit
                bodypartb, bodypartnameb = bodypart_select(bot, winner)
                ## Strike Type
                striketypeb = get_trigger_arg(bot, duel_hit_types, 'random')
                ## Damage
                damageb = duels_damage(bot, tierscaling, classloser, classwinner, loser, winner)
                damagetextb = duels_damage_text(bot, damage, loser, winner, bodypartb, striketypeb, weaponb, classloser, bodypartnameb)
                combattextarraycomplete.append(damagetextb)
                ## Damage Resist
                if damage > 0:
                    damage, damagetextarray = damage_resistance(bot, loser, damage, bodypart)
                    for x in damagetextarray:
                        combattextarraycomplete.append(x)
                    if damage > 0:
                        if winner == maindueler:
                            adjust_database_value(bot, maindueler, 'assault_damagetaken', damage)
                            adjust_database_value(bot, target, 'assault_damagedealt', damage)
                        else:
                            adjust_database_value(bot, maindueler, 'assault_damagedealt', damage)
                            adjust_database_value(bot, target, 'assault_damagetaken', damage)
                        adjust_database_value(bot, winner, bodypartb, -abs(damage))
                        ## Update Health Of winner, respawn, allow loser to loot
                        winnerheadhealth = get_database_value(bot, winner, 'head')
                        winnertorsohealth = get_database_value(bot, winner, 'health_torso')
                        if winnerheadhealth  <= 0 or winnertorsohealth <= 0:
                            if winner == maindueler:
                                adjust_database_value(bot, maindueler, 'assault_deaths', 1)
                                adjust_database_value(bot, target, 'assault_kills', 1)
                            else:
                                adjust_database_value(bot, maindueler, 'assault_kills', 1)
                                adjust_database_value(bot, target, 'assault_deaths', 1)
                            loserkilledwinner = whokilledwhom(bot, loser, winner) or ''
                            for x in loserkilledwinner:
                                combattextarraycomplete.append(x)
                        else:
                            winnercurrenthealthbody  = get_database_value(bot, winner, bodypart)
                            if winnercurrenthealthbody  <= 0:
                                combattextarraycomplete.append(winner + "'s " + bodypartnameb + " has become crippled!")

        ## Chance that maindueler loses found loot
        if target != bot.nick and maindueler != target:
            if randominventoryfind == 'true':
                ## Barbarians get a 50/50 chance of getting loot even if they lose
                classloser = get_database_value(bot, loser, 'class_setting') or 'notclassy'
                barbarianstealroll = randint(0, 100)
                if classloser == 'barbarian' and barbarianstealroll >= 50:
                    combattextarraycomplete.append(loser + " steals the " + str(loot))
                    lootwinner = loser
                elif winner == target:
                    combattextarraycomplete.append(winner + " gains the " + str(loot))
                    lootwinner = winner
                else:
                    lootwinner = winner
                adjust_database_value(bot, lootwinner, "loot_"+loot, 1)
                if lootwinner == maindueler:
                    adjust_database_value(bot, maindueler, 'assault_potionswon', 1)
                    adjust_database_value(bot, target, 'assault_potionslost', 1)
                else:
                    adjust_database_value(bot, maindueler, 'assault_potionslost', 1)
                    adjust_database_value(bot, target, 'assault_potionswon', 1)

        ## Update XP points
        if classwinner == 'ranger':
            XPearnedwinner = xp_winner_ranger
        else:
            XPearnedwinner = xp_winner
        if classloser == 'ranger':
            XPearnedloser = xp_loser_ranger
        else:
            XPearnedloser = xp_loser
        if maindueler != target and target != bot.nick:
            winnertier = get_database_value(bot, winner, 'tier')
            losertier = get_database_value(bot, loser, 'tier')
            if winnertier < currenttierstart:
                XPearnedwinner = XPearnedwinner * tierscaling
            if losertier < currenttierstart:
                XPearnedloser = XPearnedloser * tierscaling
            adjust_database_value(bot, winner, 'xp', XPearnedwinner)
            adjust_database_value(bot, loser, 'xp', XPearnedloser)
            if winner == maindueler:
                adjust_database_value(bot, maindueler, 'assault_xp', XPearnedwinner)
                adjust_database_value(bot, target, 'assault_xp', XPearnedloser)
            else:
                adjust_database_value(bot, maindueler, 'assault_xp', XPearnedloser)
                adjust_database_value(bot, target, 'assault_xp', XPearnedwinner)

        ## Streaks Text
        if maindueler != target:
            streaktext = get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak) or ''
            if streaktext != '':
                combattextarraycomplete.append(streaktext)

        ## new pepper level?
        mainduelerpeppernow = get_pepper(bot, maindueler)
        if mainduelerpeppernow != mainduelerpepperstart and maindueler != target:
            combattextarraycomplete.append(maindueler + " graduates to " + mainduelerpeppernow + "! ")
            adjust_database_value(bot, maindueler, 'assault_levelups', 1)
        targetpeppernow = get_pepper(bot, target)
        if targetpeppernow != targetpepperstart and maindueler != target and target != bot.nick:
            adjust_database_value(bot, target, 'assault_levelups', 1)
            combattextarraycomplete.append(target + " graduates to " + targetpeppernow + "! ")

        ## Tier update
        currenttierend = get_database_value(bot, duelrecorduser, 'tier') or 1
        if int(currenttierend) > int(currenttierstart):
            combattextarraycomplete.append("New Tier Unlocked!")
            tiercheck = eval("commandarray_tier_unlocks_"+str(currenttierend))
            if tiercheck != []:
                newtierlist = get_trigger_arg(bot, tiercheck, "list")
                combattextarraycomplete.append("Feature(s) now available: " + newtierlist)

        ## Magic Attributes text
        if maindueler != target:
            magicattributestext = get_magic_attributes_text(bot, winner, loser, winnershieldstart, losershieldstart, winnercursestart , losercursestart)
            for x in magicattributestext:
                combattextarraycomplete.append(x)

        ## Special Event
        speceventtext = ''
        speceventtotal = get_database_value(bot, duelrecorduser, 'specevent') or 0
        if speceventtotal >= 49:
            set_database_value(bot, duelrecorduser, 'specevent', 1)
            combattextarraycomplete.append(maindueler + " triggered the special event! Winnings are "+str(duel_special_event)+" Coins!")
            adjust_database_value(bot, maindueler, 'coin', duel_special_event)
        else:
            adjust_database_value(bot, duelrecorduser, 'specevent', 1)

        ## Random Bonus
        if typeofduel == 'random' and winner == maindueler and winner != bot.nick and winner != loser:
            adjust_database_value(bot, winner, 'coin', random_payout)
            combattextarraycomplete.append(maindueler + " won the random attack payout!")

        ## On Screen Text
        if typeofduel != 'assault' and typeofduel != 'colosseum':
            onscreentext(bot, [inchannel], combattextarraycomplete)
        else:
            onscreentext(bot, [winner,loser], combattextarraycomplete)

        ## Pause Between duels
        if typeofduel == 'assault':
            bot.notice("  ", maindueler)
            time.sleep(randint(2, 5)) # added to protect bot from "excess flood"

        ## End Of assault
        if typeofduel == 'assault':
            set_database_value(bot, target, 'lastfought', targetlastfoughtstart)

#################
## Subcommands ##
#################

## Author Subcommand
def subcommand_author(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    onscreentext(bot, inchannel, "The author of Duels is deathbybandaid.")

def subcommand_version(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    bot.say("WIP") ## TODO

## Docs Subcommand
def subcommand_docs(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    target = get_trigger_arg(bot, triggerargsarray, 2)
    if not target:
        onscreentext(bot, inchannel, "Online Docs: " + GITWIKIURL)
        return
    ## private message player
    validtarget, validtargetmsg = targetcheck(bot, commandortarget, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
        return
    osd_notice(bot, target, "Online Docs: " + GITWIKIURL)

## On Subcommand
def subcommand_on(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):

    ## User can't toggle status all the time
    instigatoropttime = get_timesince_duels(bot, instigator, 'timeout_opttime')
    if instigatoropttime < timeout_opt and not inchannel in devenabledchannels:
        osd_notice(bot, instigator, "It looks like you can't enable/disable duels for " + str(hours_minutes_seconds((timeout_opt - instigatoropttime))) + ".")
        return

    ## check if player already has duels on
    if instigator.lower() in [x.lower() for x in dueloptedinarray]:
        osd_notice(bot, instigator, "It looks like you already have duels on.")
        return

    ## make the adjustment
    adjust_database_array(bot, duelrecorduser, [instigator], 'duelusers', 'add')
    set_database_value(bot, instigator, 'timeout_opttime', now)
    osd_notice(bot, instigator, "Duels should now be " +  commandortarget + " for you.")

    ## Anounce to channels
    gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    dispmsgarray = []
    dispmsgarray.append(instigator + " has entered the arena!")
    onscreentext(bot, gameenabledchannels, dispmsgarray)

## Off Subcommand
def subcommand_off(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):

    ## array of insulting departures
    cowardarray = ['A man that flies from his fear may find that he has only taken a short cut to meet it. ― J.R.R. Tolkien','He was just a coward and that was the worst luck any many could have. - Ernest Hemingway','The coward fears the prick of Fate, not he who dares all, becoming himself the dreaded one. - Elise Pumpelly Cabot']

    ## User can't toggle status all the time
    instigatoropttime = get_timesince_duels(bot, instigator, 'timeout_opttime')
    if instigatoropttime < timeout_opt and not inchannel in devenabledchannels:
        osd_notice(bot, instigator, "It looks like you can't enable/disable duels for " + str(hours_minutes_seconds((timeout_opt - instigatoropttime))) + ".")
        return

    ## check if player already has duels off
    if instigator.lower() not in [x.lower() for x in dueloptedinarray]:
        osd_notice(bot, instigator, "It looks like you already have duels off.")
        return

    ## make the adjustment
    adjust_database_array(bot, duelrecorduser, [instigator], 'duelusers', 'del')
    set_database_value(bot, instigator, 'timeout_opttime', now)
    osd_notice(bot, instigator, "Duels should now be " +  commandortarget + " for you.")

    ## Anounce to channels
    gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    dispmsgarray = []
    cowardterm = get_trigger_arg(bot, cowardarray, 'random')
    dispmsgarray.append(instigator + " has left the arena! " + cowardterm)
    onscreentext(bot, gameenabledchannels, dispmsgarray)

## Enable game
def subcommand_game(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    command = get_trigger_arg(bot, triggerargsarray, 2)
    if not command:
        osd_notice(bot, instigator, "Options are On or Off.")
        return
    if command == 'on':
        adjust_database_array(bot, duelrecorduser, [inchannel], 'gameenabled', 'add')
        osd_notice(bot, instigator, "Duels is on in " + inchannel + ".")
    else:
        adjust_database_array(bot, duelrecorduser, [inchannel], 'gameenabled', 'del')
        osd_notice(bot, instigator, "Duels is off in " + inchannel + ".")

## dev bypass
def subcommand_devmode(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    command = get_trigger_arg(bot, triggerargsarray, 2)
    if not command:
        osd_notice(bot, instigator, "Options are On or Off.")
        return
    if command == 'on':
        adjust_database_array(bot, duelrecorduser, [inchannel], 'devenabled', 'add')
        osd_notice(bot, instigator, "Devmode is on in " + inchannel + ".")
    else:
        adjust_database_array(bot, duelrecorduser, [inchannel], 'devenabled', 'del')
        osd_notice(bot, instigator, "Devmode is off in " + inchannel + ".")

## Health Subcommand
def subcommand_health(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    healthcommand = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    if not healthcommand or healthcommand.lower() in [x.lower() for x in dueloptedinarray]:
        if int(tiercommandeval) > int(currenttier) and healthcommand != instigator:
            osd_notice(bot, instigator, "Health for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!")
            if not inchannel in devenabledchannels:
                return
        validtarget, validtargetmsg = targetcheck(bot, healthcommand, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        healthcommand = actualname(bot, healthcommand)
        dispmsgarray = []
        totalhealth = 0
        targetclass = get_database_value(bot, healthcommand, 'class_setting') or 'notclassy'
        for x in stats_healthbodyparts:
            gethowmany = get_database_value(bot, healthcommand, x)
            if gethowmany:
                xname = x.replace("_", " ")
                xname = xname.title()
                if targetclass == 'vampire':
                    gethowmany = -abs(gethowmany)
                dispmsgarray.append(str(xname) + "=" + str(gethowmany))
                totalhealth = totalhealth + gethowmany
        dispmsgarrayb = []
        if dispmsgarray != []:
            dispmsgarrayb.append(healthcommand + "'s " + commandortarget + ":")
            dispmsgarrayb.append("Total Health=" + str(totalhealth))
            for y in dispmsgarray:
                dispmsgarrayb.append(y)
        else:
            dispmsgarrayb.append(instigator + ", It looks like " + healthcommand + " has no " +  commandortarget + ".")
        onscreentext(bot, ['say'], dispmsgarrayb)

## Tier Subcommand
def subcommand_tier(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    command = get_trigger_arg(bot, triggerargsarray, 2)
    dispmsgarray = []
    currenttierpepper = pepper_tier(bot, currenttier)
    dispmsgarray.append("The current tier is " + str(currenttier)+ " ("+ str(currenttierpepper.title()) + ").")

    ## Display current/future features
    if not command:
        currenttierlistarray = []
        futuretierlistarray = []
        for i in range(0,16):
            tiercheck = eval("commandarray_tier_unlocks_"+str(i))
            for x in tiercheck:
                if i <= currenttier:
                    if x not in commandarray_tier_display_exclude:
                        currenttierlistarray.append(x)
                else:
                    if x not in commandarray_tier_display_exclude:
                        futuretierlistarray.append(x)
        if currenttierlistarray != []:
            currenttierlist = get_trigger_arg(bot, currenttierlistarray, "list")
            dispmsgarray.append("Feature(s) currently available: " + currenttierlist + ".")
        if futuretierlistarray != []:
            futuretierlist = get_trigger_arg(bot, futuretierlistarray, "list")
            dispmsgarray.append("Feature(s) not yet unlocked: " + futuretierlist + ".")

    ## Don't show list
    elif command.lower() in commandarray_tier_display_exclude:
        osd_notice(bot, instigator, "That appears to be an invalid command.")
        return

    ## What tier is next
    elif command.lower() == 'next':
        nexttier = currenttier + 1
        if nexttier > 15:
            onscreentext(bot, inchannel, "Tiers do not got past 15 (Pure Capsaicin).")
            return
        nextpepper = pepper_tier(bot, nexttier)
        tiercheck = eval("commandarray_tier_unlocks_"+str(nexttier))
        if tiercheck != []:
            tierlist = get_trigger_arg(bot, tiercheck, "list")
            dispmsgarray.append("Feature(s) that are available at tier " + str(nexttier) + " (" + str(nextpepper.title()) +"): " + tierlist + ".")
        else:
            dispmsgarray.append("No New Feature(s) available at tier " + str(nexttier) + " (" + str(nextpepper.title()) + ").")

    ## Find what tier a command is in
    elif command.lower() in validcommands:
        commandtier = tier_command(bot, command)
        commandpepper = pepper_tier(bot, commandtier)
        dispmsgarray.append("The " + str(command) + " is unlocked at tier " + str(commandtier)+ " ("+ str(commandpepper.title()) + ").")
        tiercheck = eval("commandarray_tier_unlocks_"+str(commandtier))
        tiermath = commandtier - currenttier
        if tiermath > 0:
            dispmsgarray.append(str(tiermath) + " tier(s) remaining!")

    ## find what tier a pepper level is
    elif command.lower() in commandarray_pepper_levels:
        commandtier = tier_pepper(bot, command)
        tiercheck = eval("commandarray_tier_unlocks_"+str(commandtier))
        if tiercheck != []:
            tierlist = get_trigger_arg(bot, tiercheck, "list")
            dispmsgarray.append("Feature(s) that are available at tier " + str(commandtier) + " (" + str(command.title()) +"): " + tierlist + ".")
        else:
            dispmsgarray.append("No New Feature(s) available at tier " + str(commandtier) + " (" + str(command.title()) + ").")
        tiermath = int(commandtier) - currenttier
        if tiermath > 0:
            dispmsgarray.append(str(tiermath) + " tier(s) remaining!")

    ## process a tier number
    elif command.isdigit():
        command = int(command)
        if int(command) > 15:
            onscreentext(bot, inchannel, "Tiers do not got past 15 (Pure Capsaicin).")
            return
        commandpepper = pepper_tier(bot, command)
        tiercheck = eval("commandarray_tier_unlocks_"+str(command))
        if tiercheck != []:
            tierlist = get_trigger_arg(bot, tiercheck, "list")
            dispmsgarray.append("Feature(s) that are available at tier " + str(command) + " (" + str(commandpepper.title()) +"): " + tierlist + ".")
        else:
            dispmsgarray.append("No New Feature(s) available at tier " + str(command) + " (" + str(commandpepper.title()) + ").")
        tiermath = int(command) - currenttier
        if tiermath > 0:
            dispmsgarray.append(str(tiermath) + " tier(s) remaining!")

    ## find the player with the most xp, and how long until they reach a new tier
    elif command.lower() == 'closest':
        statleadername = ''
        statleadernumber  = 0
        for user in currentuserlistarray:
            statamount = get_database_value(bot, user, 'xp')
            if statamount >= statleadernumber and statamount > 0:
                statleadername = user
                statleadernumber = statamount
        if statleadername != '':
            nexttier = currenttier + 1
            if int(nexttier) > 15:
                onscreentext(bot, inchannel, "Tiers do not got past 15 (Pure Capsaicin).")
                return
            tierxprequired = get_trigger_arg(bot, commandarray_xp_levels, nexttier)
            tierxpmath = tierxprequired - statleadernumber
            dispmsgarray.append("The leader in xp is " + statleadername + " with " + str(statleadernumber) + ". The next tier is " + str(abs(tierxpmath)) + " xp away.")
            nextpepper = pepper_tier(bot, nexttier)
            tiercheck = eval("commandarray_tier_unlocks_"+str(nexttier))
            if tiercheck != []:
                tierlist = get_trigger_arg(bot, tiercheck, "list")
                dispmsgarray.append("Feature(s) that are available at tier " + str(nexttier) + " (" + str(nextpepper.title()) +"): " + tierlist + ".")
            else:
                dispmsgarray.append("No New Feature(s) available at tier " + str(nexttier) + " (" + str(nextpepper.title()) + ").")
            tiermath = int(nexttier) - currenttier
            if tiermath > 0:
                dispmsgarray.append(str(tiermath) + " tier(s) remaining!")
        else:
            dispmsgarray.append("Nobody is the closest to the next pepper level.")

    ## anything else is deemed a target, see what tier they are on if valid
    else:
        validtarget, validtargetmsg = targetcheck(bot, command, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        targettier = get_database_value(bot, command, 'tier') or 0
        dispmsgarray.append(command + "'s current tier is " + str(targettier)+ ". ")

    ## display the info
    onscreentext(bot, ['say'], dispmsgarray)

## Suicide/harakiri
def subcommand_harakiri(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    if target != instigator and target != 'confirm':
        onscreentext(bot, inchannel, "You can't suicide other people. It's called Murder.")
    elif target == instigator:
        onscreentext(bot, inchannel, "You must run this command with 'confirm' to kill yourself. No rewards are given in to cowards.")
    else:
        suicidetextarray = suicidekill(bot,instigator)
        onscreentext(bot, ['say'], suicidetextarray)

## Russian Roulette
def subcommand_roulette(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):

    ## instigator must wait until the next round
    roulettelastshot = get_database_value(bot, duelrecorduser, 'roulettelastplayershot') or bot.nick
    if roulettelastshot == instigator and not inchannel in devenabledchannels:
        osd_notice(bot, instigator, "You must wait for the current round to complete, until you may play again.")
        return

    ## Instigator must wait a day after death
    getlastdeath = get_timesince_duels(bot, instigator, 'roulettedeath') or roulette_death_timeout
    if getlastdeath < roulette_death_timeout and not inchannel in devenabledchannels:
        osd_notice(bot, instigator, "You must wait 24 hours between roulette deaths.")
        return

    ## Small timeout
    getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + commandortarget)) or timeout_roulette
    if getlastusage < timeout_roulette and not inchannel in devenabledchannels:
        osd_notice(bot, instigator, "Roulette has a small timeout.")
        return
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)

    ## Check who last pulled the trigger, or if it's a new chamber
    roulettelastplayer = get_database_value(bot, duelrecorduser, 'roulettelastplayer') or bot.nick
    roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1

    ## Get the selected chamber from the database,, or set one
    roulettechamber = get_database_value(bot, duelrecorduser, 'roulettechamber')
    if not roulettechamber:
        roulettechamber = randint(1, 6)
        set_database_value(bot, duelrecorduser, 'roulettechamber', roulettechamber)

    ## Display Text
    instigatorcurse = get_database_value(bot, instigator, 'curse') or 0
    if instigatorcurse:
        onscreentext(bot, inchannel, instigator + " spins the cylinder to the bullet's chamber and pulls the trigger.")
    elif roulettelastplayer == instigator and int(roulettecount) > 1:
        onscreentext(bot, inchannel, instigator + " spins the revolver and pulls the trigger.")
    elif int(roulettecount) == 1:
        onscreentext(bot, inchannel, instigator + " reloads the revolver, spins the cylinder and pulls the trigger.")
    else:
        onscreentext(bot, inchannel, instigator + " spins the cylinder and pulls the trigger.")

    ## Default 6 possible locations for bullet.
    ### curses
    if instigatorcurse:
        adjust_database_value(bot, instigator, 'curse', -1)
        reset_database_value(bot, duelrecorduser, 'roulettespinarray')
        currentspin = roulettechamber
    ### If instigator uses multiple times in a row, decrease odds of success
    elif roulettelastplayer == instigator:
        roulettespinarray = get_database_value(bot, duelrecorduser, 'roulettespinarray')
        if not roulettespinarray:
            roulettespinarray = [1,2,3,4,5,6]
        if len(roulettespinarray) > 1:
            roulettetemp = []
            for x in roulettespinarray:
                if int(x) != int(roulettechamber):
                    roulettetemp.append(x)
            rouletteremove = get_trigger_arg(bot, roulettetemp, "random")
            roulettetempb = []
            roulettetempb.append(roulettechamber)
            for j in roulettetemp:
                if int(j) != int(rouletteremove):
                    roulettetempb.append(j)
            set_database_value(bot, duelrecorduser, 'roulettespinarray', roulettetempb)
            currentspin = get_trigger_arg(bot, roulettetempb, "random")
        else:
            currentspin = roulettechamber ## if only one location left
            reset_database_value(bot, duelrecorduser, 'roulettespinarray')
    else:
        roulettespinarray = [1,2,3,4,5,6]
        reset_database_value(bot, duelrecorduser, 'roulettespinarray')
        currentspin = get_trigger_arg(bot, roulettespinarray, "random")

    ### current spin is safe
    if int(currentspin) != int(roulettechamber):
        time.sleep(randint(1, 3)) # added to build suspense
        onscreentext(bot, inchannel, "*click*")
        roulettecount = roulettecount + 1
        roulettepayout = roulette_payout_default * roulettecount
        currentpayout = get_database_value(bot, instigator, 'roulettepayout')
        adjust_database_value(bot, instigator, 'roulettepayout', roulettepayout)
        set_database_value(bot, duelrecorduser, 'roulettecount', roulettecount)
        set_database_value(bot, duelrecorduser, 'roulettelastplayer', instigator)
        adjust_database_array(bot, duelrecorduser, [instigator], 'roulettewinners', 'add')

    ### instigator shoots themself in the head
    else:
        tierscaling = tierratio_level(bot)
        currenttierstart = get_database_value(bot, duelrecorduser, 'tier') or 0
        dispmsgarray = []
        if roulettecount == 1:
            if instigatorcurse:
                dispmsgarray.append("First in the chamber. Looks like " + instigator + " was cursed!")
            else:
                dispmsgarray.append("First in the chamber. What bad luck.")

        ## XP
        classloser = get_database_value(bot, instigator, 'class_setting')
        losertier = get_database_value(bot, instigator, 'tier')
        if classloser == 'ranger':
            XPearnedloser = xp_loser_ranger
        else:
            XPearnedloser = xp_loser
        if losertier < currenttierstart:
            XPearnedloser = XPearnedloser * tierscaling
        adjust_database_value(bot, instigator, 'xp', XPearnedloser)

        ## Dish out the pain
        damage = randint(50, 120)
        bodypart = 'head'
        revolver = get_trigger_arg(bot, roulette_revolver_list, 'random')
        damagescale = tierratio_level(bot)
        damage = damagescale * damage
        dispmsgarray.append(instigator + " shoots themself in the head with the " + revolver + ", dealing " + str(damage) + " damage. ")
        damage, damagetextarray = damage_resistance(bot, instigator, damage, bodypart)
        for x in damagetextarray:
            dispmsgarray.append(x)
        if damage > 0:
            adjust_database_value(bot, instigator, 'head', -abs(damage))
            instigatorcurrenthealth  = get_database_value(bot, instigator, 'head')
            if instigatorcurrenthealth  <= 0:
                suicidetextarray = suicidekill(bot,instigator)
                for x in suicidetextarray:
                    dispmsgarray.append(x)

        ## Payouts
        biggestpayout, biggestpayoutwinner = 0,''
        roulettewinners = get_database_value(bot, duelrecorduser, 'roulettewinners') or []
        uniquewinnersarray = []
        for x in roulettewinners:
            if x not in uniquewinnersarray and x != instigator:
                uniquewinnersarray.append(x)
        for x in uniquewinnersarray:

            ## Award XP
            classwinner = get_database_value(bot, x, 'class_setting')
            winnertier = get_database_value(bot, x, 'tier')
            if classwinner == 'ranger':
                XPearnedwinner = xp_winner_ranger
            else:
                XPearnedwinner = xp_winner
            if winnertier < currenttierstart:
                XPearnedwinner = XPearnedwinner * tierscaling
            adjust_database_value(bot, x, 'xp', XPearnedwinner)

            ## coin
            roulettepayoutx = get_database_value(bot, x, 'roulettepayout')
            if roulettepayoutx > biggestpayout and roulettepayoutx != 0:
                biggestpayoutwinner = x
                biggestpayout = roulettepayoutx
            elif roulettepayoutx == biggestpayout and roulettepayoutx != 0:
                biggestpayoutwinner = str(biggestpayoutwinner+ " " + x)
                biggestpayout = roulettepayoutx
            adjust_database_value(bot, x, 'coin', roulettepayoutx)
            if roulettepayoutx > 0:
                osd_notice(bot, x, "Your roulette payouts = " + str(roulettepayoutx) + " coins!")
            reset_database_value(bot, x, 'roulettepayout')

        ## unique winner list
        if uniquewinnersarray != []:
            displaymessage = get_trigger_arg(bot, uniquewinnersarray, "list")
            if len(uniquewinnersarray) > 1:
                dispmsgarray.append("Winners: " + displaymessage + ".")
            else:
                dispmsgarray.append("Winner: " + displaymessage + ".")
        if biggestpayoutwinner != '':
            dispmsgarray.append("Biggest Payout: "+ biggestpayoutwinner + " with " + str(biggestpayout) + " coins.")
        roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1
        if roulettecount > 1:
            roulettecount = roulettecount + 1
            dispmsgarray.append("The chamber spun " + str(roulettecount) + " times. ")
        time.sleep(randint(1, 2)) # added to build suspense
        onscreentext(bot, [inchannel], dispmsgarray)

        ## instigator must wait until the next round
        reset_database_value(bot, duelrecorduser, 'roulettelastplayershot')
        set_database_value(bot, duelrecorduser, 'roulettelastplayershot', instigator)

        ### Reset for next run
        reset_database_value(bot, duelrecorduser, 'roulettelastplayer')
        reset_database_value(bot, duelrecorduser, 'roulettechamber')
        reset_database_value(bot, duelrecorduser, 'roulettewinners')
        reset_database_value(bot, duelrecorduser, 'roulettecount')
        reset_database_value(bot, instigator, 'roulettepayout')

## Mayhem
def subcommand_mayhem(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    if instigator not in canduelarray:
        canduel, validtargetmsg = duelcriteria(bot, instigator, commandortarget, currentduelplayersarray, inchannel)
        osd_notice(bot, instigator, validtargetmsg)
        return
    duelslockout = get_database_value(bot, duelrecorduser, 'duelslockout') or 0
    if duelslockout:
        lockoutsince = get_timesince_duels(bot, instigator, 'duelslockout')
        if lockoutsince < duel_lockout_timer:
            osd_notice(bot, x, "Duel(s) is/are currently in progress. You must wait. If this is an error, it should clear itself in 5 minutes.")
            return
        reset_database_value(bot, duelrecorduser, 'duelslockout')
    set_database_value(bot, duelrecorduser, 'duelslockout', now)
    if bot.nick in canduelarray:
        canduelarray.remove(bot.nick)
    executedueling, executeduelingmsg = eventchecks(bot, canduelarray, commandortarget, instigator, currentduelplayersarray, inchannel)
    if not executedueling:
        osd_notice(bot, instigator, executeduelingmsg)
        return
    displaymessage = get_trigger_arg(bot, canduelarray, "list")
    onscreentext(bot, inchannel, instigator + " Initiated a full channel " + commandortarget + " event. Good luck to " + displaymessage)
    for user in canduelarray:
        for astat in assault_results:
            reset_database_value(bot, instigator, "assault_" + astat)
    for maindueler in canduelarray:
        targetarray = []
        for player in canduelarray:
            if player != maindueler:
                targetarray.append(player)
        duel_combat(bot, instigator, maindueler, targetarray, triggerargsarray, now, inchannel, 'assault', devenabledchannels)
    for user in canduelarray:
        assaultstatsarray = []
        assaultstatsarray.append(user + "'s Full Channel Mayhem results:")
        for astat in assault_results:
            astateval = get_database_value(bot, user, "assault_" + astat) or 0
            if astateval:
                astatstr = str(str(astat) + " = " + str(astateval))
                assaultstatsarray.append(astatstr)
                reset_database_value(bot, user, "assault_" + astat)
        onscreentext(bot, [inchannel], assaultstatsarray)
        time.sleep(1)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator'), instigator)

## Hunger Games
def subcommand_hungergames(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    if instigator not in canduelarray:
        canduel, validtargetmsg = duelcriteria(bot, instigator, commandortarget, currentduelplayersarray, inchannel)
        osd_notice(bot, instigator, executeduelingmsg)
        return
    if bot.nick in canduelarray:
        canduelarray.remove(bot.nick)
    executedueling, executeduelingmsg = eventchecks(bot, canduelarray, commandortarget, instigator, currentduelplayersarray, inchannel)
    if not executedueling:
        osd_notice(bot, instigator, executeduelingmsg)
        return
    totaltributes = len(canduelarray)
    totaltributesstart = totaltributes
    if totaltributes == 1:
        osd_notice(bot, instigator, "There is only one tribute.  Try again later.")
        return
    currenttierstart = get_database_value(bot, duelrecorduser, 'tier') or 0
    tierscaling = tierratio_level(bot)
    dispmsgarray = []
    displaymessage = get_trigger_arg(bot, canduelarray, "list")
    onscreentext(bot, inchannel, instigator + " Initiated a full channel " + commandortarget + " event. Good luck to " + displaymessage)
    winnerorder = []
    while totaltributes > 0:
        totaltributes = totaltributes - 1
        winner = selectwinner(bot, canduelarray)
        winnerorder.append(winner)
        canduelarray.remove(winner)
    reversedorder = get_trigger_arg(bot, winnerorder, 'reverse')
    lastkilled = ''
    for player in reversedorder:
        if lastkilled != '':
            minidispmsgarray = []
            classplayer = get_database_value(bot, player, 'class_setting') or 'notclassy'
            classlastkilled = get_database_value(bot, lastkilled, 'class_setting') or 'notclassy'
            weapon = weaponofchoice(bot, player)
            weapon = weaponformatter(bot, weapon)
            minidispmsgarray.append(player + " hits " + lastkilled + " " + weapon + ', forcing a respawn.')
            whokilledwhom(bot, player, lastkilled)
            classplayer = get_database_value(bot, player, 'class_setting')
            playertier = get_database_value(bot, player, 'tier')
            if classplayer == 'ranger':
                XPearnedplayer = xp_winner_ranger
            else:
                XPearnedplayer = xp_winner
            if playertier < currenttierstart:
                XPearnedplayer = XPearnedplayer * tierscaling
            adjust_database_value(bot, player, 'xp', XPearnedplayer)
            classlastkilled = get_database_value(bot, lastkilled, 'class_setting')
            lastkilledtier = get_database_value(bot, lastkilled, 'tier')
            if classlastkilled == 'ranger':
                XPearnedlastkilled = xp_loser_ranger
            else:
                XPearnedlastkilled = xp_loser
            if lastkilledtier < currenttierstart:
                XPearnedlastkilled = XPearnedlastkilled * tierscaling
            adjust_database_value(bot, lastkilled, 'xp', XPearnedlastkilled)
            onscreentext(bot, [player,lastkilled], minidispmsgarray)
        else:
            dispmsgarray.append(player + " was the first to die.")
        lastkilled = player
    dispmsgarray.append(player + " is the victor!")
    reverseddisplay = get_trigger_arg(bot, dispmsgarray, 'reverse')
    onscreentext(bot, ['say'], reverseddisplay)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator'), instigator)

## Colosseum
def subcommand_colosseum(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    if bot.nick in canduelarray:
        canduelarray.remove(bot.nick)
    executedueling, executeduelingmsg = eventchecks(bot, canduelarray, commandortarget, instigator, currentduelplayersarray, inchannel)
    if not executedueling:
        osd_notice(bot, instigator, executeduelingmsg)
        return
    if instigator in canduelarray:
        canduelarray.remove(instigator)
    currenttierstart = get_database_value(bot, duelrecorduser, 'tier') or 0
    tierscaling = tierratio_level(bot)
    dispmsgarray = []
    displaymessage = get_trigger_arg(bot, canduelarray, "list")
    onscreentext(bot, inchannel, instigator + " Initiated a full channel " + commandortarget + " event. Good luck to " + displaymessage)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator'), instigator)
    totalplayers = len(canduelarray)
    riskcoins = int(totalplayers) * 30
    damage = riskcoins
    winner = selectwinner(bot, canduelarray)
    dispmsgarray.append("The Winner is: " + winner + "! Total winnings: " + str(riskcoins) + " coin! Losers took " + str(riskcoins) + " damage.")
    diedinbattle = []
    canduelarray.remove(winner)
    classwinner = get_database_value(bot, winner, 'class_setting')
    winnertier = get_database_value(bot, winner, 'tier')
    if classwinner == 'ranger':
        XPearnedwinner = xp_winner_ranger
    else:
        XPearnedwinner = xp_winner
    if winnertier < currenttierstart:
        XPearnedwinner = XPearnedwinner * tierscaling
    adjust_database_value(bot, winner, 'xp', XPearnedwinner)
    for x in canduelarray:
        classloser = get_database_value(bot, x, 'class_setting')
        losertier = get_database_value(bot, x, 'tier')
        if classloser == 'ranger':
            XPearnedloser = xp_loser_ranger
        else:
            XPearnedloser = xp_loser
        if losertier < currenttierstart:
            XPearnedloser = XPearnedloser * tierscaling
        adjust_database_value(bot, x, 'xp', XPearnedloser)
        damagescale = tierratio_level(bot)
        damage = damagescale * damage
        bodypart, bodypartname = bodypart_select(bot, x)
        damage, damagetextarray = damage_resistance(bot, x, damage, bodypart)
        for j in damagetextarray:
            dispmsgarray.append(j)
        if damage > 0:
            splitdamage = int(damage) / 6
            for part in stats_healthbodyparts:
                adjust_database_value(bot, x, part, -abs(splitdamage))
            xheadhealth = get_database_value(bot, x, 'head')
            xtorsohealth = get_database_value(bot, x, 'health_torso')
            if xheadhealth  <= 0 or xtorsohealth <= 0:
                winnertextarray = whokilledwhom(bot, winner, x)
                diedinbattle.append(x)
            else:
                for part in stats_healthbodyparts:
                    xcurrenthealthbody  = get_database_value(bot, x, part)
                    if xcurrenthealthbody  <= 0:
                        if "_" in bodypartname:
                            bodypartname = bodypartname.replace("_", " ")
                        dispmsgarray.append(x + "'s " + bodypartname + " has become crippled!")
    if diedinbattle != []:
        displaymessage = get_trigger_arg(bot, diedinbattle, "list")
        dispmsgarray.append(displaymessage + " died in this event.")
    adjust_database_value(bot, winner, 'coin', riskcoins)
    onscreentext(bot, [inchannel], dispmsgarray)

## Assault
def subcommand_assault(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    if bot.nick in canduelarray:
        canduelarray.remove(bot.nick)
    executedueling, executeduelingmsg = eventchecks(bot, canduelarray, commandortarget, instigator, currentduelplayersarray, inchannel)
    if not executedueling:
        osd_notice(bot, instigator, executeduelingmsg)
        return
    duelslockout = get_database_value(bot, duelrecorduser, 'duelslockout') or 0
    if duelslockout:
        lockoutsince = get_timesince_duels(bot, instigator, 'duelslockout')
        if lockoutsince < duel_lockout_timer:
            osd_notice(bot, instigator, "Duel(s) is/are currently in progress. You must wait. If this is an error, it should clear itself in 5 minutes.")
            return
        reset_database_value(bot, duelrecorduser, 'duelslockout')
    set_database_value(bot, duelrecorduser, 'duelslockout', now)
    if instigator in canduelarray:
        canduelarray.remove(instigator)
    displaymessage = get_trigger_arg(bot, canduelarray, "list")
    onscreentext(bot, inchannel, instigator + " Initiated a full channel " + commandortarget + " event. Good luck to " + displaymessage)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
    set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator'), instigator)
    lastfoughtstart = get_database_value(bot, instigator, 'lastfought')
    for astat in assault_results:
        reset_database_value(bot, instigator, "assault_" + astat)
    for player in canduelarray:
        for astat in assault_results:
            reset_database_value(bot, player, "assault_" + astat)
    duel_combat(bot, instigator, instigator, canduelarray, triggerargsarray, now, inchannel, 'assault', devenabledchannels)
    maindueler = instigator
    osd_notice(bot, maindueler, "It looks like the Full Channel Assault has completed.")
    assaultstatsarray = []
    assaultstatsarray.append(maindueler + "'s Full Channel Assault results:")
    for astat in assault_results:
        astateval = get_database_value(bot, instigator, "assault_" + astat) or 0
        if astateval:
            astatstr = str(str(astat) + " = " + str(astateval))
            assaultstatsarray.append(astatstr)
            reset_database_value(bot, instigator, "assault_" + astat)
    onscreentext(bot, [inchannel], assaultstatsarray)
    for player in canduelarray:
        for astat in assault_results:
            reset_database_value(bot, player, "assault_" + astat)

    set_database_value(bot, instigator, 'lastfought', lastfoughtstart)
    reset_database_value(bot, duelrecorduser, 'duelslockout')

    ## usage counter ## TODO use len(canduelarray)
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, instigator, 'usage_combat', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_combat', 1)

## Random Target
def subcommand_random(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    if instigator not in canduelarray:
        canduel, validtargetmsg = duelcriteria(bot, instigator, commandortarget, currentduelplayersarray, inchannel)
        osd_notice(bot, instigator, validtargetmsg)
        return
    if canduelarray == []:
        osd_notice(bot, instigator, "It looks like the full channel " + commandortarget + " event target finder has failed.")
        return
    duelslockout = get_database_value(bot, duelrecorduser, 'duelslockout') or 0
    if duelslockout:
        lockoutsince = get_timesince_duels(bot, instigator, 'duelslockout')
        if lockoutsince < duel_lockout_timer:
            osd_notice(bot, instigator, "Duel(s) is/are currently in progress. You must wait. If this is an error, it should clear itself in 5 minutes.")
            return
        reset_database_value(bot, duelrecorduser, 'duelslockout')
    set_database_value(bot, duelrecorduser, 'duelslockout', now)
    if bot.nick not in canduelarray:
        canduelarray.append(bot.nick)
    target = get_trigger_arg(bot, canduelarray, 'random')
    statreset(bot, target)
    duel_combat(bot, instigator, instigator, [target], triggerargsarray, now, inchannel, 'random', devenabledchannels)
    reset_database_value(bot, duelrecorduser, 'duelslockout')

    ## usage counter
    adjust_database_value(bot, instigator, 'usage_total', 1)
    adjust_database_value(bot, instigator, 'usage_combat', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_total', 1)
    adjust_database_value(bot, duelrecorduser, 'usage_combat', 1)

## Usage
def subcommand_usage(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    targetcom = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    targetcomname = targetcom
    if targetcom in validcommands or targetcom == 'combat':
        target = get_trigger_arg(bot, triggerargsarray, 3) or instigator
        targetname = target
        if target == 'channel':
            target = bot.nick
        totaluses = get_database_value(bot, target, 'usage_'+targetcom)
        target = actualname(bot, target)
        onscreentext(bot, inchannel, targetname + " has used duel " + str(targetcom) + " " + str(totaluses) + " times.")
        return
    if targetcom == 'channel':
        targetcom = bot.nick
    validtarget, validtargetmsg = targetcheck(bot, targetcom, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
    if not validtarget and targetcom != bot.nick:
        osd_notice(bot, instigator, validtargetmsg)
        return
    totaluses = get_database_value(bot, targetcom, 'usage_total')
    targetcom = actualname(bot, targetcomname)
    onscreentext(bot, inchannel, targetcom + " has used duels " + str(totaluses) + " times.")

## War Room
def subcommand_warroom(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    subcommand = get_trigger_arg(bot, triggerargsarray, 2).lower()
    if not subcommand:
        if instigator not in canduelarray:
            canduel, validtargetmsg = duelcriteria(bot, instigator, subcommand, currentduelplayersarray, inchannel)
            osd_notice(bot, instigator, validtargetmsg)
        else:
            osd_notice(bot, instigator, "It looks like you can duel.")
    elif subcommand == 'colosseum' or subcommand == 'assault':
        ## TODO new event types, maybe make an event array?
        ## TODO: alt commands
        executedueling, executeduelingmsg = eventchecks(bot, canduelarray, subcommand, instigator, currentduelplayersarray, inchannel)
        if not executedueling:
            osd_notice(bot, instigator, executeduelingmsg)
        else:
            osd_notice(bot, instigator, "It looks like full channel " + subcommand + " event can be used.")
    elif subcommand == 'list':
        if instigator in canduelarray:
            canduelarray.remove(instigator)
        if bot.nick in canduelarray:
            canduelarray.remove(bot.nick)
        if canduelarray != []:
            displaymessage = get_trigger_arg(bot, canduelarray, "list")
            onscreentext(bot, inchannel, instigator + ", you may duel the following users: "+ str(displaymessage ))
        else:
            osd_notice(bot, instigator, "It looks like nobody can duel at the moment.")
    else:
        validtarget, validtargetmsg = targetcheck(bot, subcommand, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        executedueling, executeduelingmsg = duelcriteria(bot, instigator, subcommand, currentduelplayersarray, inchannel)
        if not executedueling:
            osd_notice(bot, instigator, executeduelingmsg)
            return
        subcommand = actualname(bot, subcommand)
        if subcommand in canduelarray and instigator in canduelarray:
            osd_notice(bot, instigator, "It looks like you can duel " + subcommand + ".")

## Title
def subcommand_title(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    instigatortitle = get_database_value(bot, instigator, 'title')
    titletoset = get_trigger_arg(bot, triggerargsarray, "2+")
    if not titletoset:
        osd_notice(bot, instigator, "What do you want your title to be?")
    elif titletoset == 'remove':
        reset_database_value(bot, instigator, 'title')
        osd_notice(bot, instigator, "Your title has been removed.")
    else:
        titletoset = str(titletoset)
        instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
        if instigatorcoin < class_cost:
            osd_notice(bot, instigator, "Changing your title costs " + str(title_cost) + " coin. You need more funding.")
        elif len(titletoset) > 10:
            osd_notice(bot, instigator, "Purchased titles can be no longer than 10 characters.")
        else:
            set_database_value(bot, instigator, 'title', titletoset)
            adjust_database_value(bot, instigator, 'coin', -abs(title_cost))
            osd_notice(bot, instigator, "Your title is now " + titletoset + ".")

## Class
def subcommand_class(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    subcommandarray = ['set','change']
    classes = get_trigger_arg(bot, class_array, "list")
    subcommand = get_trigger_arg(bot, triggerargsarray, 2).lower()
    setclass = get_trigger_arg(bot, triggerargsarray, 3).lower()
    instigatorclass = get_database_value(bot, instigator, 'class_setting')
    instigatorfreebie = get_database_value(bot, instigator, 'class_freebie') or 0
    classtime = get_timesince_duels(bot, instigator, 'class_timeout')
    instigatorclasstime = get_timesince_duels(bot, instigator, 'class_timeout')
    instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
    if not instigatorclass and not subcommand:
        osd_notice(bot, instigator, "You don't appear to have a class set. Options are : " + classes + ". Run .duel class set    to set your class.")
    elif not subcommand:
        osd_notice(bot, instigator, "Your class is currently set to " + str(instigatorclass) + ". Use .duel class change    to change class. Options are : " + classes + ".")
    elif classtime < timeout_class and not inchannel in devenabledchannels:
        osd_notice(bot, instigator, "You may not change your class more than once per 24 hours. Please wait "+str(hours_minutes_seconds((timeout_class - instigatorclasstime)))+" to change.")
    elif subcommand not in subcommandarray:
        osd_notice(bot, instigator, "Invalid command. Options are set or change.")
    elif not setclass:
        osd_notice(bot, instigator, "Which class would you like to use? Options are: " + classes +".")
    elif instigatorcoin < class_cost and instigatorfreebie:
        osd_notice(bot, instigator, "Changing class costs " + str(class_cost) + " coin. You need more funding.")
    elif setclass not in class_array:
        osd_notice(bot, instigator, "Invalid class. Options are: " + classes +".")
    elif setclass == instigatorclass:
        osd_notice(bot, instigator, "Your class is already set to " + setclass + ".")
    else:
        set_database_value(bot, instigator, 'class_setting', setclass)
        osd_notice(bot, instigator, "Your class is now set to " + setclass + ".")
        set_database_value(bot, instigator, 'class_timeout', now)
        if instigatorfreebie:
            adjust_database_value(bot, instigator, 'coin', -abs(class_cost))
        else:
            set_database_value(bot, instigator, 'class_freebie', 1)

## Streaks
def subcommand_streaks(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    if int(tiercommandeval) > int(currenttier) and target != instigator:
        osd_notice(bot, instigator, "Streaks for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!")
        if not inchannel in devenabledchannels:
            return
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
        return
    target = actualname(bot, target)
    streak_type = get_database_value(bot, target, 'streak_type_current') or 'none'
    best_wins = get_database_value(bot, target, 'streak_win_best') or 0
    worst_losses = get_database_value(bot, target, 'streak_loss_best') or 0
    if streak_type == 'win':
        streak_count = get_database_value(bot, target, 'streak_win_current') or 0
        typeofstreak = 'winning'
    elif streak_type == 'loss':
        streak_count = get_database_value(bot, target, 'streak_loss_current') or 0
        typeofstreak = 'losing'
    else:
        streak_count = 0
    dispmsgarray = []
    if streak_count > 1 and streak_type != 'none':
        dispmsgarray.append("Currently on a " + typeofstreak + " streak of " + str(streak_count) + ".")
    if int(best_wins) > 1:
        dispmsgarray.append("Best Win streak= " + str(best_wins) + ".")
    if int(worst_losses) > 1:
        dispmsgarray.append("Worst Losing streak= " + str(worst_losses) + ".")
    if dispmsgarray != []:
        dispmsgarrayb = []
        dispmsgarrayb.append(target + "'s streaks:")
        for x in dispmsgarray:
            dispmsgarrayb.append(x)
    else:
        dispmsgarrayb.append(target + " has no streaks.")
    onscreentext(bot, ['say'], dispmsgarrayb)

## Stats
def subcommand_stats(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    if int(tiercommandeval) > int(currenttier) and target != instigator:
        osd_notice(bot, instigator, "Stats for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!")
        if not inchannel in devenabledchannels:
            return
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
        return
    target = actualname(bot, target)
    targetclass = get_database_value(bot, target, 'class_setting') or 'notclassy'
    dispmsgarray = []
    totalhealth = get_health(bot,target)
    if totalhealth:
        if targetclass == 'vampire':
            totalhealth = -abs(totalhealth)
        dispmsgarray.append("Health="+str(totalhealth))
    for x in stats_view:
        if x in stats_view_functions:
            scriptdef = str('get_' + x + '(bot,target)')
            gethowmany = eval(scriptdef)
        else:
            gethowmany = get_database_value(bot, target, x)
        if gethowmany:
            if x == 'winlossratio':
                gethowmany = format(gethowmany, '.3f')
            statname = x
            if statname == 'class_setting':
                statname = 'class'
            statname = statname.title()
            dispmsgarray.append(statname + "=" + str(gethowmany))
    dispmsgarrayb = []
    if dispmsgarray != []:
        pepper = get_pepper(bot, target)
        if not pepper or pepper == '':
            targetname = target
        else:
            targetname = str("(" + str(pepper.title()) + ") " + target)
        dispmsgarrayb.append(targetname + "'s " + commandortarget + ":")
        for y in dispmsgarray:
            dispmsgarrayb.append(y)
    else:
        dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  commandortarget + ".")
    onscreentext(bot, ['say'], dispmsgarrayb)

## Leaderboard
def subcommand_leaderboard(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    subcommand = get_trigger_arg(bot, triggerargsarray, 2)
    if bot.nick in currentduelplayersarray:
        currentduelplayersarray.remove(bot.nick)
    if not subcommand:
        leaderscript = []
        leaderboardarraystats = ['winlossratio','kills','respawns','health','streak_win_best','streak_loss_best','bounty']
        streak_loss_bestdispmsg, streak_loss_bestdispmsgb = "Worst Losing Streak:", ""
        winlossratiodispmsg, winlossratiodispmsgb = "Wins/Losses:", ""
        killsdispmsg, killsdispmsgb = "Most Kills:", "kills"
        respawnsdispmsg, respawnsdispmsgb = "Most Deaths:", "respawns"
        healthdispmsg, healthdispmsgb = "Closest To Death:", "health"
        streak_win_bestdispmsg, streak_win_bestdispmsgb = "Best Win Streak:", ""
        bountydispmsg, bountydispmsgb = "Largest Bounty:", "coins"
        for x in leaderboardarraystats:
            playerarray = []
            statvaluearray = []
            for u in currentduelplayersarray:
                if x != 'winlossratio' and x != 'health':
                    statamount = get_database_value(bot, u, x)
                else:
                    scriptdef = str('get_' + x + '(bot,u)')
                    statamount = eval(scriptdef)
                if statamount > 0:
                    playerarray.append(u)
                    statvaluearray.append(statamount)
            if playerarray != [] and statvaluearray != []:
                zip(*sorted(zip(statvaluearray, playerarray)))
                if x == 'health':
                    statleadername = get_trigger_arg(bot, playerarray, 'last')
                    statleadernumber = get_trigger_arg(bot, statvaluearray, 'last')
                    leaderclass = get_database_value(bot, statleadername, 'class_setting') or 'notclassy'
                    if leaderclass == 'vampire':
                        statleadernumber = int(statleadernumber)
                        statleadernumber = -abs(statleadernumber)
                elif x == 'winlossratio':
                    statleadername = get_trigger_arg(bot, playerarray, 1)
                    statleadernumber = get_trigger_arg(bot, statvaluearray, 1)
                    statleadernumber = format(statleadernumber, '.3f')
                else:
                    statleadername = get_trigger_arg(bot, playerarray, 1)
                    statleadernumber = get_trigger_arg(bot, statvaluearray, 1)
                leaderscript.append(eval(x+"dispmsg") + " "+ statleadername + " at "+ str(statleadernumber)+ " "+ eval(x+"dispmsgb"))
        if leaderscript == []:
            leaderscript.append("Leaderboard appears to be empty")
        onscreentext(bot, ['say'], leaderscript)
        return
    if subcommand.lower() != 'highest' and subcommand.lower() != 'lowest':
        osd_notice(bot, instigator, "Invalid Command.")
        return
    subcommand = subcommand.lower()
    subcommanda = get_trigger_arg(bot, triggerargsarray, 3)
    if not subcommanda:
        onscreentext(bot, inchannel, "What stat do you want to check?")
        return
    subcommanda = subcommanda.lower()
    duelstatsadminarray = duels_valid_stats(bot)
    if subcommanda.lower() not in duelstatsadminarray and subcommanda.lower() != 'health':
        onscreentext(bot, inchannel, "This stat is either not comparable at the moment or invalid.")
        return
    playerarray = []
    statvaluearray = []
    for u in currentduelplayersarray:
        if subcommanda.lower() != 'winlossratio' and subcommanda.lower() != 'health':
            statamount = get_database_value(bot, u, subcommanda.lower())
        else:
            scriptdef = str('get_' + subcommanda.lower() + '(bot,u)')
            statamount = eval(scriptdef)
        if statamount > 0:
            playerarray.append(u)
            statvaluearray.append(statamount)
    if playerarray != [] and statvaluearray != []:
        zip(*sorted(zip(statvaluearray, playerarray)))
        if subcommand.lower() == 'highest':
            statleadername = get_trigger_arg(bot, playerarray, 1)
            statleadernumber = get_trigger_arg(bot, statvaluearray, 1)
        else:
            statleadername = get_trigger_arg(bot, playerarray, 'last')
            statleadernumber = get_trigger_arg(bot, statvaluearray, 'last')
        if subcommanda.lower() == 'health':
            leaderclass = get_database_value(bot, statleadername, 'class_setting') or 'notclassy'
            if leaderclass == 'vampire':
                statleadernumber = int(statleadernumber)
                statleadernumber = -abs(statleadernumber)
        onscreentext(bot, inchannel, "The " + subcommand + " amount for "+ subcommanda+ " is " + statleadername+ " with "+ str(statleadernumber) + ".")
    else:
        onscreentext(bot, inchannel, "There doesn't appear to be a "+ subcommand + " amount for "+subcommanda+".")

## Armor
def subcommand_armor(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    subcommand = get_trigger_arg(bot, triggerargsarray, 2)
    typearmor = get_trigger_arg(bot, triggerargsarray, 3)
    instigatorclass = get_database_value(bot, instigator, 'class_setting')
    if not subcommand or subcommand.lower() in [x.lower() for x in dueloptedinarray]:
        target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        target = actualname(bot, target)
        dispmsgarray = []
        for x in stats_armor:
            gethowmany = get_database_value(bot, target, x)
            if gethowmany:
                xname = x.replace("_", " ")
                xname = xname.title()
                if gethowmany > armor_durability:
                    xname = str("Enhanced " + xname)
                dispmsgarray.append(str(xname) + "=" + str(gethowmany))
        dispmsgarrayb = []
        if dispmsgarray != []:
            dispmsgarrayb.append(target + "'s " + commandortarget + " durability:")
            for y in dispmsgarray:
                dispmsgarrayb.append(y)
        else:
            dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  commandortarget + ".")
        onscreentext(bot, ['say'], dispmsgarrayb)
    elif subcommand == 'buy':
        instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
        costinvolved = armor_cost
        if instigatorclass == 'blacksmith':
            costinvolved = costinvolved * armor_cost_blacksmith_cut
        costinvolved = int(costinvolved)
        if not typearmor or "armor_"+typearmor not in stats_armor:
            armors = get_trigger_arg(bot, stats_armor, 'list')
            onscreentext(bot, inchannel, "What type of armor do you wish to " + subcommand + "? Options are: " + armors + ".")
        elif instigatorcoin < costinvolved:
            onscreentext(bot, inchannel, "Insufficient Funds.")
        else:
            getarmor = get_database_value(bot, instigator, "armor_"+typearmor) or 0
            if getarmor and getarmor > 0:
                onscreentext(bot, inchannel, "It looks like you already have a " + typearmor + ".")
            else:
                onscreentext(bot, inchannel, instigator + " bought " + typearmor + " for " + str(costinvolved) + " coins.")
                adjust_database_value(bot, instigator, 'coin', -abs(costinvolved))
                set_database_value(bot, instigator, "armor_"+typearmor, armor_durability)
    elif subcommand == 'sell':
        if not typearmor or "armor_"+typearmor not in stats_armor:
            armors = get_trigger_arg(bot, stats_armor, 'list')
            onscreentext(bot, inchannel, "What type of armor do you wish to " + subcommand + "? Options are: " + armors + ".")
        else:
            getarmor = get_database_value(bot, instigator, "armor_"+typearmor) or 0
            if not getarmor:
                onscreentext(bot, inchannel, "You don't have a " + typearmor + " to sell.")
            elif getarmor < 0:
                onscreentext(bot, inchannel, "Your armor is too damaged to sell.")
                reset_database_value(bot, instigator, "armor_"+typearmor)
            else:
                durabilityremaining = getarmor / armor_durability
                sellingamount = durabilityremaining * armor_cost
                if instigatorclass == 'blacksmith':
                    sellingamount = sellingamount * armor_sell_blacksmith_cut
                sellingamount = int(sellingamount)
                if sellingamount <= 0:
                    onscreentext(bot, inchannel, "Your armor is too damaged to sell.")
                else:
                    onscreentext(bot, inchannel, "Selling your "+typearmor +" earned you " + str(sellingamount) + " coins.")
                    adjust_database_value(bot, instigator, 'coin', sellingamount)
                    reset_database_value(bot, instigator, "armor_"+typearmor)
    elif subcommand == 'repair':
        if not typearmor or "armor_"+typearmor not in stats_armor:
            armors = get_trigger_arg(bot, stats_armor, 'list')
            onscreentext(bot, inchannel, "What type of armor do you wish to " + subcommand + "? Options are: " + armors + ".")
        else:
            getarmor = get_database_value(bot, instigator, "armor_"+typearmor) or 0
            durabilitycompare = armor_durability
            if instigatorclass == 'blacksmith':
                durabilitycompare = armor_durability_blacksmith
            if not getarmor:
                onscreentext(bot, inchannel, "You don't have a " + typearmor + " to repair.")
            elif getarmor >= durabilitycompare:
                onscreentext(bot, inchannel, "It looks like your armor does not need repair.")
            else:
                durabilitytorepair = durabilitycompare - getarmor
                if durabilitytorepair <= 0:
                    onscreentext(bot, inchannel, "Looks like you can't repair that right now.")
                else:
                    instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
                    costinvolved  = durabilitytorepair / durabilitycompare
                    costinvolved = costinvolved * armor_cost
                    costinvolved = costinvolved * armor_repair_cost
                    if instigatorclass == 'blacksmith':
                        costinvolved = costinvolved * armor_cost_blacksmith_cut
                    costinvolved = int(costinvolved)
                    if instigatorcoin < costinvolved:
                        onscreentext(bot, inchannel, "Insufficient Funds.")
                    else:
                        onscreentext(bot, inchannel, typearmor + " repaired  for " + str(costinvolved)+" coins.")
                        adjust_database_value(bot, instigator, 'coin', -abs(costinvolved))
                        set_database_value(bot, instigator, "armor_"+typearmor, durabilitycompare)

## Bounty
def subcommand_bounty(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    target = get_trigger_arg(bot, triggerargsarray, 2)
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
        return
    target = actualname(bot, target)
    amount = get_trigger_arg(bot, triggerargsarray, 3)
    if not str(amount).isdigit():
        osd_notice(bot, instigator, "Invalid Amount.")
        return
    amount = int(amount)
    if not amount:
        osd_notice(bot, instigator, "How much of a bounty do you wish to place on "+target+".")
        return
    instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
    if int(instigatorcoin) < int(amount):
        osd_notice(bot, instigator, "Insufficient Funds.")
        return
    adjust_database_value(bot, instigator, 'coin', -abs(amount))
    bountyontarget = get_database_value(bot, target, 'bounty') or 0
    if not bountyontarget:
       onscreentext(bot, inchannel, instigator + " places a bounty of " + str(amount) + " on " + target + ".")
    else:
       onscreentext(bot, inchannel, instigator + " adds " + str(amount) + " to the bounty on " + target + ".")
    adjust_database_value(bot, target, 'bounty', amount)

## Loot ## TODO
def subcommand_loot(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    instigatorclass = get_database_value(bot, instigator, 'class_setting')
    instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
    lootcommand = get_trigger_arg(bot, triggerargsarray, 2).lower()
    if not lootcommand or lootcommand.lower() in [x.lower() for x in dueloptedinarray]:
        target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
        if int(tiercommandeval) > int(currenttier) and target != instigator:
            osd_notice(bot, instigator, "Loot for other players cannot be viewed until somebody reaches " + str(tierpepperrequired.title()) + ". "+str(tiermath) + " tier(s) remaining!")
            if not inchannel in devenabledchannels:
                return
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        target = actualname(bot, target)
        dispmsgarray = []
        for x in loot_view:
            gethowmany = get_database_value(bot, target, x)
            if gethowmany:
                xname = x.title()
                if gethowmany == 1:
                    loottype = str(xname)
                else:
                    loottype = str(str(xname)+"s")
                dispmsgarray.append(str(loottype) + "=" + str(gethowmany))
        dispmsgarrayb = []
        if dispmsgarray != []:
            dispmsgarrayb.append(target + "'s " + commandortarget + ":")
            for y in dispmsgarray:
                dispmsgarrayb.append(y)
        else:
            dispmsgarrayb.append(instigator + ", It looks like " + target + " has no " +  commandortarget + ".")
        onscreentext(bot, ['say'], dispmsgarrayb)
    elif lootcommand == 'use':
        lootitem = get_trigger_arg(bot, triggerargsarray, 3).lower()
        gethowmanylootitem = get_database_value(bot, instigator, "loot_"+lootitem) or 0
        if not lootitem:
            osd_notice(bot, instigator, "What do you want to " + str(lootcommand) + "?")
        elif lootitem not in potion_types and lootitem != 'grenade':
            osd_notice(bot, instigator, "Invalid loot item.")
        elif not gethowmanylootitem:
            osd_notice(bot, instigator, "You do not have any " +  lootitem + "!")
        elif lootitem == 'magicpotion':
            osd_notice(bot, instigator, "Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
        elif lootitem == 'grenade':
            if not inchannel.startswith("#"):
                osd_notice(bot, instigator, "Grenades must be used in channel.")
                return
            instigatorgrenade = get_database_value(bot, instigator, 'grenade') or 0
            if instigator in canduelarray:
                canduelarray.remove(instigator)
            if bot.nick in canduelarray:
                canduelarray.remove(bot.nick)
            if canduelarray == []:
                osd_notice(bot, instigator, "It looks like using a grenade right now won't hurt anybody.")
            else:
                dispmsgarray = []
                adjust_database_value(bot, instigator, "loot_"+lootitem, -1)
                fulltarget, secondarytarget, thirdtarget = '','',''
                fulltarget = get_trigger_arg(bot, canduelarray, "random")
                dispmsgarray.append(fulltarget + " takes the brunt of the grenade dealing " + str(abs(grenade_full_damage)) + " damage.")
                canduelarray.remove(fulltarget)
                if canduelarray != []:
                    secondarytarget = get_trigger_arg(bot, canduelarray, "random")
                    canduelarray.remove(secondarytarget)
                    if canduelarray != []:
                        thirdtarget = get_trigger_arg(bot, canduelarray, "random")
                        dispmsgarray.append(secondarytarget + " and " + thirdtarget + " jump away but still take " + str(abs(grenade_secondary_damage)) + " damage.")
                        canduelarray.remove(thirdtarget)
                        if canduelarray != []:
                            remainingarray = get_trigger_arg(bot, canduelarray, "list")
                            dispmsgarray.append(remainingarray + " completely jump out of the way")
                    else:
                        dispmsgarray.append(secondarytarget + " jumps away but still takes " + str(abs(grenade_secondary_damage)) + " damage.")
                painarray = []
                damagearray = []
                deatharray = []
                if fulltarget != '':
                    painarray.append(fulltarget)
                    damagearray.append(grenade_full_damage)
                if secondarytarget != '':
                    painarray.append(secondarytarget)
                    damagearray.append(grenade_secondary_damage)
                if thirdtarget != '':
                    painarray.append(thirdtarget)
                    damagearray.append(grenade_secondary_damage)
                diedinbattle = []
                for player, damage in zip(painarray, damagearray):
                    damage = int(damage)
                    damagescale = tierratio_level(bot)
                    damage = damagescale * damage
                    bodypart, bodypartname = bodypart_select(bot, player)
                    damage, damagetextarray = damage_resistance(bot, player, damage, bodypart, bodypartname)
                    for j in damagetextarray:
                        dispmsgarray.append(j)
                    if damage > 0:
                        splitdamage = int(damage) / 6
                        for part in stats_healthbodyparts:
                            adjust_database_value(bot, x, part, -abs(splitdamage))
                        loserheadhealth = get_database_value(bot, loser, 'head')
                        losertorsohealth = get_database_value(bot, loser, 'health_torso')
                        if loserheadhealth  <= 0 or losertorsohealth <= 0:
                            winnertextarray = whokilledwhom(bot, instigator, player)
                            diedinbattle.append(player)
                        else:
                            for part in stats_healthbodyparts:
                                losercurrenthealthbody  = get_database_value(bot, loser, part)
                                if losercurrenthealthbody  <= 0:
                                    bodypartname = bodypartname.replace("_", " ")
                                    dispmsgarray.append(loser + "'s " + bodypartname + " has become crippled!")
                if diedinbattle != []:
                    displaymessage = get_trigger_arg(bot, diedinbattle, "list")
                    dispmsgarray.append(displaymessage + " died by this grenade volley.")
                onscreentext(bot, [inchannel], dispmsgarray)
        else:
            targnum = get_trigger_arg(bot, triggerargsarray, 4).lower()
            if not targnum:
                quantity = 1
                target = instigator
            elif targnum.isdigit():
                quantity = int(targnum)
                target = instigator
            elif targnum.lower() in [x.lower() for x in dueloptedinarray]:
                targnumb = get_trigger_arg(bot, triggerargsarray, 5).lower()
                target = targnum
                if not targnumb:
                    quantity = 1
                elif targnumb.isdigit():
                    quantity = int(targnumb)
                elif targnumb == 'all':
                    quantity = int(gethowmanylootitem)
                else:
                    osd_notice(bot, inchannel, "Invalid command.")
                    return
            elif targnum == 'all':
                target = instigator
                quantity = int(gethowmanylootitem)
            else:
                osd_notice(bot, inchannel, "Invalid command.")
                return
            if not quantity:
                onscreentext(bot, inchannel, "Invalid command.")
                return
            if target == bot.nick:
                osd_notice(bot, instigator, "I am immune to " + lootitem + ".")
                return
            validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
            if not validtarget:
                osd_notice(bot, instigator, validtargetmsg)
                return
            target = actualname(bot, target)
            targetclass = get_database_value(bot, target, 'class_setting') or 'notclassy'
            if int(gethowmanylootitem) < int(quantity):
                osd_notice(bot, instigator, "You do not have enough " +  lootitem + " to use this command!")
                return
            if target.lower() != instigator.lower() and targetclass == 'fiend':
                osd_notice(bot, instigator, "It looks like " + target + " is a fiend and can only self-use potions.")
                adjust_database_value(bot, instigator, "loot_"+lootitem, -abs(quantity))
                return
            uselootarray = []
            adjust_database_value(bot, instigator, "loot_"+lootitem, -abs(quantity))
            lootusedeaths = 0
            if lootitem == 'mysterypotion':
                while int(quantity) > 0:
                    quantity = quantity - 1
                    loot = get_trigger_arg(bot, potion_types, 'random')
                    if loot == 'mysterypotion' or loot == 'magicpotion':
                        loot = get_trigger_arg(bot, loot_null, 'random')
                    uselootarray.append(loot)
            else:
                while int(quantity) > 0:
                    quantity = quantity - 1
                    uselootarray.append(lootitem)
            uselootarraytotal = len(uselootarray)
            extramsg = '.'
            if lootitem == 'healthpotion':
                if targetclass == 'barbarian':
                    potionmaths = int(uselootarraytotal) * healthpotion_worth_barbarian
                else:
                    potionmaths = int(uselootarraytotal) * healthpotion_worth
                extramsg = str(" restoring " + str(potionmaths) + " health.")
            elif lootitem == 'poisonpotion':
                poisonpotionworthb = abs(poisonpotion_worth)
                potionmaths = int(uselootarraytotal) * int(poisonpotionworthb)
                extramsg = str(" draining " + str(potionmaths) + " health.")
            elif lootitem == 'manapotion':
                if targetclass == 'mage':
                    potionmaths = int(uselootarraytotal) * manapotion_worth_mage
                else:
                    potionmaths = int(uselootarraytotal) * manapotion_worth
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
                        splitdamage = healthpotion_worth_barbarian / 6
                        for part in stats_healthbodyparts:
                            adjust_database_value(bot, target, part, splitdamage)
                    else:
                        splitdamage = healthpotion_worth / 6
                        for part in stats_healthbodyparts:
                            adjust_database_value(bot, target, part, splitdamage)
                elif x == 'poisonpotion':
                    splitdamage = poisonpotion_worth / 6
                    for part in stats_healthbodyparts:
                        adjust_database_value(bot, target, part, splitdamage)
                elif x == 'manapotion':
                    if targetclass == 'mage':
                        adjust_database_value(bot, target, 'mana', manapotion_worth_mage)
                    else:
                        adjust_database_value(bot, target, 'mana', manapotion_worth)
                elif x == 'timepotion':
                    reset_database_value(bot, target, 'lastfought')
                    reset_database_value(bot, duelrecorduser, 'timeout_timeout')
                    for k in timepotiontargetarray:
                        targetequalcheck = get_database_value(bot, bot.nick, k) or bot.nick
                        if targetequalcheck == target:
                            reset_database_value(bot, bot.nick, k)
                    for j in timepotiontimeoutarray:
                        reset_database_value(bot, target, j)
                    reset_database_value(bot, bot.nick, 'timeout_timeout')
                    targetheadhealth = get_database_value(bot, target, 'head')
                    targettorsohealth = get_database_value(bot, target, 'health_torso')
                    if targetheadhealth  <= 0 or targettorsohealth <= 0:
                        if target == instigator:
                            deathmsgb = suicidekill(bot,loser) ## TODO array
                        else:
                            deathmsgb = whokilledwhom(bot, instigator, target) or ''  ## TODO array
                        lootusedeaths = lootusedeaths + 1
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
                postionsusedarray = get_trigger_arg(bot, actualpotionmathedarray, "list")
                mainlootusemessage = str(mainlootusemessage + " Potion(s) used: " + postionsusedarray)
            if lootusedeaths > 0:
                if lootusedeaths == 1:
                    mainlootusemessage = str(mainlootusemessage + " This resulted in death.")
                else:
                    mainlootusemessage = str(mainlootusemessage + " This resulted in "+str(lootusedeaths)+" deaths.")
            onscreentext(bot, inchannel, mainlootusemessage)
            if target != instigator and not inchannel.startswith("#"):
                osd_notice(bot, target, mainlootusemessage)
    elif lootcommand == 'buy':
        lootitem = get_trigger_arg(bot, triggerargsarray, 3).lower()
        if not lootitem:
            osd_notice(bot, instigator, "What do you want to " + str(lootcommand) + "?")
        elif lootitem not in potion_types and lootitem != 'grenade':
            osd_notice(bot, instigator, "Invalid loot item.")
        elif lootitem == 'magicpotion':
            osd_notice(bot, instigator, "Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
        else:
            quantity = get_trigger_arg(bot, triggerargsarray, 4).lower() or 1
            if quantity == 'all':
                if instigatorclass == 'scavenger':
                    quantity = int(instigatorcoin) / loot_buy_scavenger
                else:
                    quantity = int(instigatorcoin) / loot_buy_scavenger
                if not quantity > 1:
                    osd_notice(bot, instigator, "You do not have enough coin for this action.")
                    return
            quantity = int(quantity)
            if instigatorclass == 'scavenger':
                coinrequired = loot_buy_scavenger * int(quantity)
            else:
                coinrequired = loot_buy * int(quantity)
            if instigatorcoin < coinrequired:
                osd_notice(bot, instigator, "You do not have enough coin for this action.")
            else:
                adjust_database_value(bot, instigator, 'coin', -abs(coinrequired))
                adjust_database_value(bot, instigator, "loot_"+lootitem, quantity)
                onscreentext(bot, instigator, instigator + " bought " + str(quantity) +  " "+lootitem + "s for " +str(coinrequired)+ " coins.")
    elif lootcommand == 'sell':
        lootitem = get_trigger_arg(bot, triggerargsarray, 3).lower()
        gethowmanylootitem = get_database_value(bot, instigator, "loot_"+lootitem) or 0
        if not lootitem:
            osd_notice(bot, instigator, "What do you want to " + str(lootcommand) + "?")
        elif lootitem not in potion_types and lootitem != 'grenade':
            osd_notice(bot, instigator, "Invalid loot item.")
        elif not gethowmanylootitem:
            osd_notice(bot, instigator, "You do not have any " +  lootitem + "!")
        elif lootitem == 'magicpotion':
            onscreentext(bot, inchannel, "Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
        else:
            quantity = get_trigger_arg(bot, triggerargsarray, 4).lower() or 1
            if quantity == 'all':
                quantity = gethowmanylootitem
            if int(quantity) > gethowmanylootitem:
                osd_notice(bot, instigator, "You do not have enough " + lootitem + " for this action.")
            else:
                quantity = int(quantity)
                if instigatorclass == 'scavenger':
                    reward = loot_sell_scavenger * int(quantity)
                else:
                    reward = loot_sell * int(quantity)
                adjust_database_value(bot, instigator, 'coin', reward)
                adjust_database_value(bot, instigator, "loot_"+lootitem, -abs(quantity))
                onscreentext(bot, inchannel, instigator + " sold " + str(quantity) + " "+ lootitem + "s for " +str(reward)+ " coins.")
    elif lootcommand == 'trade':
        lootitem = get_trigger_arg(bot, triggerargsarray, 3).lower()
        lootitemb = get_trigger_arg(bot, triggerargsarray, 4).lower()
        if not lootitem or not lootitemb:
            osd_notice(bot, instigator, "What do you want to " + str(lootcommand) + "?")
        elif lootitem not in potion_types or lootitemb not in potion_types:
            osd_notice(bot, instigator, "Invalid loot item.")
        elif lootitem == 'grenade' or lootitemb == 'grenade':
            osd_notice(bot, instigator, "You can't trade for grenades.")
        elif lootitemb == lootitem:
            osd_notice(bot, instigator, "You can't trade for the same type of potion.")
        else:
            gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
            quantity = get_trigger_arg(bot, triggerargsarray, 5).lower() or 1
            if lootitem == 'magicpotion':
                tradingratio = 1
            elif instigatorclass == 'scavenger':
                tradingratio = loot_trade_scavenger
            else:
                tradingratio = loot_trade
            if quantity == 'all':
                quantity = gethowmanylootitem / tradingratio
            if quantity <= 0:
                osd_notice(bot, instigator, "You do not have enough "+lootitem+" for this action.")
                return
            quantitymath = tradingratio * int(quantity)
            if gethowmanylootitem < quantitymath:
                osd_notice(bot, instigator, "You don't have enough of this item to trade.")
            else:
                adjust_database_value(bot, instigator, "loot_"+lootitem, -abs(quantitymath))
                adjust_database_value(bot, instigator, "loot_"+lootitemb, quantity)
                quantity = int(quantity)
                onscreentext(bot, inchannel, instigator + " traded " + str(quantitymath) + " "+ lootitem + "s for " +str(quantity) + " "+ lootitemb+ "s.")
    else:
        transactiontypesarraylist = get_trigger_arg(bot, loot_transaction_types, "list")
        osd_notice(bot, instigator, "It looks like " + lootcommand + " is either not here, not a valid person, or an invalid command. Valid commands are: " + transactiontypesarraylist + ".")

## Weaponslocker ## TODO
def subcommand_weaponslocker(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    target = get_trigger_arg(bot, triggerargsarray, 2) or instigator
    validdirectionarray = ['total','inv','add','del','reset']
    if target in validdirectionarray:
        target = instigator
        adjustmentdirection = get_trigger_arg(bot, triggerargsarray, 2).lower()
        weaponchange = get_trigger_arg(bot, triggerargsarray, '3+')
    else:
        adjustmentdirection = get_trigger_arg(bot, triggerargsarray, 3).lower()
        weaponchange = get_trigger_arg(bot, triggerargsarray, '4+')
    weaponslist = get_database_value(bot, target, 'weaponslocker_complete') or []
    validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
    if not validtarget:
        osd_notice(bot, instigator, validtargetmsg)
        return
    target = actualname(bot, target)
    if not adjustmentdirection:
        osd_notice(bot, instigator, "Use .duel weaponslocker add/del to adjust Locker Inventory.")
    elif adjustmentdirection == 'total':
        gethowmany = get_database_array_total(bot, target, 'weaponslocker_complete')
        onscreentext(bot, inchannel, target + ' has ' + str(gethowmany) + " weapons in their locker. They Can be viewed in privmsg by running .duel weaponslocker inv .")
    elif adjustmentdirection == 'inv':
        if weaponslist == []:
            osd_notice(bot, instigator, "There doesnt appear to be anything in the weapons locker! Use .duel weaponslocker add/del to adjust Locker Inventory.")
            return
        howmanyweapons = len(weaponslist)
        weaponsonscreenarray = []
        for weapon in weaponslist:
            howmanyweapons = howmanyweapons - 1
            if howmanyweapons > 0:
                weapon = str(weapon+",")
            weaponsonscreenarray.append(weapon)
        onscreentext(bot, [instigator], weaponsonscreenarray)
    elif target != instigator and not trigger.admin:
        osd_notice(bot, instigator, "You may not adjust somebody elses locker.")
    elif adjustmentdirection == 'reset':
        reset_database_value(bot, target, 'weaponslocker_complete')
        osd_notice(bot, instigator, "Locker Reset.")
    else:
        if not weaponchange:
            osd_notice(bot, instigator, "What weapon would you like to add/remove?")
        elif adjustmentdirection != 'add' and adjustmentdirection != 'del':
            onscreentext(bot, inchannel, "Invalid Command.")
        elif adjustmentdirection == 'add' and weaponchange in weaponslist:
            osd_notice(bot, instigator, weaponchange + " is already in weapons locker.")
        elif adjustmentdirection == 'del' and weaponchange not in weaponslist:
            osd_notice(bot, instigator, weaponchange + " is already not in weapons locker.")
        elif adjustmentdirection == 'add' and len(weaponchange) > weapon_name_length:
            osd_notice(bot, instigator, "That weapon exceeds the character limit of "+str(weapon_name_length)+".")
        else:
            if adjustmentdirection == 'add':
                weaponlockerstatus = 'now'
            else:
                weaponlockerstatus = 'no longer'
            adjust_database_array(bot, target, [weaponchange], 'weaponslocker_complete', adjustmentdirection)
            message = str(weaponchange + " is " + weaponlockerstatus + " in weapons locker.")
            osd_notice(bot, instigator, message)

## Magic ## TODO
def subcommand_magic(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    instigatorclass = get_database_value(bot, instigator, 'class_setting')
    instigatormana = get_database_value(bot, instigator, 'mana')
    magicusage = get_trigger_arg(bot, triggerargsarray, 2)
    if not magicusage or magicusage not in magic_types:
        magicoptions = get_trigger_arg(bot, magic_types, 'list')
        onscreentext(bot, inchannel, "Magic uses include: " + magicoptions + ".")
    else:
        targnum = get_trigger_arg(bot, triggerargsarray, 3).lower()
        if not targnum:
            quantity = 1
            target = instigator
        elif targnum.isdigit():
            quantity = int(targnum)
            target = instigator
        elif targnum.lower() in [x.lower() for x in dueloptedinarray]:
            targnumb = get_trigger_arg(bot, triggerargsarray, 4).lower()
            target = targnum
            if not targnumb:
                quantity = 1
            elif targnumb.isdigit():
                quantity = int(targnumb)
            elif targnumb == 'all':
                quantity = int(gethowmanylootitem)
            else:
                onscreentext(bot, inchannel, "Invalid command.")
                return
        if not instigatormana:
            osd_notice(bot, instigator, "You don't have any mana.")
            return
        validtarget, validtargetmsg = targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands)
        if not validtarget:
            osd_notice(bot, instigator, validtargetmsg)
            return
        if target == bot.nick:
            osd_notice(bot, instigator, "I am immune to magic " + magicusage + ".")
            return
        target = actualname(bot, target)
        targetclass = get_database_value(bot, target, 'class_setting') or 'notclassy'
        if target.lower() != instigator.lower() and targetclass == 'fiend':
            osd_notice(bot, instigator, "It looks like " + target + " is a fiend and can only self-use magic.")
            manarequired = -abs(manarequired)
            adjust_database_value(bot, instigator, 'mana', manarequired)
            return
        targetcurse = get_database_value(bot, target, 'curse') or 0
        if magicusage == 'curse' and targetcurse:
            osd_notice(bot, instigator, "It looks like " + target + " is already cursed.")
            return
        if magicusage == 'curse':
            manarequired = magic_mana_required_curse
        elif magicusage == 'shield':
            manarequired = magic_mana_required_shield
        else:
            return
        if instigatorclass == 'mage':
            manarequired = manarequired * magic_usage_mage
        actualmanarequired = int(manarequired) * int(quantity)
        if int(actualmanarequired) > int(instigatormana):
            manamath = int(int(actualmanarequired) - int(instigatormana))
            osd_notice(bot, instigator, "You need " + str(manamath) + " more mana to use magic " + magicusage + ".")
        else:
            specialtext = ''
            manarequired = -abs(actualmanarequired)
            adjust_database_value(bot, instigator, 'mana', manarequired)
            if magicusage == 'curse':
                damagedealt = magic_curse_damage * int(quantity)
                set_database_value(bot, target, 'curse', magic_curse_duration)
                specialtext = str("which forces " + target + " to lose the next " + str(magic_curse_duration) + " duels.")
                splitdamage = int(damagedealt) / 6
                for part in stats_healthbodyparts:
                    adjust_database_value(bot, target, part, -abs(splitdamage))
            elif magicusage == 'shield':
                damagedealt = magic_shield_health * int(quantity)
                actualshieldduration = int(quantity) * int(magic_shield_duration)
                adjust_database_value(bot, target, 'shield', actualshieldduration)
                specialtext = str("which allows " + target + " to take no damage for the duration of " + str(actualshieldduration) + " damage AND restoring " +str(abs(damagedealt)) + " health.")
                splitdamage = int(damagedealt) / 6
                for part in stats_healthbodyparts:
                    adjust_database_value(bot, target, part, splitdamage)
            if instigator == target:
                displaymsg = str(instigator + " uses magic " + magicusage + " " + specialtext + ".")
            else:
                displaymsg = str(instigator + " uses magic " + magicusage + " on " + target + " " + specialtext + ".")
            onscreentext(bot, inchannel, displaymsg)
            if not inchannel.startswith("#") and target != instigator:
                osd_notice(bot, instigator, displaymsg)
            instigatormana = get_database_value(bot, instigator, 'mana')
            if instigatormana <= 0:
                reset_database_value(bot, instigator, 'mana')

## Admin ## TODO
def subcommand_admin(bot, instigator, triggerargsarray, botvisibleusers, currentuserlistarray, dueloptedinarray, commandortarget, now, trigger, currenttier, inchannel, currentduelplayersarray, canduelarray, fullcommandused, tiercommandeval, tierpepperrequired, tiermath, devenabledchannels, validcommands):
    subcommand = get_trigger_arg(bot, triggerargsarray, 2).lower()
    if subcommand not in validcommands and subcommand != 'bugbounty' and subcommand != 'channel':
        osd_notice(bot, instigator, "What Admin adjustment do you want to make?")
        return
    if subcommand == 'on' or subcommand == 'off':
        target = get_trigger_arg(bot, triggerargsarray, 3).lower() or instigator
        if target == 'everyone':
            if subcommand == 'on':
                adjust_database_array(bot, duelrecorduser, botvisibleusers, 'duelusers', 'add')
            else:
                reset_database_value(bot, duelrecorduser, 'duelusers')
            osd_notice(bot, instigator, "Duels should now be " +  subcommand + ' for ' + target +".")
            return
        if subcommand == 'on':
            adjust_database_array(bot, duelrecorduser, [target], 'duelusers', 'add')
        else:
            adjust_database_array(bot, duelrecorduser, [target], 'duelusers', 'del')
        set_database_value(bot, target, 'timeout_opttime', now)
        osd_notice(bot, instigator, "Duels should now be " +  subcommand + ' for ' + target +".")
    elif subcommand == 'tier':
        command = get_trigger_arg(bot, triggerargsarray, 3).lower()
        if not command:
            osd_notice(bot, instigator, "What did you intend to do with tiers?")
            return
        target = get_trigger_arg(bot, triggerargsarray, 4).lower() or instigator
        if target == 'channel':
            target = duelrecorduser
        if command == 'view':
            viewedtier = get_database_value(bot, target, 'tier')
            osd_notice(bot, instigator, target + " is at tier " + str(viewedtier) + ".")
        elif command == 'reset':
            osd_notice(bot, instigator, target + "'s tier has been reset.")
            reset_database_value(bot, target, 'tier')
        elif command == 'set':
            newsetting = get_trigger_arg(bot, triggerargsarray, 5)
            if not newsetting or not newsetting.isdigit():
                osd_notice(bot, instigator, "You must specify a number setting.")
                return
            osd_notice(bot, instigator, target + "'s tier has been set to " + str(newsetting) + ".")
            set_database_value(bot, target, 'tier', int(newsetting))
        else:
            osd_notice(bot, instigator, "This looks to be an invalid command.")
    elif subcommand == 'bugbounty':
        target = get_trigger_arg(bot, triggerargsarray, 3).lower() or instigator
        onscreentext(bot, inchannel, target + ' is awarded ' + str(bugbounty_reward) + " coin for finding a bug in duels.")
        adjust_database_value(bot, target, 'coin', bugbounty_reward)
    elif subcommand == 'roulette':
        command = get_trigger_arg(bot, triggerargsarray, 3).lower()
        if command != 'reset':
            osd_notice(bot, instigator, "What did you intend to do with roulette?")
            return
        osd_notice(bot, instigator, "Roulette should now be reset.")
        reset_database_value(bot, duelrecorduser, 'roulettelastplayer')
        reset_database_value(bot, duelrecorduser, 'roulettechamber')
        reset_database_value(bot, duelrecorduser, 'roulettewinners')
        reset_database_value(bot, duelrecorduser, 'roulettecount')
        reset_database_value(bot, duelrecorduser, 'roulettespinarray')
        for user in botvisibleusers:
            reset_database_value(bot, user, 'roulettepayout')
    elif subcommand == 'stats':
        incorrectdisplay = "A correct command use is .duel admin stats target set/reset stat."
        target = get_trigger_arg(bot, triggerargsarray, 3)
        subcommand = get_trigger_arg(bot, triggerargsarray, 4)
        statset = get_trigger_arg(bot, triggerargsarray, 5)
        newvalue = get_trigger_arg(bot, triggerargsarray, 6)
        duelstatsadminarray = duels_valid_stats(bot)
        if not target:
            osd_notice(bot, instigator, "Target Missing. " + incorrectdisplay)
        elif target.lower() not in [u.lower() for u in botvisibleusers] and target != 'everyone':
            osd_notice(bot, instigator, "It looks like " + str(target) + " is either not here, or not a valid person.")
        elif not subcommand:
            osd_notice(bot, instigator, "Subcommand Missing. " + incorrectdisplay)
        elif subcommand not in stat_admin_commands:
            osd_notice(bot, instigator, "Invalid subcommand. " + incorrectdisplay)
        elif not statset:
            osd_notice(bot, instigator, "Stat Missing. " + incorrectdisplay)
        elif statset not in duelstatsadminarray and statset != 'all':
            osd_notice(bot, instigator, "Invalid stat. " + incorrectdisplay)
        else:
            target = actualname(bot, target)
            if subcommand == 'reset':
                newvalue = None
            if subcommand == 'set' and newvalue == None:
                osd_notice(bot, instigator, "When using set, you must specify a value. " + incorrectdisplay)
            elif target == 'everyone':
                set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
                reset_database_value(bot, duelrecorduser, 'tier')
                reset_database_value(bot, duelrecorduser, 'specevent')
                for u in botvisibleusers:
                    if statset == 'all':
                         for x in duelstatsadminarray:
                             set_database_value(bot, u, x, newvalue)
                    else:
                        set_database_value(bot, u, statset, newvalue)
                osd_notice(bot, instigator, "Possibly done Adjusting stat(s).")
            else:
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
                osd_notice(bot, instigator, "Possibly done Adjusting stat(s).")
    elif subcommand == 'channel':
        settingchange = get_trigger_arg(bot, triggerargsarray, 3)
        if not settingchange:
            osd_notice(bot, instigator, "What channel setting do you want to change?")
        elif settingchange == 'statreset':
            set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
        elif settingchange == 'lastassault':
            reset_database_value(bot, duelrecorduser, 'lastfullroomassultinstigator')
            osd_notice(bot, instigator, "Last Assault Instigator removed.")
            reset_database_value(bot, duelrecorduser, 'lastfullroomassult')
        elif settingchange == 'lastroman':
            reset_database_value(bot, duelrecorduser, 'lastfullroomcolosseuminstigator')
            osd_notice(bot, instigator, "Last Colosseum Instigator removed.")
            reset_database_value(bot, duelrecorduser, 'lastfullroomcolosseum')
        elif settingchange == 'lastinstigator':
            reset_database_value(bot, duelrecorduser, 'lastinstigator')
            osd_notice(bot, instigator, "Last Fought Instigator removed.")
        elif settingchange == 'halfhoursim':
            osd_notice(bot, instigator, "Simulating the half hour automated events.")
            halfhourtimer(bot)
        else:
            osd_notice(bot, instigator, "Must be an invalid command.")
    else:
        osd_notice(bot, instigator, "An admin command has not been written for the " + subcommand + " command.")

##########################
## 30 minute automation ##
##########################

@sopel.module.interval(1800)
def halfhourtimer(bot):
    now = time.time()

    ## Tier the stats
    tierratio = tierratio_level(bot)
    #healthregencurrent = tierratio * halfhour_regen_health_max
    magemanaregencurrent = tierratio * halfhour_regen_mage_mana_max


    ## Who gets to win a mysterypotion?
    randomuarray = []
    duelusersarray = get_database_value(bot, duelrecorduser, 'duelusers')

    ## Log Out Array
    logoutarray = []

    for u in bot.users:
        ## must have duels enabled, but has to use the game every so often
        if u in duelusersarray and u != bot.nick:

            ## Log out users that aren't playing
            lastcommandusedtime = get_timesince_duels(bot, u, 'lastcommand') or 0
            lastping = get_timesince_duels(bot, u, 'lastping') or 0
            if timeout_auto_opt_out < lastcommandusedtime and lastping < timeout_auto_opt_out:
                logoutarray.append(u)
                reset_database_value(bot, u, 'lastping')
            else:
                set_database_value(bot, u, 'lastping', now)

                uclass = get_database_value(bot, u, 'class_setting') or 'notclassy'
                mana = get_database_value(bot, u, 'mana') or 0

                ## Random user gets a mysterypotion
                lasttimedlootwinner = get_database_value(bot, duelrecorduser, 'lasttimedlootwinner') or bot.nick
                if u != lasttimedlootwinner:
                    randomuarray.append(u)

                ## award coin to all
                adjust_database_value(bot, u, 'coin', halfhour_coin)

                ## health regenerates for all
                for part in stats_healthbodyparts:
                    currenthealthtier = tierratio_level(bot)
                    maxhealthpart = array_compare(bot, part, stats_healthbodyparts, health_bodypart_max)
                    maxhealthpart = int(maxhealthpart)
                    currenthealthtier = currenthealthtier * int(maxhealthpart)
                    currenthealthtier = int(currenthealthtier)
                    currenthealthsplit = maxhealthpart / 2
                    healthsplit = halfhour_regen_health / 6
                    gethowmany = get_database_value(bot, u, part) or 0
                    if not gethowmany or gethowmany <= 0 or gethowmany > currenthealthtier:
                        set_database_value(bot, u, part, currenthealthtier)
                    elif gethowmany < currenthealthsplit:
                        adjust_database_value(bot, u, part, healthsplit)
                        gethowmany = get_database_value(bot, u, part) or 0
                        if gethowmany > currenthealthsplit:
                            set_database_value(bot, u, part, currenthealthsplit)

                ## mages regen mana
                if uclass == 'mage':
                    if int(mana) < magemanaregencurrent:
                        adjust_database_value(bot, u, 'mana', halfhour_regen_mage_mana)
                        mana = get_database_value(bot, u, 'mana')
                        if int(mana) > magemanaregencurrent:
                            set_database_value(bot, u, 'mana', magemanaregencurrent)

    ## Log Out Users
    gameenabledchannels = get_database_value(bot, duelrecorduser, 'gameenabled') or []
    if logoutarray != []:
        dispmsgarray = []
        logoutusers = get_trigger_arg(bot, logoutarray, 'list')
        dispmsgarray.append(logoutusers + " has/have been logged out of duels for inactivity!")
        onscreentext(bot, gameenabledchannels, dispmsgarray)
        adjust_database_array(bot, duelrecorduser, logoutarray, 'duelusers', 'del')

    ## Random winner select
    if randomuarray != []:
        lootwinner = halfhourpotionwinner(bot, randomuarray)
        adjust_database_value(bot, lootwinner, 'mysterypotion', 1)
        osd_notice(bot, lootwinner, "You have been awarded a mysterypotion! Use .duel loot use mysterypotion to consume.")

## Select winner of potion
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
    lootwinner = get_trigger_arg(bot, winnerselectarray, 'random') or bot.nick
    adjust_database_array(bot, duelrecorduser, [lootwinner], 'lasttimedlootwinners', 'add')
    set_database_value(bot, duelrecorduser, 'lasttimedlootwinner', lootwinner)
    return lootwinner

#######################
## Valid Stats Array ##
#######################

def duels_valid_stats(bot):
    duelstatsadminarray = []
    for stattype in stats_admin_types:
        stattypeeval = eval("stats_"+stattype)
        for duelstat in stattypeeval:
            duelstatsadminarray.append(duelstat)
    return duelstatsadminarray

def array_compare(bot, indexitem, arraytoindex, arraytocompare):
    item = ''
    for x, y in zip(arraytoindex, arraytocompare):
        if x == indexitem:
            item = y
    return item

def duels_valid_commands(bot):
    duelcommandsarray = []
    for i in range(0,16):
        tiercheck = eval("commandarray_tier_unlocks_"+str(i))
        for x in tiercheck:
            duelcommandsarray.append(x)
    return duelcommandsarray

###########
## Tiers ##
###########

def tier_command(bot, command):
    tiercommandeval = 0
    for i in range(0,16):
        tiercheck = eval("commandarray_tier_unlocks_"+str(i))
        if command.lower() in tiercheck:
            tiercommandeval = int(i)
            continue
    return tiercommandeval

def tier_pepper(bot, pepper):
    tiernumber = commandarray_pepper_levels.index(pepper.lower())
    return tiernumber

def pepper_tier(bot, tiernumber):
    if not tiernumber:
        pepper = 'n00b'
    else:
        pepper = get_trigger_arg(bot, commandarray_pepper_levels, tiernumber + 1)
        pepper = pepper.title()
    return pepper

def tier_xp(bot, xp):
    tiernumber = 0
    smallerxparray = []
    for x in commandarray_xp_levels:
        if x <= xp:
            smallerxparray.append(x)
    if smallerxparray != []:
        bigestxp = max(smallerxparray)
        tiernumber = commandarray_xp_levels.index(bigestxp)
    return tiernumber

def get_pepper(bot, nick):
    if nick == bot.nick:
        pepper = 'Dragon Breath Chilli'
        return pepper
    xp = get_database_value(bot, nick, 'xp') or 0
    if not xp:
        pepper = 'n00b'
        return pepper
    xptier = tier_xp(bot, xp)
    pepper = pepper_tier(bot, xptier)
    # advance respawn tier
    tiernumber = tier_pepper(bot, pepper)
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 0
    if tiernumber > currenttier:
        set_database_value(bot, duelrecorduser, 'tier', tiernumber)
    nicktier = get_database_value(bot, nick, 'tier')
    if tiernumber != nicktier:
        set_database_value(bot, nick, 'tier', tiernumber)
    pepper = pepper.title()
    return pepper

def tierratio_level(bot):
    currenttier = get_database_value(bot, duelrecorduser, 'tier') or 1
    tierratio = get_trigger_arg(bot, commandarray_tier_ratio, currenttier) or 1
    return tierratio

#####################
## Target Criteria ##
#####################

## Target
def targetcheck(bot, target, dueloptedinarray, botvisibleusers, currentuserlistarray, instigator, currentduelplayersarray, validcommands):

    ## Guilty until proven Innocent
    validtarget = 1
    validtargetmsg = []

    ## Null Target
    if not target:
        validtarget = 0
        validtargetmsg.append("You must specify a target.")

    ## Bot
    if target == bot.nick or target == 'duelrecorduser':
        validtarget = 0
        validtargetmsg.append(target + " can't be targeted.")

    ## Target can't be a valid command
    if target.lower() in validcommands:
        validtarget = 0
        validtargetmsg.append(target + "'s nick is the same as a valid command for duels.")

    ## Target can't be duelrecorduser
    if target.lower() == duelrecorduser:
        validtarget = 0
        validtargetmsg.append(target + "'s nick is unusable for duels.")

    ## Offline User
    if target.lower() in [x.lower() for x in botvisibleusers] and target.lower() not in [y.lower() for y in currentuserlistarray]:
        validtarget = 0
        target = actualname(bot, target)
        validtargetmsg.append(target + " is offline right now.")

    ## Opted Out
    if target.lower() in [x.lower() for x in currentuserlistarray] and target.lower() not in [j.lower() for j in dueloptedinarray]:
        target = actualname(bot, target)
        validtarget = 0
        validtargetmsg.append(target + " has duels disabled.")

    ## None of the above
    if target.lower() not in [y.lower() for y in currentuserlistarray]:
        target = actualname(bot, target)
        validtarget = 0
        validtargetmsg.append(target + " is either not here, or not a valid nick to target.")

    if target != instigator and validtarget == 1:
        statreset(bot, target)

    return validtarget, validtargetmsg

# mustpassthesetoduel
def duelcriteria(bot, usera, userb, currentduelplayersarray, inchannel):

    ## Guilty until proven Innocent
    validtarget = 1
    validtargetmsg = []

    ## usera ignores lastfought
    useraclass = get_database_value(bot, usera, 'class_setting') or 'notclassy'
    if useraclass != 'knight':
        useralastfought = get_database_value(bot, usera, 'lastfought') or ''
    else:
        useralastfought = bot.nick

    ## Timeout Retrieval
    useratime = get_timesince_duels(bot, usera, 'timeout_timeout') or 0
    userbtime = get_timesince_duels(bot, userb, 'timeout_timeout') or 0
    channeltime = get_timesince_duels(bot, duelrecorduser, 'timeout_timeout') or 0

    ## Last instigator
    channellastinstigator = get_database_value(bot, duelrecorduser, 'lastinstigator') or bot.nick

    ## Current Users List
    dueluserslist = []
    for x in currentduelplayersarray:
        if x != bot.nick:
            dueluserslist.append(x)
    howmanyduelsers = len(dueluserslist)

    ## Correct userb Name
    userb = actualname(bot, userb)

    ## Devroom bypass
    devenabledchannels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    if inchannel in devenabledchannels:
        validtarget = 1
        return validtarget, validtargetmsg

    ## Don't allow usera to duel twice in a row
    if usera == channellastinstigator and useratime <= INSTIGATORTIMEOUT:
        validtargetmsg.append("You may not instigate fights twice in a row within a half hour. You must wait for somebody else to instigate, or "+str(hours_minutes_seconds((INSTIGATORTIMEOUT - useratime)))+" .")
        validtarget = 0

    ## usera can't duel the same person twice in a row, unless there are only two people in the channel
    if userb == useralastfought and howmanyduelsers > 2:
        validtargetmsg.append('You may not fight the same person twice in a row.')
        validtarget = 0

    ## usera Timeout
    if useratime <= USERTIMEOUT:
        validtargetmsg.append("You can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - useratime)))+".")
        validtarget = 0

    ## Target Timeout
    if userbtime <= USERTIMEOUT:
        validtargetmsg.append(userb + " can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - userbtime)))+".")
        validtarget = 0

    ## Channel Timeout
    if channeltime <= CHANTIMEOUT:
        validtargetmsg.append("Channel can't duel for "+str(hours_minutes_seconds((CHANTIMEOUT - channeltime)))+".")
        validtarget = 0

    return validtarget, validtargetmsg

def duelcriteriashort(bot, usera, userb, currentduelplayersarray, inchannel):

    ## Guilty until proven Innocent
    validtarget = 0

    ## Devroom bypass
    devenabledchannels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    if inchannel in devenabledchannels:
        validtarget = 1
        return validtarget

    ## Don't allow usera to duel twice in a row
    useratime = get_timesince_duels(bot, usera, 'timeout_timeout') or 0
    channellastinstigator = get_database_value(bot, duelrecorduser, 'lastinstigator') or bot.nick
    if usera == channellastinstigator and useratime <= INSTIGATORTIMEOUT:
        return validtarget

    ## usera can't duel the same person twice in a row, unless there are only two people in the channel
    howmanyduelsers = len(currentduelplayersarray)
    userbtime = get_timesince_duels(bot, userb, 'timeout_timeout') or 0
    if userb == useralastfought and howmanyduelusers > 2:
        useraclass = get_database_value(bot, usera, 'class_setting') or 'notclassy'
        if useraclass != 'knight':
            return validtarget

    ## usera Timeout
    if useratime <= USERTIMEOUT:
        return validtarget

    ## Target Timeout
    channeltime = get_timesince_duels(bot, duelrecorduser, 'timeout_timeout') or 0
    if userbtime <= USERTIMEOUT:
        return validtarget

    ## Channel Timeout
    if channeltime <= CHANTIMEOUT:
        return validtarget

    validtarget = 1
    return validtarget

## Events
def eventchecks(bot, canduelarray, commandortarget, instigator, currentduelplayersarray, inchannel):

    ## Guilty until proven Innocent
    validtarget = 1
    validtargetmsg = []

    if canduelarray == []:
        validtarget = 0
        validtargetmsg.append(instigator + ", It looks like the full channel " + commandortarget + " event target finder has failed.")
        return validtarget, validtargetmsg

    ## Devroom bypass
    devenabledchannels = get_database_value(bot, duelrecorduser, 'devenabled') or []
    if inchannel in devenabledchannels:
       return validtarget, validtargetmsg

    if instigator not in canduelarray:
        validtarget = 0
        canduel, validtargetmsgb = duelcriteria(bot, instigator, instigator, currentduelplayersarray, inchannel)
        for x in validtargetmsgb:
            validtargetmsg.append(x)

    timeouteval = eval("timeout_"+commandortarget.lower())
    getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + commandortarget)) or timeouteval
    getlastinstigator = get_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator')) or bot.nick

    if getlastusage < timeouteval:
        validtargetmsg.append("Full channel " + commandortarget + " event can't be used for "+str(hours_minutes_seconds((timeouteval - getlastusage)))+".")
        validtarget = 0

    if getlastinstigator == instigator:
        validtargetmsg.append("You may not instigate a full channel " + commandortarget + " event twice in a row.")
        validtarget = 0

    if validtarget == 1:
        for player in canduelarray:
            statreset(bot, player)

    return validtarget, validtargetmsg

############
## Damage ##
############

## bodypart selector
def bodypart_select(bot, nick):
    ## selection roll
    hitchance = randint(1, 101)
    if hitchance <= 50:
        bodypart = 'chest'
    elif hitchance >= 90:
        bodypart = 'head'
    else:
        currentbodypartsarray = bodypartarray(bot, nick)
        bodypart = get_trigger_arg(bot, currentbodypartsarray, 'random')
    if "_" in bodypart:
        bodypartname = bodypart.replace("_", " ")
    else:
        bodypartname = bodypart
    return bodypart, bodypartname

## Damage Caused
def duels_damage(bot, damagescale, classwinner, classloser, winner, loser):

    ## Rogue can't be hurt by themselves or bot
    if classloser == 'rogue' and winner == loser:
        damage = 0

    ## Bot deals a set amount
    elif winner == bot.nick:
        if classloser == 'rogue':
            damage = 0
        else:
            damage = bot_damage

    ## Barbarians get extra damage (minimum)
    elif classwinner == 'barbarian':
        damage = randint(duel_advantage_barbarian_min_damage, 120)

    ## vampires have a minimum damage
    elif classwinner == 'vampire' and winner != loser:
        damage = randint(0, duel_disadvantage_vampire_max_damage)

    ## All Other Players
    else:
        damage = randint(0, 120)

    ## Damage Tiers
    if damage > 0:
        damage = damagescale * damage

    return damage

## Damage Text
def duels_damage_text(bot, damage, winnername, losername, bodypart, striketype, weapon, classwinner, bodypartname):

    if losername == winnername:
        losername = "themself"

    if damage == 0:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypartname + weapon + ', but deals no damage.')
    elif classwinner == 'vampire' and winnername != losername:
        damagetext = str(winnername + " drains " + str(damage)+ " health from " + losername + weapon + " in the " + bodypartname + ".")
    else:
        damagetext = str(winnername + " " + striketype + " " + losername + " in the " + bodypartname + weapon + ", dealing " + str(damage) + " damage.")
    return damagetext

## Damage Resistance
def damage_resistance(bot, nick, damage, bodypart):
    damagetextarray = []

    ## Shields
    if damage > 0:
        shieldnick = get_database_value(bot, nick, 'shield') or 0
        if shieldnick:
            damagemath = int(shieldnick) - damage
            if int(damagemath) > 0:
                adjust_database_value(bot, nick, 'shield', -abs(damage))
                damage = 0
                absorbed = 'all'
            else:
                absorbed = damagemath + damage
                damage = abs(damagemath)
                reset_database_value(bot, nick, 'shield')
            damagetextarray.append(nick + " absorbs " + str(absorbed) + " of the damage. ")

    ## Armor
    if damage > 0:
        armortype = array_compare(bot, "health_"+bodypart, stats_healthbodyparts, stats_armor)
        armornick = get_database_value(bot, nick, armortype) or 0
        if armornick:
            if "_" in armortype:
                armorname = armorname.replace("_", " ")
            else:
                armorname = armortype
            adjust_database_value(bot, nick, armortype, -1)
            damagepercent = randint(1, armor_relief_percentage) / 100
            damagereduced = damage * damagepercent
            damagereduced = int(damagereduced)
            damage = damage - damagereduced
            damagetext = str(nick + "s "+ armorname + " alleviated " + str(damagereduced) + " of the damage.")
            armornick = get_database_value(bot, nick, armortype) or 0
            if armornick <= 0:
                reset_database_value(bot, nick, armortype)
                damagetext = str(damagetext + ", causing the armor to break!")
            elif armornick <= 5:
                damagetext = str(damagetext + ", causing the armor to be in need of repair!")
            else:
                damagetext = str(damagetext + ".")
            damagetextarray.append(damagetext)

    return damage, damagetextarray

###################
## Living Status ##
###################

## player killed a player
def whokilledwhom(bot, winner, loser):
    winnertextarray = []
    winnertextarray.append(loser + ' dies forcing a respawn!!')
    ## Reset mana and health
    reset_database_value(bot, loser, 'mana')
    healthfresh(bot, loser) ## TODO, replace with just building the health
    ## update kills/deaths
    adjust_database_value(bot, winner, 'kills', 1)
    adjust_database_value(bot, loser, 'respawns', 1)
    ## Loot Corpse
    loserclass = get_database_value(bot, loser, 'class_setting') or 'notclassy'
    bountyonloser = get_database_value(bot, loser, 'bounty')
    if bountyonloser:
        adjust_database_value(bot, winner, 'coin', bountyonloser)
        reset_database_value(bot, loser, 'bounty')
        winnertextarray.append(winner + " wins a bounty of " + str(bountyonloser) + " that was placed on " + loser + ".")
    ## rangers don't lose their stuff
    if loserclass != 'ranger':
        for x in potion_types:
            gethowmany = get_database_value(bot, loser, x)
            ## TODO array of loot won
            adjust_database_value(bot, winner, x, gethowmany)
            reset_database_value(bot, loser, x)
    return winnertextarray

## player killed themself
def suicidekill(bot,loser):
    suicidetextarray = []
    suicidetextarray.append(loser + " committed suicide, forcing a respawn.")
    ## Reset mana
    reset_database_value(bot, loser, 'mana')
    suicidetextarray.append(loser + " lose all mana.")
    ## Stock health
    #set_database_value(bot, loser, 'health_b4se', stockhealth)
    healthfresh(bot, loser) ## TODO: non-tiered
    ## update deaths
    adjust_database_value(bot, loser, 'respawns', 1)
    ## bounty
    bountyonloser = get_database_value(bot, loser, 'bounty')
    if bountyonloser:
        suicidetextarray.append(loser + " wastes the bounty of " + str(bountyonloser) + " coin.")
    reset_database_value(bot, loser, 'bounty')
    ## rangers don't lose their stuff
    loserclass = get_database_value(bot, loser, 'class_setting') or 'notclassy'
    if loserclass != 'ranger':
        for x in potion_types:
            reset_database_value(bot, loser, x)
        suicidetextarray.append(loser + " loses all loot.")
    return suicidetextarray

## Verify health is not below zero, and not above max
def healthcheck(bot, nick):
    ## logic for crippled bodyparts
    for part in stats_healthbodyparts:
        currenthealthtier = tierratio_level(bot)
        maxhealthpart = array_compare(bot, part, stats_healthbodyparts, health_bodypart_max)
        maxhealthpart = int(maxhealthpart)
        currenthealthtier = currenthealthtier * int(maxhealthpart)
        currenthealthtier = int(currenthealthtier)
        gethowmany = get_database_value(bot, nick, part) or 0
        if not gethowmany or gethowmany <= 0 or gethowmany > currenthealthtier:
            set_database_value(bot, nick, part, currenthealthtier)
    ## no mana at respawn
    mana = get_database_value(bot, nick, 'mana')
    if int(mana) <= 0:
        reset_database_value(bot, nick, 'mana')

## Health after death
def healthfresh(bot, nick):
    ## logic for crippled bodyparts
    for part in stats_healthbodyparts:
        currenthealthtier = tierratio_level(bot)
        maxhealthpart = array_compare(bot, part, stats_healthbodyparts, health_bodypart_max)
        maxhealthpart = int(maxhealthpart)
        currenthealthtier = currenthealthtier * int(maxhealthpart)
        currenthealthtier = int(currenthealthtier)
        gethowmany = get_database_value(bot, nick, part) or 0
        set_database_value(bot, nick, part, currenthealthtier)
    ## no mana at respawn
    mana = get_database_value(bot, nick, 'mana')
    if int(mana) <= 0:
        reset_database_value(bot, nick, 'mana')

## Total Health
def get_health(bot,nick):
    totalhealth = 0
    for x in stats_healthbodyparts:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            totalhealth = totalhealth + gethowmany
    return totalhealth

## Non-Crippled Body Parts
def bodypartarray(bot, nick):
    currentbodypartsarray = []
    for x in stats_healthbodyparts:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            currentbodypartsarray.append(x)
    return currentbodypartsarray

################
## User Nicks ##
################

## Build Duel Name Text
def duel_names(bot, nick, channel):
    nickname = ''
    for q in duel_nick_order:
        nickscriptdef = str(q + "(bot, nick, channel)")
        nicknameadd = eval(nickscriptdef)
        if nicknameadd != '':
            if nickname != '':
                nickname = str(nickname + " " + nicknameadd)
            else:
                nickname = nicknameadd
    if nickname == '':
        nickname = nick
    return nickname

## Titles
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
    ## development_team
        elif nick in development_team:
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

## Pepper
def nickpepper(bot, nick, channel):
    pepperstart = get_pepper(bot, nick)
    if not pepperstart or pepperstart == '':
        nickname = "(n00b)"
    else:
        nickname = str("(" + pepperstart.title() + ")")
    return nickname

## Magic
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

## Armored
def nickarmor(bot, nick, channel):
    nickname = ''
    for x in stats_armor:
        gethowmany = get_database_value(bot, nick, x)
        if gethowmany:
            nickname = "{Armored}"
    return nickname

## Outputs Nicks with correct capitalization
def actualname(bot,nick):
    actualnick = nick
    for u in bot.users:
        if u.lower() == nick.lower():
            actualnick = u
    return actualnick

##########
## Time ##
##########

## compare timestamps
def get_timesince_duels(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))

## Get timediff for user timeouts for stats display
def get_timeout_timeout(bot, nick):
    time_since = get_timesince_duels(bot, nick, 'timeout_timeout')
    if time_since < USERTIMEOUT:
        timediff = str(hours_minutes_seconds((USERTIMEOUT - time_since)))
    else:
        timediff = 0
    return timediff

## Convert seconds to a readable format
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
        beststreaktype = 'streak_win_best'
        currentstreaktype = 'streak_win_current'
        oppositestreaktype = 'streak_loss_current'
    elif winlose == 'loss':
        beststreaktype = 'streak_loss_best'
        currentstreaktype = 'streak_loss_current'
        oppositestreaktype = 'streak_win_current'

    ## Update Current streak
    adjust_database_value(bot, nick, currentstreaktype, 1)
    set_database_value(bot, nick, 'streak_type_current', winlose)

    ## Update Best Streak
    beststreak = get_database_value(bot, nick, beststreaktype) or 0
    currentstreak = get_database_value(bot, nick, currentstreaktype) or 0
    if int(currentstreak) > int(beststreak):
        set_database_value(bot, nick, beststreaktype, int(currentstreak))

    ## Clear current opposite streak
    reset_database_value(bot, nick, oppositestreaktype)

def get_current_streaks(bot, winner, loser):
    winner_loss_streak = get_database_value(bot, winner, 'streak_loss_current') or 0
    loser_win_streak = get_database_value(bot, loser, 'streak_win_current') or 0
    return winner_loss_streak, loser_win_streak

def get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak):
    win_streak = get_database_value(bot, winner, 'streak_win_current') or 0
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

## Chance of Finding loot in a duel
def randominventory(bot, instigator):
    yourclass = get_database_value(bot, instigator, 'class_setting') or 'notclassy'
    if yourclass == 'scavenger':
        randomfindchance = randint(duel_advantage_scavenger_loot_find, 100)
    else:
        randomfindchance = randint(0, 120)
    randominventoryfind = 'false'
    if randomfindchance >= 90:
        randominventoryfind = 'true'
    return randominventoryfind

######################
## Weapon Selection ##
######################

## allchan weapons
def getallchanweaponsrandom(bot):
    allchanweaponsarray = []
    for u in bot.users:
        weaponslist = get_database_value(bot, u, 'weaponslocker_complete') or ['fist']
        for x in weaponslist:
            allchanweaponsarray.append(x)
    weapon = get_trigger_arg(bot, allchanweaponsarray, 'random')
    return weapon

def weaponofchoice(bot, nick):
    weaponslistselect = []
    weaponslist = get_database_value(bot, nick, 'weaponslocker_complete') or []
    lastusedweaponarry = get_database_value(bot, nick, 'weaponslocker_lastweaponusedarray') or []
    lastusedweapon = get_database_value(bot, nick, 'weaponslocker_lastweaponused') or 'fist'
    howmanyweapons = get_database_array_total(bot, nick, 'weaponslocker_complete') or 0
    if not howmanyweapons > 1:
        reset_database_value(bot, nick, 'weaponslocker_lastweaponused')
    for x in weaponslist:
        if len(x) > weapon_name_length:
            adjust_database_array(bot, nick, [x], 'weaponslocker_complete', 'del')
        if x not in lastusedweaponarry and x != lastusedweapon and len(x) <= weapon_name_length:
            weaponslistselect.append(x)
    if weaponslistselect == [] and weaponslist != []:
        reset_database_value(bot, nick, 'weaponslocker_lastweaponusedarray')
        return weaponofchoice(bot, nick)
    weapon = get_trigger_arg(bot, weaponslistselect, 'random') or 'fist'
    adjust_database_array(bot, nick, [weapon], 'weaponslocker_lastweaponusedarray', 'add')
    set_database_value(bot, nick, 'weaponslocker_lastweaponused', weapon)
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

def chanstatreset(bot):
    now = time.time()
    duelstatsadminarray = duels_valid_stats(bot)
    for x in duelstatsadminarray:
        reset_database_value(bot, duelrecorduser, "usage_"+x)
        reset_database_value(bot, bot.nick, "usage_"+x)
        reset_database_value(bot, duelrecorduser, "usage_total")
        reset_database_value(bot, bot.nick, "usage_total")
        reset_database_value(bot, bot.nick, x)
        reset_database_value(bot, duelrecorduser, x)
    set_database_value(bot, duelrecorduser, 'chanstatsreset', now)

def duelrecordwipe(bot):
    chanrecordsarray = ['gameenabled','devenabled','botvisibleusers','duelusers','duelslockout','tier','lastinstigator','timeout_timeout','specevent','roulettelastplayershot','roulettelastplayer','roulettecount','roulettechamber','roulettespinarray','roulettewinners','lasttimedlootwinner']
    eventsarray = ['roulette','colosseum','assault']
    for event in eventsarray:
        reset_database_value(bot, duelrecorduser, "lastfullroom" + event)
        reset_database_value(bot, bot.nick, "lastfullroom" + event)
    for astat in assault_results:
        reset_database_value(bot, duelrecorduser, "assault_" + astat)
        reset_database_value(bot, bot.nick, "assault_" + astat)
    for record in chanrecordsarray:
        reset_database_value(bot, duelrecorduser, record)
        reset_database_value(bot, bot.nick, record)

def statreset(bot, nick):
    now = time.time()
    getlastchanstatreset = get_database_value(bot, duelrecorduser, 'chanstatsreset')
    if not getlastchanstatreset:
        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
    getnicklastreset = get_database_value(bot, nick, 'chanstatsreset')
    if getnicklastreset < getlastchanstatreset:
        duelstatsadminarray = duels_valid_stats(bot)
        for x in duelstatsadminarray:
            reset_database_value(bot, nick, "usage_"+x)
            reset_database_value(bot, nick, x)
        set_database_value(bot, nick, 'chanstatsreset', now)
        reset_database_value(bot, nick, "usage_combat")
        reset_database_value(bot, nick, "usage_total")
        reset_database_value(bot, nick, "roulettepayout")

## Bot no stats
def refreshbot(bot):
    duelstatsadminarray = duels_valid_stats(bot)
    for x in duelstatsadminarray:
        set_database_value(bot, bot.nick, x, None)

######################
## Winner Selection ##
######################

## Select winner from an array (stat based)
def selectwinner(bot, nickarray):
    statcheckarray = ['health','xp','kills','respawns','streak_win_current']

    ## empty var to start
    for user in nickarray:
        reset_database_value(bot, user, 'winnerselection')

    ## everyone gets a roll
    for user in nickarray:
        adjust_database_value(bot, user, 'winnerselection', 1)

    ## random roll
    randomrollwinner = get_trigger_arg(bot, nickarray, 'random')
    adjust_database_value(bot, randomrollwinner, 'winnerselection', 1)

    ## Stats
    for x in statcheckarray:
        statscore = 0
        if x == 'respawns' or x == 'streak_win_current':
            statscore = 99999999
        statleader = ''
        for u in nickarray:
            if x != 'health':
                value = get_database_value(bot, u, x) or 0
            else:
                scriptdef = str('get_' + x + '(bot,u)')
                value = eval(scriptdef)
            if x == 'respawns' or x == 'streak_win_current':
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
        weaponslist = get_database_value(bot, user, 'weaponslocker_complete') or []
        if weaponslist != []:
            adjust_database_value(bot, user, 'winnerselection', 1)

    ## anybody rogue?
    for user in nickarray:
        nickclass = get_database_value(bot, user, 'class_setting') or ''
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

## Max diceroll
def winnerdicerolling(bot, nick, rolls):
    nickclass = get_database_value(bot, nick, 'class_setting') or ''
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

def get_current_magic_attributes(bot, nick):
    nickshield = get_database_value(bot, nick, 'shield') or 0
    nickcurse = get_database_value(bot, nick, 'curse') or 0
    return nickshield, nickcurse

def get_magic_attributes_text(bot, winner, loser, winnershieldstart, losershieldstart, winnercursestart, losercursestart):
    attributetext = []
    winnershieldnow, winnercursenow = get_current_magic_attributes(bot, winner)
    losershieldnow, losercursenow = get_current_magic_attributes(bot, loser)
    magicattributesarray = ['shield','curse']
    nickarray = ['winner','loser']
    attributetext = ''
    for j in nickarray:
        if j == 'winner':
            scanningperson = winner
        else:
            scanningperson = loser
        for x in magicattributesarray:
            magicname = x.replace("magic_", "")
            workingvarnow = eval(j+magicname+"now")
            workingvarstart = eval(j+magicname+"start")
            if workingvarnow == 0 and workingvarnow != workingvarstart:
                message = str(scanningperson + " is no longer affected by " + x + ".")
                attributetext.append(message)
    return attributetext

###############
## ScoreCard ##
###############

## compare wins/losses
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

#############
## Similar ##
#############

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

##############
## Database ##
##############

## Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

## set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)

## set a value to None
def reset_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)

## add or subtract from current value
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))

## array stored in database length
def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal

## array stored in database, add or remove elements
def adjust_database_array(bot, nick, entries, databasekey, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    reset_database_value(bot, nick, databasekey)
    adjustarray = []
    if adjustmentdirection == 'add':
        for y in entries:
            if y not in adjustarraynew:
                adjustarraynew.append(y)
    elif adjustmentdirection == 'del':
        for y in entries:
            if y in adjustarraynew:
                adjustarraynew.remove(y)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        reset_database_value(bot, nick, databasekey)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)

######################
## On Screen Text ##
######################

def osd_notice(bot, target, textarraycomplete):
    target = actualname(bot,target)
    if not isinstance(textarraycomplete, list):
        texttoadd = str(textarraycomplete)
        textarraycomplete = []
        textarraycomplete.append(texttoadd)
    passthrough = []
    passthrough.append(target + ", ")
    for x in textarraycomplete:
        passthrough.append(x)
    onscreentext(bot, [target], passthrough)

def onscreentext(bot, texttargetarray, textarraycomplete):
    if not isinstance(textarraycomplete, list):
        texttoadd = str(textarraycomplete)
        textarraycomplete = []
        textarraycomplete.append(texttoadd)
    if not isinstance(texttargetarray, list):
        target = texttargetarray
        texttargetarray = []
        texttargetarray.append(target)
    combinedtextarray = []
    currentstring = ''
    for textstring in textarraycomplete:
        if currentstring == '':
            currentstring = textstring
        elif len(textstring) > 200:
            if currentstring != '':
                combinedtextarray.append(currentstring)
                currentstring = ''
            combinedtextarray.append(textstring)
        else:
            tempstring = str(currentstring + "   " + textstring)
            if len(tempstring) <= 200:
                currentstring = tempstring
            else:
                combinedtextarray.append(currentstring)
                currentstring = textstring
    if currentstring != '':
        combinedtextarray.append(currentstring)
    for combinedline in combinedtextarray:
        for user in texttargetarray:
            if user == 'say':
                bot.say(combinedline)
            elif user.startswith("#"):
                bot.msg(user, combinedline)
            else:
                bot.notice(combinedline, user)

####################################
## Array/List/String Manipulation ##
####################################

## Hub
def get_trigger_arg(bot, inputs, outputtask):
    ## Create
    if outputtask == 'create':
        return create_array(bot, inputs)
    ## reverse
    if outputtask == 'reverse':
        return reverse_array(bot, inputs)
    ## Comma Seperated List
    if outputtask == 'list':
        return list_array(bot, inputs)
    if outputtask == 'random':
        return random_array(bot, inputs)
    ## Last element
    if outputtask == 'last':
        return last_array(bot, inputs)
    ## Complete String
    if outputtask == 0 or outputtask == 'complete' or outputtask == 'string':
        return string_array(bot, inputs)
    ## Number
    if str(outputtask).isdigit():
        return number_array(bot, inputs, outputtask)
    ## Exlude from array
    if str(outputtask).endswith("!"):
        return excludefrom_array(bot, inputs, outputtask)
    ## Inclusive range starting at
    if str(outputtask).endswith("+"):
        return incrange_plus_array(bot, inputs, outputtask)
    ## Inclusive range ending at
    if str(outputtask).endswith("-"):
        return incrange_minus_array(bot, inputs, outputtask)
    ## Exclusive range starting at
    if str(outputtask).endswith(">"):
        return excrange_plus_array(bot, inputs, outputtask)
    ## Exclusive range ending at
    if str(outputtask).endswith("<"):
        return excrange_minus_array(bot, inputs, outputtask)
    ## Range Between Numbers
    if "^" in str(outputtask):
        return rangebetween_array(bot, inputs, outputtask)
    string = ''
    return string

## Convert String to array
def create_array(bot, inputs):
    if isinstance(inputs, list):
        string = ''
        for x in inputs:
            if string != '':
                string = str(string + " " + str(x))
            else:
                string = str(x)
        inputs = string
    outputs = []
    if inputs:
        for word in inputs.split():
            outputs.append(word)
    return outputs

## Convert Array to String
def string_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    for x in inputs:
        if string != '':
            string = str(string + " " + str(x))
        else:
            string = str(x)
    return string

## output reverse order
def reverse_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    if len(inputs) == 1:
        return inputs
    outputs = []
    if inputs == []:
        return outputs
    for d in inputs:
        outputs.append(d)
    outputs.reverse()
    return outputs

## Comma Seperated List
def list_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    for x in inputs:
        if string != '':
            string  = str(string  + ", " + x)
        else:
            string  = str(x)
    return string

## Random element
def random_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    temparray = []
    for d in inputs:
        temparray.append(d)
    shuffledarray = random.shuffle(temparray)
    randomselected = random.randint(0,len(temparray) - 1)
    string = str(temparray [randomselected])
    return string

## Last element
def last_array(bot, inputs):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if inputs == []:
        return string
    string = inputs[len(inputs)-1]
    return string

## select a number
def number_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if str(number).isdigit():
        numberadjust = int(number) -1
        if numberadjust< len(inputs) and numberadjust >= 0:
            number = int(number) - 1
            string = inputs[number]
    return string

## range
def range_array(bot, inputs, rangea, rangeb):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    if int(rangeb) == int(rangea):
        return number_array(bot, inputs, rangeb)
    if int(rangeb) < int(rangea):
        tempa, tempb = rangeb, rangea
        rangea, rangeb = tempa, tempb
    if int(rangea) < 1:
        rangea = 1
    if int(rangeb) > len(inputs):
        rangeb = len(inputs)
    for i in range(int(rangea) + 1,int(rangeb) + 1):
        arg = number_array(bot, inputs, i)
        if string != '':
            string = str(string + " " + arg)
        else:
            string = str(arg)
    return string

## exclude a number
def excludefrom_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    if str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
    if str(number).isdigit():
        for i in range(1,len(inputs)):
            if int(i) != int(number):
                arg = number_array(bot, inputs, i)
                if string != '':
                    string = str(string + " " + arg)
                else:
                    string = str(arg)
    return string

## range between
def rangebetween_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if "^" in str(number):
        rangea = number.split("^", 1)[0]
        rangeb = number.split("^", 1)[1]
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

## inclusive forward
def incrange_plus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("+"):
        rangea = re.sub(r"\+", '', str(number))
        rangeb = len(inputs)
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

## inclusive reverse
def incrange_minus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("-"):
        rangea = 1
        rangeb = re.sub(r"-", '', str(number))
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

## excluding forward
def excrange_plus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith(">"):
        rangea = re.sub(r">", '', str(number))
        rangea = int(rangea) + 1
        rangeb = len(inputs)
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)

## excluding reverse
def excrange_minus_array(bot, inputs, number):
    if not isinstance(inputs, list):
        inputs = create_array(bot, inputs)
    string = ''
    rangea = 'error'
    rangeb = 'handling'
    if str(number).endswith("<"):
        rangea = 1
        rangeb = re.sub(r"<", '', str(number))
        rangeb = int(rangeb) - 1
    if not str(rangea).isdigit() or not str(rangeb).isdigit():
        return string
    return range_array(bot, inputs, rangea, rangeb)
