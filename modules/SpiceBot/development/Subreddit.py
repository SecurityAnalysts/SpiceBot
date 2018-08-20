#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
import requests
from fake_useragent import UserAgent
from lxml import html

# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

# author deathbybandaid


@sopel.module.commands('reddit')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):
    url = str("https://www.reddit.com/")
    url = str(url + get_trigger_arg(bot, triggerargsarray, 0))

    page = requests.get(url, headers=header)
    tree = html.fromstring(page.content)

    if page.status_code == 200:
        osd(bot, trigger.sender, 'say', url)
    else:
        osd(bot, trigger.sender, 'say', url + " failed")


@rule(r"""(?:)r/(
          )
          """)
@sopel.module.thread(True)
def mainfunctionnobeguine(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(0), 'create')
    triggerargsarray = get_trigger_arg(bot, triggerargsarray, 0).replace(" ", "")
    triggerargsarray = get_trigger_arg(bot, triggerargsarray, 'create')
    execute_main(bot, trigger, triggerargsarray)
