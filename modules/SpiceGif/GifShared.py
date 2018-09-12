#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import ConfigParser
import requests
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
gifshareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(gifshareddir)
from BotShared import *
from GifShared import *

# creds
config = ConfigParser.ConfigParser()
config.read("/home/spicebot/spicebot.conf")


"""
Giphy
"""


giphyapi = config.get("giphy", "apikey")
giphylimit = 50


def getGif_giphy(bot, query, searchnum, searchlimit=giphylimit):

    returngifdict = {
                    "query": query,
                    "searchquery": query,
                    "querysuccess": False,
                    "returnnum": searchnum,
                    "returnurl": None,
                    "error": None
                    }

    # Make sure there is a valid input of query and search number
    if not query:
        returngifdict["error"] = 'No Query to Search'
        return returngifdict
    if not str(searchnum).isdigit() and searchnum != 'random':
        returngifdict["error"] = 'No Search Number or Random Specified'
        return returngifdict

    # spaces in query
    searchquery = query.replace(' ', '%20')
    returngifdict["searchquery"] = searchquery

    # Random
    if searchnum == 'random':
        searchnum = randint(0, searchlimit)

    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(searchquery) + '&api_key=' + str(giphyapi) + '&limit=' + str(searchlimit) + '&rating=r'
    data = json.loads(urllib2.urlopen(url).read())

    # Verifythere are results
    resultsamount = data['pagination']['total_count']
    returngifdict["resultsamount"] = resultsamount
    if not resultsamount:
        return returngifdict
    returngifdict["querysuccess"] = True

    if int(searchnum) > int(resultsamount):
        searchnum = resultsamount
    returngifdict["returnnum"] = searchnum

    id = data['data'][searchnum]['id']
    returngifdict["returnurl"] = 'https://media2.giphy.com/media/'+id+'/giphy.gif'

    return returngifdict


"""
Tenor
"""

tenorapi = config.get("tenor", "apikey")
tenorlimit = 50


def getGif_tenor(bot, query, searchnum, searchlimit=tenorlimit):

    returngifdict = {
                    "query": query,
                    "searchquery": query,
                    "querysuccess": False,
                    "returnnum": searchnum,
                    "returnurl": None,
                    "error": None
                    }

    # Make sure there is a valid input of query and search number
    if not query:
        returngifdict["error"] = 'No Query to Search'
        return returngifdict
    if not str(searchnum).isdigit() and searchnum != 'random':
        returngifdict["error"] = 'No Search Number or Random Specified'
        return returngifdict

    # spaces in query
    searchquery = query.replace(' ', '%20')
    returngifdict["searchquery"] = searchquery

    # Random
    if searchnum == 'random':
        searchnum = randint(0, searchlimit)

    url = 'https://api.tenor.com/v1/search?q=' + str(searchquery) + '&key=' + str(tenorapi) + '&limit=' + str(searchlimit)  # + '&anon_id=r' + str(anon_id)
    data = json.loads(urllib2.urlopen(url).read())

    # Verifythere are results
    resultsamount = len(data['results'])
    if not resultsamount:
        return returngifdict
    returngifdict["querysuccess"] = True

    if int(searchnum) > int(resultsamount):
        searchnum = resultsamount
    returngifdict["returnnum"] = searchnum

    returngifdict["returnurl"] = data['results'][searchnum]['media'][0]['gif']['url']

    return returngifdict
