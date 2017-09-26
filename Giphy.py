import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint


@sopel.module.rate(120)
@sopel.module.commands('gif','giphy')

def gif(bot,trigger):
    query = trigger.group(2).replace(' ', '+')
    if query:
        gif = getGif(query)
        if gif:
            bot.say(gif)
        else:
            bot.say('Hmm...Couldn't find a gif for that!')
    else:
        bot.say('Tell me what you're looking for!')


def getGif(query):
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    url = 'http://api.giphy.com/v1/gifs/search?q='+query+'&api_key=' + api + '&limit=100'
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(0,99)
    id = data['data'][randno]['id']
    gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    return gif
