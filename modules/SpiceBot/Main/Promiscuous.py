#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib2
import json
import requests
from BeautifulSoup import BeautifulSoup
from random import random
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'


@sopel.module.commands('sexbot', 'cockbot', 'fuckbot')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    rando = randint(2, 22)
    osd(bot, trigger.sender, 'say', "Please insert " + str(rando) + " bitcoins, for that kind of service.")
    price = get_price()
    osd(bot, trigger.sender, 'say', "One bitcoin is priced at $" + str(price) + " right now.")


def get_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    # Convert the price to a floating point number
    return float(response_json[0]['price_usd'])
