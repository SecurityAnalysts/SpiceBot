#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib2
from BeautifulSoup import BeautifulSoup
from random import randint
from pyparsing import anyOpenTag, anyCloseTag
from xml.sax.saxutils import unescape as unescape
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('spicyquote')
def execute_main(bot, trigger):
    query = trigger.group(2)
    if query:
        quote = getQuote(bot, query)
        if 'Invalid quote' not in quote:
            if 'http://spice.dussed.com' in quote:
                osd(bot, trigger.sender, 'say', 'That is a long quote! Here is the link: ' + quote)
            else:
                osd(bot, trigger.sender, 'say', quote)
        else:
            osd(bot, trigger.sender, 'say', "I can't seem to find that quote! Are you sure it exists?")
    else:
        osd(bot, trigger.sender, 'say', "Please provide a quote number or search term and try again!")


def getQuote(bot, query):
    unescape_xml_entities = lambda s: unescape(s, {"&apos;": "'", "&quot;": '"', "&nbsp;": " "})
    stripper = (anyOpenTag | anyCloseTag).suppress()
    urlsuffix = 'http://spice.dussed.com/?'
    if query.isdigit():
        qNum = query
        url = urlsuffix + qNum
    else:
        url = urlsuffix + 'do=search&q=' + query
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    links = []
    qlinks = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    if links == []:
        txt = "Invalid quote"
        return txt
    for qlink in links:
        if str(qlink).startswith("./?"):
            link = qlink.replace(".", "http://spice.dussed.com")
            qlinks.append(link)
    url = spicemanip(bot, qlinks, 'random')  # update when replacement happens
    if url == '':
        txt = "Invalid quote"
        return txt
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    txt = soup.find('td', {'class': 'body'}).text
    txt = unescape_xml_entities(stripper.transformString(txt))
    if len(txt) > 200:
        quote = url
    else:
        quote = txt
    return quote
