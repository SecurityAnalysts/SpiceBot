#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel.module import commands, example, NOLIMIT
import random
import sys
import os
import requests
import re
import urllib2
import sopel.web as web
import json
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@commands('google', 'search', 'lookup')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'google')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    if len(triggerargsarray)>=1:
        mysite = get_trigger_arg(bot, triggerargsarray, 1).lower()
        searchterm = get_trigger_arg(bot, triggerargsarray, '1+')
        querystring = get_trigger_arg(bot, triggerargsarray, '2+')
        if (mysite == 'video' or mysite == 'youtube'):           
            data=querystring.replace(' ', '+')
            site = '+site%3Ayoutube.com'
            url = 'https://www.youtube.com/'
            url2 = 'https://youtube.com/'
            searchterm = data+site
            query=searchfor(searchterm)
            if not query:
                bot.say('I cannot find anything about that')
            else:
                if(str(query).startswith(url) or str(query).startswith(url2)):
                    bot.say(query)
                else:
                    bot.say(query)
                    bot.say('Valid website not found')

        elif mysite == 'meme':
            data=querystring.replace(' ', '+') 
            site = '+site%3Aknowyourmeme.com'
            url = 'knowyourmeme.com'
            url2 = 'http://knowyourmeme.com'
            searchterm = data+site
            query=searchfor(searchterm)
            if not query:
                bot.say('I cannot find anything about that')
            else:
                if(str(query).startswith(url) or str(query).startswith(url2)):
                    bot.say(query)
                else:
                    bot.say('I could not find that but check this out: https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        elif mysite == 'walmart':
            data=querystring.replace(' ', '+') 
            site = '+site%3Apeopleofwalmart.com'
            url = 'http://www.peopleofwalmart.com'
            url2 = 'https://www.peopleofwalmart.com'
            searchterm = data+site
            query=searchfor(searchterm)
            if not query:
                bot.say('https://goo.gl/SsAhv')
            else:
                if(str(query).startswith(url) or str(query).startswith(url2)):
                    bot.say(query)
                else:
                    bot.say('I could not find that but check this out: https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                    
        elif mysite == 'urban':
            data=querystring.replace(' ', '+')
            query=urbansearch(data)
            bot.say(query)
            
        else:
            #data=searchterm.replace(' ', '+')
            query=searchfor(searchterm)
            if not query:
                bot.say('I cannot find anything about that')
            else:
                bot.say(query)   

def searchfor(data):
    lookfor = data.replace(':', '%3A')
    var = requests.get(r'http://www.google.com/search?q=' + lookfor + '&btnI')
    query=str(var.url)
    return query            

def urbansearch(searchterm):
    try:
        #data = web.get("http://api.urbandictionary.com/v0/define?term={0}".format(web.quote(searchterm)))
        data = web.get("http://api.urbandictionary.com/v0/define?term="+searchterm)
        data = json.loads(data)
    except:
        return bot.say("Error connecting to urban dictionary")
    if data['result_type'] == 'no_results':
        return "No results found for {0}".format(searchterm)
    result = data['list'][0]
    url = 'http://www.urbandictionary.com/define.php?term={0}'.format(web.quote(searchterm))
    response = "{0} - {1}".format(result['definition'].strip()[:256], url)
    return response
