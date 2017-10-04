import sopel.module
from random import random
from random import randint
from sopel import module, tools

@sopel.module.rate(120)
@sopel.module.commands('points','takepoints')
def points_cmd(bot, trigger):
    commandused = trigger.group(1)
    if commandused == 'points':
        giveortake = ' gives '
        tofrom = ' to '
        addminus = 'up'
    else:
        giveortake = ' takes '
        tofrom = ' from '
        addminus = 'down'
    return pointstask(bot, trigger.sender, trigger.nick, trigger.group(3) or '', giveortake, tofrom, addminus)
    
@sopel.module.commands('checkpoints')
def checkpoints(bot, trigger):
    target = trigger.group(3) or trigger.nick
    points = get_points(bot, target)
    if not points:
        bot.say(target + ' has no points history.')
    else:
        bot.say(target + ' has ' + points + ' points.')
    
def pointstask(bot, channel, instigator, target, giveortake, tofrom, addminus):
    target = tools.Identifier(target or '')
    rando = randint(1, 666)
    randopoints = (instigator + str(giveortake) + str(rando) + ' points' + str(tofrom) + ' ')    
    if not target:
        for u in bot.channels[channel].users:
            target = u
            bot.say(str(randopoints) + str(u))
            points_finished(bot, target, rando, addminus)
    else:
        if target == 'all' or target == 'everybody' or target == 'everyone':
            for u in bot.channels[channel].users:
                target = u
                points_finished(bot, target, rando, addminus)
        if target == instigator:
            bot.say('You can\'t adjust your own points!!')
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        else:
            bot.say(str(randopoints) + target)
            points_finished(bot, target, rando, addminus)

def points_finished(bot, target, rando, addminus):
        update_points(bot, target, rando, addminus)

def update_points(bot, nick, rando, addminus):
    points = get_points(bot, nick)
    if addminus == 'up':
        bot.db.set_nick_value(nick, 'points_points', points + int(rando))
    else:
        bot.db.set_nick_value(nick, 'points_points', points - int(rando))
        
def get_points(bot, nick):
    points = bot.db.get_nick_value(nick, 'points_points') or 0
    return points
