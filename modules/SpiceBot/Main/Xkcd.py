#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import sys
import os
import html2text
import requests
import re
import urllib2
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

ignored_sites = [
    # For google searching
    'almamater.xkcd.com',
    'blog.xkcd.com',
    'blag.xkcd.com',
    'forums.xkcd.com',
    'fora.xkcd.com',
    'forums3.xkcd.com',
    'store.xkcd.com',
    'wiki.xkcd.com',
    'what-if.xkcd.com',
]
sites_query = ' site:xkcd.com -site:' + ' -site:'.join(ignored_sites)


@sopel.module.commands('xkcd', 'comic')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    verify_ssl = bot.config.core.verify_ssl
    latest = get_info(verify_ssl=verify_ssl)
    maxcomics = latest['num']
    target = spicemanip(bot, triggerargsarray, 1)

    if not target:
        mynumber = getnumber(maxcomics)
        osd(bot, trigger.sender, 'say', 'https://xkcd.com/' + str(mynumber))
    else:
        data = target.strip()
        if data.isdigit():
            mynumber = int(data)
            if not mynumber <= int(maxcomics) and mynumber >= 1:
                osd(bot, trigger.sender, 'say', 'Please enter a number between 1 and ' + str(maxcomics))
                mynumber = maxcomics
            osd(bot, trigger.sender, 'say', 'https://xkcd.com/' + str(mynumber))
        else:
            data.lower()
            data = data.replace(' ', '%20')
            if (data == 'today' or data == 'latest' or data == 'new'):
                mynumber = maxcomics
                osd(bot, trigger.sender, 'say', 'https://xkcd.com/' + str(mynumber))
            elif (data == 'first' or data == 'oldest'):
                mynumber = 1
                osd(bot, trigger.sender, 'say', 'https://xkcd.com/' + str(mynumber))
            elif data == 'random':
                mynumber = getnumber(maxcomics)
                osd(bot, trigger.sender, 'say', 'https://xkcd.com/' + str(mynumber))
            else:
                var = requests.get(r'http://www.google.com/search?q=' + data + '%20site:xkcd.com' + '&btnI')
                if str(var.url).startswith('https://xkcd.com/'):
                    osd(bot, trigger.sender, 'say', str(var.url))
                else:
                    mynumber = getnumber(maxcomics)
                    osd(bot, trigger.sender, 'say', 'https://xkcd.com/' + str(mynumber))


def get_info(number=None, verify_ssl=True):
    if number:
        url = 'http://xkcd.com/{}/info.0.json'.format(number)
    else:
        url = 'http://xkcd.com/info.0.json'
    data = requests.get(url, verify=verify_ssl).json()
    data['url'] = 'http://xkcd.com/' + str(data['num'])
    return data


def getnumber(maxcomics):
    thenumber = random.randint(0, int(maxcomics))
    if not thenumber or thenumber == '\n':
        thenumber = getnumber()
    return thenumber
