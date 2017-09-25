import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('dave','daveb')
def sorry(bot, trigger):
    usernickname = trigger.nick.lower()
    if "dave" in usernickname:
        bot.say("Is that really you, Dave?")
    bot.say('Im sorry, ' + trigger.nick + ', but I cannot help you.')
