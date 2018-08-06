#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
sys.path.append(moduledir)
from BotShared import *
from Bucks import *
from Casino_Var import *

now = time.time()


@sopel.module.commands('gamble', 'casino')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'gamble')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, arg, botcom, instigator):
    mygame = get_trigger_arg(bot, arg, 1) or 'nocommand'
    if mygame == 'docs' or mygame == 'help':
        osd(bot, trigger.sender, 'say', "For help with this module, see here: " + wikiurl)
    elif mygame == 'slots':
        slots(bot, botcom, trigger, arg)
    elif mygame == 'blackjack':
        blackjack(bot, trigger, arg)
    elif (mygame == 'roulette' or mygame == 'spin'):
        roulette(bot, botcom, trigger, arg)
    elif mygame == 'lottery':
        lottery(bot, botcom, trigger, arg)
    elif mygame == 'freebie':
        freebie(bot, trigger)
    elif mygame == 'bank':
        bankbalance = bank(bot, trigger.nick)
        osd(bot, trigger.nick, 'priv', trigger.nick + ' has ' + str(bankbalance) + ' spicychips in the bank.')
    elif mygame == 'jackpot':
        bankbalance = bank(bot, 'casino')
        osd(bot, trigger.sender, 'say', 'The current jackpot is: ' + str(bankbalance))
    elif mygame == 'admin':
        if trigger.admin or trigger.nick == 'under_score':
            admincommands(bot, trigger, arg)
        else:
            osd(bot, trigger.nick, 'priv', 'You must be an admin to use this command')
    else:
        osd(bot, trigger.sender, 'say', 'Please choose a game. Options include: slots, blackjack, roulette, and lottery.')


def freebie(bot, trigger):
    bankbalance = bank(bot, trigger.nick) or 0
    casinobalance = bank(bot, 'casino') or 0
    if bankbalance < 1:
        if casinobalance >= 1:
            osd(bot, trigger.nick, 'priv', 'The casino gives you 1 spicychips for use in the casino')
            transfer(bot, botcom,  trigger.nick, 'casino', 1)
        else:
            osd(bot, trigger.nick, 'priv', "The casino doesn't have any funds to provide")
    else:
        osd(bot, trigger.nick, 'priv', 'Looks like you dont need a handout because your bank balance is ' + str(bankbalance))


def slots(bot, botcom, trigger, arg):
    # _____________Game 1 slots___________
    # slot machine that uses computer terms with a jackpot tied to how much money has been gambled
    player = trigger.nick
    channel = trigger.sender
    now = time.time()
    bet = get_trigger_arg(bot, arg, '2') or 'nocommand'
    if not bet.isdigit():
        bet = 1
    else:
        bet = int(bet)
    # __payouts___
    match3 = 25*bet
    match2 = 5*bet
    bankbalance = bank(bot, botcom, 'casino')
    if bankbalance < 500:
        bankbalance = 500
        set_database_value(bot, 'casino', 'spicychips_bank',  bankbalance)
    if bet == 'payout':
            osd(bot, trigger.sender, 'say', "Today's jackpot word is " + keyword + " getting it three times will get you " + str(bankbalance) + ". Match 3 and get " + str(match3))
    else:
        # start slots
        if not channel.startswith("#"):
            osd(bot, player, 'notice', "slots can only be used in a channel.")
        else:
            lastslot = get_database_value(bot, 'casino', 'slotimer')
            nextslot = get_timesince(bot, 'casino', 'slotimer')

            if nextslot >= slottimeout:
                successes = transfer(bot, botcom, 'casino', trigger.nick, bet)
                # bot.say(str(successes))
                if successes:
                    set_database_value(bot, 'casino', 'slotimer', now)
                    # add bet to casino
                    mywinnings = 0
                    wheel1 = get_trigger_arg(bot, slotwheel, 'random')
                    wheel2 = get_trigger_arg(bot, slotwheel, 'random')
                    wheel3 = get_trigger_arg(bot, slotwheel, 'random')
                    reel = [wheel1, wheel2, wheel3]
                    if bet < 2:
                        chipcount = " spicychip"
                        # bot.say(chipcount)
                    else:
                        chipcount = " spicychips"
                    osd(bot, trigger.sender, 'say', trigger.nick + " insert " + str(bet) + chipcount + " and the slot machine displays | " + wheel1 + " | " + wheel2 + " | " + wheel3 + " | ")
                    for i in reel:
                        if i == keyword:
                            mywinnings = mywinnings + 1
                    if mywinnings >= 1:
                        osd(bot, player, 'priv', 'You got a bonus word, ' + keyword + ', worth 1 spicychip')

                    if(wheel1 == wheel2 and wheel2 == wheel3):
                        if wheel1 == keyword:
                            osd(bot, trigger.sender, 'say', trigger.nick + ' hit the Jackpot of ' + str(bankbalance))
                            mywinnings = bankbalance
                        elif wheel1 == 'Patches':
                            mywinnings = mywinnings + match3
                        else:
                            mywinnings = mywinnings + match3
                    elif(wheel1 == wheel2 or wheel2 == wheel3 or wheel3 == wheel1):
                        mywinnings = mywinnings + match2
                        # osd(bot, trigger.sender, 'say', trigger.nick + ' a match')

                    if mywinnings <= 0:
                        osd(bot, trigger.sender, 'say', trigger.nick + ' gets nothing')
                    else:
                        bankbalance = bank(bot, botcom, 'casino')
                        if mywinnings > bankbalance:
                            spicychips(bot, trigger.nick, 'plus', mywinnings)
                            osd(bot, trigger.sender, 'say', trigger.nick + ' wins ' + str(mywinnings))
                        else:
                            if transfer(bot, botcom, 'casino', trigger.nick, mywinnings):
                                osd(bot, trigger.sender, 'say', trigger.nick + ' wins ' + str(mywinnings) + " spicychips")
                            else:
                                osd(bot, trigger.sender, 'say', "Error in banking system")
                else:
                    osd(bot, player, 'priv', "You don't have enough spicychips")
            else:
                osd(bot, player, 'priv', "You can not use the slot machine for " + str(hours_minutes_seconds((slottimeout-nextslot))))


# ------Start Roulette
# ----------------Roulette-------
def roulette(bot, botcom, trigger, arg):
    now = time.time()
    channel = trigger.sender
    maxwheel = int(get_database_value(bot, 'casino', 'maxwheel')) or 24

    minbet = 5  # requires at least one payday to play
    wheel = range(maxwheel + 1)
    inputcheck = 0
    maxplayers = 3
    callcheck = False
    player = trigger.nick

    mybet = get_trigger_arg(bot, arg, 2) or 'nobet'
    myitem = get_trigger_arg(bot, arg, 3) or 'noitem'
    myitem2 = get_trigger_arg(bot, arg, 4) or 'noitem'

    # __payouts___
    colorpayout = 2  # % of amount bet + amount bet
    # numberpayout = amount bet * numbers of maxwheel

    if not channel.startswith("#"):
        osd(bot, player, 'notice', "roulette can only be used in a channel.")
    else:
        # set bet/check for commands
        if mybet == 'nobet':
            osd(bot, channel, 'say', 'Please enter an amount to bet')
            inputcheck = 0
        elif mybet == 'payout':
            osd(bot, channel, 'say', 'Picking the winng number will get you ' + str(maxwheel) + ' X your bet. Picking the winning color will get you your bet plus half the amount bet')
        elif mybet == 'call':
            players = get_database_value(bot, 'casino', 'rouletteplayers') or []
            for i in players:
                if i == player:
                    osd(bot, channel, 'say', player + " has asked Spicebot to finish the roulette game. Last call for bets")
                    set_database_value(bot, 'casino', 'casinochannel', str(channel))
                    set_database_value(bot, 'casino', 'counter', 'roulette')
                    set_database_value(bot, 'casino', 'countertimer', now)
                    callcheck = True
            if not callcheck:
                osd(bot, player, 'priv', "You must first place a bet")
        elif mybet == 'end' and bot.nick == 'SpiceCasinoDEV':
            runroulette(bot, botcom)

        else:
            if mybet == 'allin':
                balance = bank(bot, player)
                if balance > 0:
                    mybet = balance
                    if myitem.isdigit():
                        myitem2 = 'noitem'
                        inputcheck = 1
                    else:
                        osd(bot, player, 'priv', "You can only bet on a number going all in.")
                else:
                    osd(bot, player, 'priv', 'You do not have any spicychips')
                    inputcheck = 0
            elif not mybet.isdigit():
                osd(bot, player, 'priv', 'Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet))
                inputcheck = 0
            else:
                inputcheck = 1
                mybet = int(mybet)
                if (mybet < minbet or mybet > maxbet):
                    osd(bot, player, 'priv', 'Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet))
                    inputcheck = 0
            # setup what was bet on
            if inputcheck == 1:
                # check to see if a number was entered
                mynumber = ''
                mycolor = ''
                if myitem.isdigit():
                    mynumber = int(myitem)
                    if(mynumber < 0 or mynumber > maxwheel):
                        osd(bot, player, 'priv', 'Please pick a number between 1 and ' + str(maxwheel))
                        inputcheck = 0
                        # check to see if a color was selected
                    else:
                        if not myitem2 == 'noitem':
                            if (str(myitem2) == 'red' or str(myitem2) == 'black'):
                                mycolor = myitem2
                            else:
                                osd(bot, player, 'priv', 'Choose either red or black')
                                inputcheck = 0
                                mycolor = ''
                        else:
                            mycolor = ''
                            inputcheck = 1
            # was a color selected first
                elif(myitem == 'red' or myitem == 'black'):
                    mycolor = myitem
                    mynumber = ''
                    inputcheck = 1
                else:
                    # no valid choices
                    osd(bot, player, 'priv', 'Please pick either a color or number to bet on')
                    inputcheck = 0

        # user input now setup game will run
        if inputcheck == 1:
            players = get_database_value(bot, 'casino', 'rouletteplayers') or []
            for i in players:
                if i == player:
                    osd(bot, player, 'priv', "You already placed a bet")
                    inputcheck = 0
            if inputcheck == 1:
                if transfer(bot, botcom, 'casino', player, mybet):
                    roulettearray = []
                    osd(bot, channel, 'say', player + " puts " + str(mybet) + " on " + str(mynumber) + " " + str(mycolor))
                    adjust_database_array(bot, 'casino', player, 'rouletteplayers', 'add')
                    set_database_value(bot, 'casino', 'casinochannel', str(channel))
                    roulettearray.append(str(mybet))
                    roulettearray.append(str(mynumber))
                    roulettearray.append(mycolor)
                    testmsg = get_trigger_arg(bot, roulettearray, "list")
                    osd(bot, player, 'priv', "Your bet has been recorded")
                    set_database_value(bot, player, 'roulettearray', roulettearray)
                    numberofplayers = len(players)
                    if numberofplayers >= maxplayers:
                        runroulette(bot)
                    else:
                        osd(bot, channel, 'say', "Spicebot will spin the wheel after " + str((maxplayers-numberofplayers)) + " more people have placed a bet")
                else:
                    osd(bot, player, 'priv', "You don't have enough spicychips to place that bet")


# -----Run roulette game
def runroulette(bot, botcom):
    maxwheel = int(get_database_value(bot, 'casino', 'maxwheel')) or 24
    wheel = range(maxwheel + 1)
    colors = ['red', 'black']
    players = get_database_value(bot, 'casino', 'rouletteplayers') or []

    if not players == []:
        channel = get_database_value(bot, 'casino', 'casinochannel')
        dispmsg = "Spicebot collects all bets"
        osd(bot, channel, 'say', dispmsg)
        winningnumber = spin(wheel)
        if winningnumber == 0:
            winningnumber == 1
        color = spin(colors)
        casinobalance = bank(bot, botcom, 'casino') or 0
        mywinnings = 0
        winners = []
        totalwon = 0
        displaymessage = get_trigger_arg(bot, players, "list")

        dispmsg = "Spicebot spins the wheel good luck to " + displaymessage
        osd(bot, channel, 'say', dispmsg)
        dispmsg = "The wheel stops on " + str(winningnumber) + " " + color
        osd(bot, channel, 'say', dispmsg)
        for player in players:
            mywinnings = 0
            mynumber = 0
            mycolor = ''
            playerarray = get_database_value(bot, player, 'roulettearray') or ''
            if not playerarray == '':
                mybet = get_trigger_arg(bot, playerarray, 1) or 0
                mybet = int(mybet)
                mynumber = get_trigger_arg(bot, playerarray, 2) or 0
                mynumber = int(mynumber)
                mycolor = get_trigger_arg(bot, playerarray, 3) or ''

                if not mybet == 0:
                    if mynumber == winningnumber:
                        mywinnings = mybet * maxwheel
                    elif mycolor == color:  # chance of choosing the same color is so high will set the payout to a fixed amount
                        newbet = int(mybet/2)
                        colorwinnings = mybet + newbet
                        mywinnings = mywinnings + colorwinnings
                    if mywinnings >= 1:
                        osd(bot, player, 'priv', "Roulette has ended and you have won " + str(mywinnings))
                        if casinobalance < mywinnings:
                            addbucks(bot, botcom, 'casino', mywinnings)
                        transfer(bot, botcom, player, 'casino', mywinnings)
                        winners.append(player)
                        totalwon = totalwon + mywinnings
                        reset_database_value(bot, player, 'roulettearray')

        reset_database_value(bot, 'casino', 'rouletteplayers')
        reset_database_value(bot, 'casino', 'counter')
        winnerarray = get_trigger_arg(bot, winners, 'list')
        if len(winners) < 1:
            dispmsg = "No winners this spin"
        elif len(winners) == 1:
            dispmsg = winnerarray + " won " + str(totalwon)
        else:
            dispmsg = "Winners: " + winnerarray + ". and total winnings were " + str(totalwon)
        osd(bot, channel, 'say', dispmsg)


# ______Game 3 Lottery________
def lottery(bot, botcom, trigger, arg):
    lotterymax = int(get_database_value(bot, 'casino', 'lotterymax')) or 25
    lotterytimeout = get_database_value(bot, 'casino', 'lotterytimeout')  # time between lottery drawings
    channel = trigger.sender
    player = trigger.nick
    success = 0
    bankbalance = bank(bot, 'casino')
    if bankbalance <= 500:
        bankbalance = 500
        spicychips(bot, 'casino', 'plus', bankbalance)

    commandused = get_trigger_arg(bot, arg, 2) or 'nocommand'
    if not channel.startswith("#"):
        osd(bot, trigger.nick, 'notice', "lottery can only be used in a channel.")
    else:
        if commandused == 'payout':
            osd(bot, trigger.sender, 'say', "Current lottery jackpot is " + str(bankbalance) + ". Getting 4 number correct pays " + str(int(match4payout*bankbalance)) + " and getting 3 correct = " + str(int(bankbalance*match3payout)))
        elif commandused == 'random':
            picks = random.sample(range(1, lotterymax), 5)
            success = 1
        else:
            picks = []
            picklen = len(arg) + 1
            for i in range(0, picklen):
                picker = get_trigger_arg(bot, arg, i)
                if picker.isdigit():
                    picks.append(int(picker))
            if len(picks) != 5:
                osd(bot, player, 'priv', 'You must enter 5 lottery numbers from 1 to ' + str(lotterymax) + ' to play.')
                success = 0
            else:
                success = 1
        if success == 1:
            pickstemp = picks
            picks = []
            for pick in pickstemp:
                if pick not in picks:
                    picks.append(pick)
            if len(picks) < 5:
                osd(bot, player, 'priv', 'You must choose 5 different numbers.')
                success = 0
            if success == 1:
                valid = 1
                for pick in picks:
                    if(pick > lotterymax or pick < 1):
                        valid = 0
                if valid == 0:
                    osd(bot, player, 'priv', 'One of the numbers you entered is not within the valid range of 1 to ' + str(lotterymax))
                else:
                    lottoplayers = get_database_value(bot, 'casino', 'lottoplayers') or []
                    if player in lottoplayers:
                        osd(bot, player, 'priv', "You are already in this drawing")
                    else:
                        if transfer(bot, botcom, 'casino', player, 1):
                            osd(bot, trigger.sender, 'say', player + " bets on the numbers " + str(picks))
                            set_database_value(bot, player, 'picks', picks)
                            adjust_database_array(bot, 'casino', player, 'lottoplayers', 'add')
                            set_database_value(bot, 'casino', 'lotterychanel', trigger.sender)
                            nextlottery = get_timesince(bot, 'casino', 'lastlottery')
                            osd(bot, player, 'priv', "Next lottery drawing in " + str(hours_minutes_seconds((lotterytimeout-nextlottery))))
                        else:
                            osd(bot, player, 'priv', 'You dont have enough spicychips')


# _______Lottery drawing
def lotterydrawing(bot):
    lotterymax = int(get_database_value(bot, 'casino', 'lotterymax')) or 25
    bankbalance = bank(bot, 'casino')
    nextlottery = get_timesince(bot, 'casino', 'lastlottery')
    lotterytimeout = get_database_value(bot, 'casino', 'lotterytimeout')

    channel = get_database_value(bot, 'casino', 'lotterychanel')
    lotteryplayers = get_database_value(bot, 'casino', 'lottoplayers')
    lotterywinners = []
    totalwon = 0
    bigwinner = ''
    bigwinpayout = 0

    # if get_database_array_total(bot, 'casino','lottoplayers') <1:
    #    msg= "No one entered this lottery. Next lottery drawing will be in " + str(hours_minutes_seconds(lotterytimeout-nextlottery))
    #    osd(bot, channel, 'say', msg)
    # else:
    if get_database_array_total(bot, 'casino', 'lottoplayers') > 0:
        if bankbalance <= 500:
            bankbalance = 500
            set_database_value(bot, 'casino', 'spicychips_bank', bankbalance)

        winningnumbers = random.sample(range(1, lotterymax), 5)

        msg = 'The winning numbers are ' + str(winningnumbers)
        osd(bot, channel, 'say', msg)
        for player in lotteryplayers:
            correct = 0
            picks = get_database_value(bot, player, 'picks') or []
            for pick in picks:
                if pick in winningnumbers:
                    correct = correct + 1
            payout = 0
            if correct == 1:
                payout = match1payout
            elif correct == 2:
                payout = match2payout
            elif correct == 3:
                payout = int(match3payout*bankbalance)
            elif correct == 4:
                payout = int(match4payout*bankbalance)
            elif correct == 5:
                payout = bankbalance

            if payout > bankbalance:
                spicychips(bot, 'casino', 'plus', payout)
            if payout > 0:
                osd(bot, player, 'priv', "You won " + str(payout) + " in the lottery drawing")
                transfer(bot, 'casino', player, payout)
                lotterywinners.append(player)
                totalwon = totalwon + payout
                if payout > bigwinpayout:
                    bigwinpayout = payout
                    bigwinner = player
                bankbalance = bank(bot, 'casino')
            else:
                osd(bot, player, 'priv', 'You are not a lottery winner')

        if totalwon > 0:
            lottowinners = get_trigger_arg(bot, lotterywinners, "list")
            if len(lotterywinners) > 1:
                msg = "Lottery winners: " + lottowinners + ", and the big winner was " + bigwinner + " winning " + str(bigwinpayout) + " in this drawing"
            else:
                msg = lottowinners + " won " + str(bigwinpayout) + " in this drawing"
            osd(bot, channel, 'say', msg)
        else:
            msg = "No one won this drawing."
            osd(bot, channel, 'say', msg)
    reset_database_value(bot, 'casino', 'lottoplayers')


# ____Game 4 Blackjack___
def blackjack(bot, trigger, arg):
    minbet = 30
    blackjackpayout = 2
    beatdealerpayout = 2
    payouton21 = 1
    mychoice = get_trigger_arg(bot, arg, 2) or 'nocommand'
    mychoice2 = get_trigger_arg(bot, arg, 3) or 'nocommand'
    if mychoice == 'nocommand':
        osd(bot, trigger.sender, 'say', "Use .gamble blackjack deal <bet> amount to start a new game")

    else:
        if bot.nick == "Spicebotdev":
            deck = [2, 3, 4, 5, 6, 10, 10, 10, 'J', 'A']*4
        else:
            deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']*4
        myhand = []
        dealerhand = []
        player = trigger.nick
        payout = 0
        if(mychoice == 'deal' or mychoice == 'start' or mychoice == '1'):
            if mychoice2 == 'nocommand':
                osd(bot, player, 'priv', "Please enter an amount you wish to bet")
            else:
                if not mychoice2.isdigit():
                    osd(bot, player, 'priv', 'Please bet a number between ' + str(minbet) + ' and ' + str(maxbet))
                else:
                    mybet = int(mychoice2)
                    if (mybet < minbet or mybet > maxbet):
                        osd(bot, player, 'priv', 'Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet))
                    else:
                        if not get_database_value(bot, player, 'mybet') == 0:
                            osd(bot, player, 'priv', "You already have a game start. Use hit or stand to finish the current game.")
                        else:
                            if transfer(bot, player, 'casino', mybet) == 1:
                                myhand = deal(bot, deck, 2)
                                dealerhand = deal(bot, deck, 2)
                                osd(bot, trigger.sender, 'say', player + ' has a ' + str(myhand[0]) + ' and a ' + str(myhand[1]) + ' Spicebot has a ' + str(dealerhand[1]) + ' showing.')
                                myscore = blackjackscore(bot, myhand)
                                dealerscore = blackjackscore(bot, dealerhand)
                                payout = mybet
                                if myscore == 21:
                                    payout = payout + (mybet*blackjackpayout)
                                    osd(bot, trigger.sender, 'say', player + ' got blackjack and wins ' + str(payout))
                                    spicychips(bot, player, 'plus', payout)
                                else:

                                    # update hand in the database
                                    set_database_value(bot, player, 'myhand', myhand)
                                    set_database_value(bot, player, 'dealerhand', dealerhand)
                                    set_database_value(bot, player, 'mybet', mybet)
                                    osd(bot, player, 'priv', "You can say'.gamble blackjack hit' to take a card or '.gamble blackjack stand' to finish the game")
                            else:
                                osd(bot, player, 'priv', 'You do not have enough ')
        elif mychoice == 'hit' or mychoice == '2':
            myhand = get_database_value(bot, player, 'myhand') or 0
            payout = get_database_value(bot, player, 'mybet') or 0
            if (myhand == [] or myhand == 0):
                osd(bot, trigger.sender, 'say', 'Use deal to start a new game')
            else:
                if len(myhand) >= 6:
                    payment = payout+(int(payout/2))
                    osd(bot, trigger.sender, 'say', player + str(payment) + " wins for having more then 5 cards.")
                    spicychips(bot, player, 'plus', payout)
                    blackjackreset(bot, player)

                else:
                    osd(bot, trigger.sender, 'say', "Player hand before hit: " + str(myhand))
                    playerhitlist = ''
                    hitcard = deal(bot, deck, 1)
                    playerhits = hitcard[0]

                    myhand.append(playerhits)
                    osd(bot, trigger.sender, 'say', "Player hand after hit: " + str(myhand))
                    myscore = blackjackscore(bot, myhand)

                    if myscore <= 21:
                        set_database_value(bot, player, 'myhand', myhand)
                        osd(bot, trigger.sender, 'say', player + " takes a hit and a gets a " + str(playerhits) + " " + player + "'s score is now " + str(myscore))
                    else:
                        osd(bot, trigger.sender, 'say', player + ' got ' + str(playerhits) + ' busted and gets nothing')
                        blackjackreset(bot, player)

        elif mychoice == 'check':
            target = mychoice2
            if targetcheck(bot, target, player) == 0:
                osd(bot, trigger.sender, 'say', "Target not found.")
            else:
                myhand = get_database_value(bot, target, 'myhand') or 0
                dealerhand = get_database_value(bot, target, 'dealerhand') or 0
                osd(bot, trigger.sender, 'say', target + ' has ' + str(myhand) + ' Spicebot has ' + str(dealerhand))

        elif mychoice == 'double' or mychoice == '4':
            myhand = get_database_value(bot, player, 'myhand') or 0
            payout = get_database_value(bot, player, 'mybet') or 0
            dealerhand = get_database_value(bot, player, 'dealerhand') or 0
            if (myhand == [] or myhand == 0):
                osd(bot, trigger.sender, 'say', 'Use deal to start a new game')
            else:
                if len(myhand) == 2:
                    mybet = payout + payout
                    set_database_value(bot, player, 'mybet', mybet)
                    playerhitlist = ''

                    playerhits = deal(bot, deck, 1)
                    playerhits = playerhits[0]
                    myhand.append(playerhits)
                    set_database_value(bot, player, 'myhand', myhand)
                    osd(bot, trigger.sender, 'say', player + " doubles down and gets " + str(playerhits))
                    blackjackstand(bot, player, myhand, dealerhand, mybet)

        elif mychoice == 'stand' or mychoice == '3':
            myhand = get_database_value(bot, player, 'myhand') or 0
            dealerhand = get_database_value(bot, player, 'dealerhand') or 0
            payout = get_database_value(bot, player, 'mybet') or 0
            blackjackstand(bot, player, myhand, dealerhand, payout)

        elif mychoice == 'payout':
            osd(bot, trigger.sender, 'say', "Getting blackjack pays 2x, getting 21 pays 1x, beating Spicebot pays 1/2 your bet.")

        else:
            osd(bot, trigger.sender, 'say', 'Choose an option: deal, hit, or stand')


# __________________________Shared Functions____________________
def spin(wheel):
    random.seed()
    selected = random.randint(0, (len(wheel)-1))
    reel = wheel[selected]
    return reel


def deal(bot, deck, cardcount):
    # choose a random card from a deck and remove it from deck
    hand = []

    for i in range(cardcount):
        card = get_trigger_arg(bot, deck, 'random')

        hand.append(card)
    return hand


def blackjackstand(bot, player, myhand, dealerhand, payout):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']*4
    if (myhand == [] or myhand == 0):
        osd(bot, trigger.sender, 'say', 'Use deal to start a new game')
    else:
        myscore = blackjackscore(bot, myhand)

        dealerscore = blackjackscore(bot, dealerhand)
        dealerwins = ''
        if myscore == 21:
            payout = payout + payout
            osd(bot, trigger.sender, 'say', player + ' got blackjack and is a winner of ' + str(payout))
            spicychips(bot, player, 'plus', payout)
        elif myscore > 21:
            osd(bot, trigger.sender, 'say', player + ' busted and gets nothing')
        elif myscore < 21:
            dealerhitlist = ''
            while dealerscore < 18:
                dealerhits = deal(bot, deck, 1)
                dealerhits = dealerhits[0]
                dealerhitlist = dealerhitlist + ' ' + str(dealerhits)
                dealerhand.append(dealerhits)
                dealerscore = blackjackscore(bot, dealerhand)
            if not dealerhitlist == '':
                hitlist = int(len(dealerhitlist)/2)  # count spaces
                if hitlist > 1:
                    osd(bot, trigger.sender, 'say', 'Spicebot takes ' + str((hitlist)) + ' hits and gets' + dealerhitlist)
                else:
                    osd(bot, trigger.sender, 'say', 'Spicebot takes a hit and gets a' + dealerhitlist)
            showdealerhand = ''

            for i in dealerhand:
                showdealerhand = showdealerhand + " " + str(i)

            if dealerscore > 21:
                payout = payout + int((payout/2))
                spicychips(bot, player, 'plus', payout)
                osd(bot, trigger.sender, 'say', "Spicebot had " + showdealerhand + " busts")
                osd(bot, trigger.sender, 'say', player + ' wins ' + str(payout))
            elif dealerscore == 21:
                osd(bot, trigger.sender, 'say', "Spicebot has " + showdealerhand + " and wins")
            elif dealerscore < myscore:
                payout = payout + int((payout/2))
                spicychips(bot, player, 'plus', payout)
                osd(bot, trigger.sender, 'say', "Spicebot had " + showdealerhand + " " + player + " wins " + str(payout))
            elif dealerscore > myscore:
                osd(bot, trigger.sender, 'say', "Spicebot had " + showdealerhand + " and wins")
            elif dealerscore == myscore:
                spicychips(bot, player, 'plus', payout)
                osd(bot, trigger.sender, 'say', 'It is a draw and ' + player + ' gets ' + str(payout))
            else:
                osd(bot, trigger.sender, 'say', 'No games found say .gamble blackjack deal to start a new game')
        blackjackreset(bot, player)


def blackjackscore(bot, hand):
    myscore = 0
    # hand = get_trigger_arg(bot,hand,'list')
    i = 0
    myhand = []
    handlen = len(hand)
    for i in range(0, handlen):
        card = get_trigger_arg(bot, hand, i)
        if card.isdigit():
            myscore = myscore + int(card)
        elif(card == 'J' or card == 'Q' or card == 'K'):
            myscore = myscore + 10
        elif card == 'A':
            myscore = myscore + 11
    if myscore > 21:
        # osd(bot, trigger.sender, 'say', "Player score: " + str(myscore))
        if 'A' in hand:
            myhand = hand.replace('A', '1')
            newscore = blackjackscore(bot, myhand)
            return newscore
        else:
            # osd(bot, trigger.sender, 'say', "Return player score : " + str(myscore))
            return myscore
    else:
        return myscore
    return myscore


def blackjackreset(bot, player):
    reset_database_value(bot, player, 'myhand')
    reset_database_value(bot, player, 'dealerhand')
    reset_database_value(bot, player, 'mybet')


@sopel.module.interval(10)
def countdown(bot, botcom):
    now = time.time()
    currentsetting = get_database_value(bot, 'casino', 'counter')
    roulettetimediff = get_timesince(bot, 'casino', 'countertimer')
    lotterytimediff = get_timesince(bot, 'casino', 'lastlottery')
    lotterytimeout = get_database_value(bot, 'casino', 'lotterytimeout')
    # if currentsetting == 'roulette':
    # if roulettetimediff >= roulettetimeout:
    # runroulette(bot)
    if lotterytimediff >= lotterytimeout and lotterytimeout >= 10:
        set_database_value(bot, 'casino', 'lastlottery', now)
        lotterydrawing(bot)


def admincommands(bot, trigger, arg):
    player = trigger.nick
    subcommand = get_trigger_arg(bot, arg, 2) or 'nocommand'
    commandvalue = get_trigger_arg(bot, arg, 3) or 'nocommand'
    if subcommand == 'slotadd':
        adjust_database_array(bot, 'casino', commandvalue, 'slotwheel', 'add')
        osd(bot, trigger.nick, 'priv', commandvalue + " added to slot wheel.")
    elif subcommand == 'slotdefault':
        wheel = ['MODEM', 'BSOD', 'RAM', 'CPU', 'RAID', 'VLANS', 'PATCH', 'WIFI', 'CPU', 'CLOUD', 'VLANS', 'AI', 'DARKWEB', 'BLOCKCHAIN', 'PASSWORD']
        set_database_value(bot, 'casino', 'slotwheel', wheel)
        set_database_value(bot, 'casino', 'slotkeyword', 'BSOD')
        osd(bot, trigger.nick, 'priv', "Slot wheel set to defaults.")
    elif subcommand == 'slotremove':
        existingwheel = get_database_value(bot, 'casino', 'slotwheel')
        if commandvalue in existingwheel:
            adjust_database_array(bot, 'casino', commandvalue, 'slotwheel', 'del')
            osd(bot, trigger.nick, 'priv', commandvalue + " removed from slot wheel.")
    elif subcommand == 'slotkeyword':
        existingwheel = get_database_value(bot, 'casino', 'slotwheel')
        if commandvalue in existingwheel:
            set_database_value(bot, 'casino', 'slotkeyword', commandvalue)
            osd(bot, trigger.nick, 'priv', "Slot keyword '" + commandvalue + "' added to slot wheel.")
    elif subcommand == 'slotlist':
        slotlist = get_database_value(bot, 'casino', 'slotwheel')
        listslots = get_trigger_arg(bot, slotlist, 'list')
        osd(bot, player, 'priv', "Slot wheel: " + listslots)

    elif subcommand == 'roulettereset':
        reset_database_value(bot, 'casino', 'rouletteplayers')
        reset_database_value(bot, 'casino', 'counter')
        osd(bot, trigger.nick, 'priv', "Stats reset for roulette")
    elif subcommand == 'rouletteend':
        set_database_value(bot, 'casino', 'casinochannel', str(trigger.sender))
        runroulette(bot)
    elif subcommand == 'roulettemax':
        if commandvalue.isdigit():
            wheelmax = int(commandvalue)
            if wheelmax >= 10:
                set_database_value(bot, 'casino', 'maxwheel', wheelmax)
                osd(bot, trigger.nick, 'priv', "Roulette wheel max set to " + str(wheelmax))
            else:
                osd(bot, trigger.nick, 'priv', "Enter a number larger then 10")
        else:
            osd(bot, trigger.nick, 'priv', "Please enter a valid number")
    elif subcommand == 'lotterymax':
        maxvalue = commandvalue
        if maxvalue.isdigit():
            maxvalue = int(maxvalue)
            if maxvalue >= 10:
                set_database_value(bot, 'casino', 'lotterymax', maxvalue)
                osd(bot, player, 'priv', "Lottery max set to " + str(maxvalue))
            else:
                osd(bot, player, 'priv', "Please enter a number large then 10")
        else:
            osd(bot, player, 'priv', "Please enter a valid number")
    elif subcommand == 'lotteryend':
        lotterydrawing(bot)
    elif subcommand == 'lotterytime':
        if commandvalue.isdigit():
            lotterytime = int(commandvalue)
            if lotterytime >= 10:
                set_database_value(bot, 'casino', 'lotterytimeout', lotterytime)
                osd(bot, trigger.nick, 'priv', "Lottery time out is set " + str(lotterytime) + " seconds")
            else:
                osd(bot, player, 'priv', "Please enter a number larger then 10")
        else:
            osd(bot,  trigger.nick, 'priv', "Please enter a valid number")

    elif subcommand == 'blackjackset':
        if targetcheck(bot, commandvalue, player) == 0:
            osd(bot, trigger.sender, 'say', "Target not found.")
        else:
            reset_database_value(bot, commandvalue, 'myhand')
            reset_database_value(bot, commandvalue, 'dealerhand')
            reset_database_value(bot, commandvalue, 'mybet')
            osd(bot, trigger.nick, 'priv', "Blackjack reset for: " + commandvalue)
