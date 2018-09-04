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
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *
from sopel.logger import get_logger

from BotShared import *

LOGGER = get_logger(__name__)


@commands('google', 'search', 'lookup')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'google')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Carry out relevant search."""
    if len(triggerargsarray) >= 1:
        mysite = get_trigger_arg(bot, triggerargsarray, 1).lower()
        searchterm = get_trigger_arg(bot, triggerargsarray, '1+')
        querystring = get_trigger_arg(bot, triggerargsarray, '2+')
        if (mysite == 'video' or mysite == 'youtube'):
            data = querystring.replace(' ', '+')
            site = '+site%3Ayoutube.com'
            url = 'https://www.youtube.com/'
            url2 = 'https://youtube.com/'
            searchterm = data+site
            query = searchfor(bot, searchterm)
            if not query:
                osd(bot, trigger.sender, 'say', 'I cannot find anything about that')
            else:
                if(str(query).startswith(url) or str(query).startswith(url2)):
                    osd(bot, trigger.sender, 'say', query)
                else:
                    osd(bot, trigger.sender, 'say', query)
                    osd(bot, trigger.sender, 'say', 'Valid website not found')

        elif mysite == 'meme':
            data = querystring.replace(' ', '+')
            site = '+site%3Aknowyourmeme.com'
            url = 'knowyourmeme.com'
            url2 = 'http://knowyourmeme.com'
            searchterm = data+site
            query = searchfor(bot, searchterm)
            if not query:
                osd(bot, trigger.sender, 'say', 'I cannot find anything about that')
            else:
                if(str(query).startswith(url) or str(query).startswith(url2)):
                    osd(bot, trigger.sender, 'say', query)
                else:
                    osd(bot, trigger.sender, 'say', 'I could not find that but check this out: https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        elif mysite == 'walmart':
            data = querystring.replace(' ', '+')
            site = '+site%3Apeopleofwalmart.com'
            url = 'http://www.peopleofwalmart.com'
            url2 = 'https://www.peopleofwalmart.com'
            searchterm = data+site
            query = searchfor(bot, searchterm)
            if not query:
                osd(bot, trigger.sender, 'say', 'https://goo.gl/SsAhv')
            else:
                if(str(query).startswith(url) or str(query).startswith(url2)):
                    osd(bot, trigger.sender, 'say', query)
                else:
                    osd(bot, trigger.sender, 'say', 'I could not find that but check this out: https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        elif mysite == 'urban':
            query = urbansearch(bot, querystring)
            osd(bot, trigger.sender, 'say', query)

        elif mysite == 'imdb' or mysite == 'movie':
            query = moviesearch(bot, querystring)
            osd(bot, trigger.sender, 'say', query)

        else:
            data = searchterm.replace(' ', '+')
            query = searchfor(bot, data)
            if not query:
                osd(bot, trigger.sender, 'say', 'I cannot find anything about that')
            else:
                osd(bot, trigger.sender, 'say', query)


def searchfor(bot, data):
    """Search Google."""
    lookfor = data.replace(':', '%3A')
    var = requests.get(r'http://www.google.com/search?q=' + lookfor + '&btnI')
    query = str(var.url)
    return query


def urbansearch(bot, searchterm):
    """Search Urban Dictionary."""
    try:
        data = web.get("http://api.urbandictionary.com/v0/define?term={0}".format(web.quote(searchterm)))
        data = json.loads(data)
    except:
        return osd(bot, trigger.sender, 'say', "Error connecting to urban dictionary")
    if data['result_type'] == 'no_results':
        return "No results found for {0}".format(searchterm)
    result = data['list'][0]
    url = 'http://www.urbandictionary.com/define.php?term={0}'.format(web.quote(searchterm))
    response = "{0} - {1}".format(result['definition'].strip()[:256], url)
    return response


def moviesearch(bot, searchterm):
    """
    Returns some information about a movie, like Title, Year, Rating, Genre and IMDB Link.
    """
    uri = "http://www.omdbapi.com/?apikey=fd34e58c&"
    data = requests.get(uri, params={'t': searchterm}, timeout=30,
                        verify=bot.config.core.verify_ssl).json()
    if data['Response'] == 'False':
        if 'Error' in data:
            message = '[MOVIE] %s' % data['Error']
        else:
            LOGGER.warning(
                'Got an error from the OMDb api, search phrase was %s; data was %s',
                word, str(data))
            message = '[MOVIE] Got an error from OMDbapi'
    else:
        message = '[MOVIE] Title: ' + data['Title'] + \
                  ' | Year: ' + data['Year'] + \
                  ' | Rating: ' + data['imdbRating'] + \
                  ' | Genre: ' + data['Genre'] + \
                  ' | IMDB Link: http://imdb.com/title/' + data['imdbID']
    return message
