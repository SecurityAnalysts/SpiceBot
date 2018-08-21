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


def execute_main(bot, trigger, triggerargsarray):

    if str(get_trigger_arg(bot, triggerargsarray, 0)).startswith("u"):
        urltype = 'user'
    else:
        urltype = 'subreddit'
    url = str("https://www.reddit.com/")
    url = str(url + get_trigger_arg(bot, triggerargsarray, 0))

    page = requests.get(url, headers=header)
    tree = html.fromstring(page.content)

    if page.status_code == 200:
        osd(bot, trigger.sender, 'say', url + " is a valid " + urltype + "!")
    else:
        osd(bot, trigger.sender, 'say', url + " is not a valid " + urltype + ".")


@rule(r"""(?:)r/
          (
            (?:\\/ | [^/])+
          )
          """)
@rule(r"""(?:)u/
          (
            (?:\\/ | [^/])+
          )
          """)
@sopel.module.thread(True)
def mainfunctionnobeguine(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(0), 'create')
    execute_main(bot, trigger, triggerargsarray)
