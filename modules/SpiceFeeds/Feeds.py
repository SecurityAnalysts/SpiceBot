#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import ConfigParser
import requests
from lxml import html
import datetime
from time import strptime
from dateutil import parser
import calendar
import arrow
import pytz
from dateutil import tz
from xml.dom import minidom
import json
from fake_useragent import UserAgent
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

# author deathbybandaid

feeds_dir = "feeds/"
feeds_file_path = os.path.join(moduledir, feeds_dir)


# Automatic Run
@sopel.module.interval(60)
def autofeeds(bot):
    # feeds dynamic Class
    feeds = class_create('feeds')
    feeds = feeds_configs(bot, feeds)
    for feed in feeds.list:
        dispmsg = feeds_display(bot, feed, feeds, 0) or []
        if dispmsg != []:
            for channel in bot.channels:
                channelmodulesarray = get_database_value(bot, channel, 'modules_enabled') or []
                if 'feeds' in channelmodulesarray:
                    feed_enabled = get_database_value(bot, channel, 'feeds_enabled') or []
                    if feed in feed_enabled:
                        osd(bot, channel, 'say', dispmsg)
            users_current = []
            for user in bot.users:
                users_current.append(str(user))
            for user in users_current:
                feed_enabled = get_database_value(bot, user, 'feeds_enabled') or []
                if feed in feed_enabled:
                    osd(bot, user, 'priv', dispmsg)


@sopel.module.commands('feeds', 'packt', 'spicewebby', 'atwebby', 'comptiawebby', 'spiceworkswebby', 'actualtechwebby', 'onion', 'theonion', 'dilbert')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'feeds')
    if not enablestatus:
        if trigger.group(1) == 'feeds':
            execute_main(bot, trigger, triggerargsarray, botcom, instigator)
        else:
            # feeds dynamic Class
            feeds = class_create('feeds')
            feeds = feeds_configs(bot, feeds)
            feed = trigger.group(1)
            if feed == 'spicewebby':
                feed = 'spiceworkswebby'
            elif feed == 'atwebby':
                feed = 'actualtechwebby'
            elif feed == 'onion':
                feed = 'theonion'
            dispmsg = feeds_display(bot, feed, feeds, 1) or []
            if dispmsg == []:
                osd(bot, botcom.channel_current, 'say', feed + " appears to have had an unknown error.")
            else:
                osd(bot, botcom.channel_current, 'say', dispmsg)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    # feeds dynamic Class
    feeds = class_create('feeds')

    valid_commands = ['enable', 'disable', 'reset', 'run', 'subscribe', 'unsubscribe']
    command = get_trigger_arg(bot, [x for x in triggerargsarray if x in valid_commands], 1) or 'run'
    if command in triggerargsarray:
        triggerargsarray.remove(command)

    feeds = feeds_configs(bot, feeds)

    feed_select = get_trigger_arg(bot, [x for x in triggerargsarray if x in feeds.list or x == 'all'], 1) or 'nofeed'
    if feed_select == 'nofeed':
        feed_list = get_trigger_arg(bot, feeds.list, 'list')
        osd(bot, botcom.channel_current, 'say', "Valid Feeds are " + feed_list)
        return
    if feed_select == 'all':
        current_feed_list = feeds.list
    else:
        current_feed_list = []
        for word in triggerargsarray:
            if word in feeds.list:
                current_feed_list.append(word)

    if command == 'run':
        for feed in current_feed_list:
            dispmsg = feeds_display(bot, feed, feeds, 1) or []
            if dispmsg == []:
                osd(bot, botcom.channel_current, 'say', feed_select + " appears to have had an unknown error.")
            else:
                if feed_select == 'all':
                    osd(bot, botcom.instigator, 'priv', dispmsg)
                else:
                    osd(bot, botcom.channel_current, 'say', dispmsg)
        return

    if command == 'subscribe':
        instigatormodulesarray = get_database_value(bot, botcom.instigator, 'feeds_enabled') or []
        newlist = []
        for feed in current_feed_list:
            if feed not in instigatormodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_database_array(bot, botcom.instigator, newlist, 'feeds_enabled', 'add')
            osd(bot, botcom.channel_current, 'say', "You are now " + command + "d to " + get_trigger_arg(bot, newlist, 'list'))
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if command == 'unsubscribe':
        instigatormodulesarray = get_database_value(bot, botcom.instigator, 'feeds_enabled') or []
        newlist = []
        for feed in current_feed_list:
            if feed in instigatormodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_database_array(bot, botcom.instigator, newlist, 'feeds_enabled', 'del')
            osd(bot, botcom.channel_current, 'say', "You are now " + command + "d from " + get_trigger_arg(bot, newlist, 'list'))
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if instigator.default not in botcom.opadmin:
        osd(bot, botcom.channel_current, 'say', "Only Bot Admins and Channel Operators are able to adjust Feed settings.")
        return

    if command == 'reset':
        newlist = []
        for feed in current_feed_list:
            feed_type = eval("feeds." + feed + ".type")
            if feed_type in ['rss', 'youtube', 'scrape', 'json']:
                newlist.append(feed)
        if newlist != []:
            for feed in newlist:
                reset_database_value(bot, bot.nick, feed + '_lastbuildcurrent')
            osd(bot, botcom.channel_current, 'say', get_trigger_arg(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    channelselect = get_trigger_arg(bot, [x for x in triggerargsarray if x in botcom.channel_list], 1) or botcom.channel_current

    if command == 'enable':
        channelmodulesarray = get_database_value(bot, channelselect, 'feeds_enabled') or []
        newlist = []
        for feed in current_feed_list:
            if feed not in channelmodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_database_array(bot, channelselect, newlist, 'feeds_enabled', 'add')
            osd(bot, botcom.channel_current, 'say', get_trigger_arg(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + "d for " + str(channelselect) + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if command == 'disable':
        channelmodulesarray = get_database_value(bot, channelselect, 'feeds_enabled') or []
        newlist = []
        for feed in current_feed_list:
            if feed in channelmodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_database_array(bot, channelselect, newlist, 'feeds_enabled', 'del')
            osd(bot, botcom.channel_current, 'say', get_trigger_arg(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + "d for " + str(channelselect) + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return


def feeds_display(bot, feed, feeds, displayifnotnew):

    dispmsg = []
    titleappend = 0

    url = eval("feeds." + feed + ".url")
    if feed == 'spicebot':
        if bot.nick.endswith('dev'):
            url = url.replace("master", "dev")
    page = requests.get(url, headers=header)
    tree = html.fromstring(page.content)

    if page.status_code == 200:

        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=pytz.UTC)

        displayname = eval("feeds." + feed + ".displayname")

        feed_type = eval("feeds." + feed + ".type")

        if feed_type in ['rss', 'youtube', 'github']:

            lastbuildcurrent = get_database_value(bot, bot.nick, feed + '_lastbuildcurrent') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            lastbuildcurrent = parser.parse(str(lastbuildcurrent))

            xml = page.text
            xml = xml.encode('ascii', 'ignore').decode('ascii')
            xmldoc = minidom.parseString(xml)

            lastbuildtype = eval("feeds." + feed + ".lastbuildtype")
            lastBuildXML = xmldoc.getElementsByTagName(lastbuildtype)
            lastbuildparent = int(eval("feeds." + feed + ".lastbuildparent"))
            lastbuildchild = int(eval("feeds." + feed + ".lastbuildchild"))
            lastBuildXML = lastBuildXML[lastbuildparent].childNodes[lastbuildchild].nodeValue
            lastBuildXML = parser.parse(str(lastBuildXML))

            if displayifnotnew or lastBuildXML > lastbuildcurrent:

                titleappend = 1

                titletype = eval("feeds." + feed + ".titletype")
                titles = xmldoc.getElementsByTagName(titletype)
                titleparent = int(eval("feeds." + feed + ".titleparent"))
                titlechild = int(eval("feeds." + feed + ".titlechild"))
                title = titles[titleparent].childNodes[titlechild].nodeValue
                if feed_type == 'github':
                    authors = xmldoc.getElementsByTagName('name')
                    author = authors[0].childNodes[0].nodeValue
                    dispmsg.append(author + " committed")
                title = unicode_string_cleanup(title)
                dispmsg.append(title)

                linktype = eval("feeds." + feed + ".linktype")
                links = xmldoc.getElementsByTagName(linktype)
                linkparent = int(eval("feeds." + feed + ".linkparent"))
                linkchild = eval("feeds." + feed + ".linkchild")
                if str(linkchild).isdigit():
                    linkchild = int(linkchild)
                    link = links[linkparent].childNodes[linkchild].nodeValue.split("?")[0]
                else:
                    link = links[linkparent].getAttribute(linkchild)
                dispmsg.append(link)

                if not displayifnotnew:
                    set_database_value(bot, bot.nick, feed + '_lastbuildcurrent', str(lastBuildXML))

        elif feed_type == 'webinar':

            scrapetime = eval("feeds." + feed + ".time")
            scrapetimezone = eval("feeds." + feed + ".timezone")

            webbytime = str(tree.xpath(scrapetime))
            for r in (("['", ""), ("']", ""), ("\\n", ""), ("\\t", ""), ("@ ", "")):
                webbytime = webbytime.replace(*r)

            if feed == 'spiceworkswebby':
                webbytime = str(webbytime.split("+", 1)[0])

            webbytz = pytz.timezone(scrapetimezone)
            webbytime = parser.parse(webbytime)
            webbytime = webbytz.localize(webbytime)

            timeuntil = (webbytime - now).total_seconds()

            if displayifnotnew or (int(timeuntil) < 900 and int(timeuntil) > 840):

                titleappend = 1

                timecompare = get_timeuntil(now, webbytime)
                dispmsg.append("{" + timecompare + "}")

                scrapetitle = eval("feeds." + feed + ".title")
                webbytitle = str(tree.xpath(scrapetitle))
                for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
                    webbytitle = webbytitle.replace(*r)
                webbytitle = unicode_string_cleanup(webbytitle)
                dispmsg.append(webbytitle)

                scrapelink = eval("feeds." + feed + ".link")
                webbylink = str(tree.xpath(scrapelink))
                for r in (("['", ""), ("']", "")):
                    webbylink = webbylink.replace(*r)
                if feed == 'actualtechwebby':
                    webbylink = str(url + webbylink.split("&", 1)[0])
                webbylinkprecede = eval("feeds." + feed + ".linkprecede")
                if webbylinkprecede != 'noprecede':
                    webbylink = str(webbylinkprecede + webbylink)
                dispmsg.append(webbylink)

                scrapebonus = eval("feeds." + feed + ".bonus")
                if scrapebonus != 'nobonus':
                    webbybonus = ''
                    try:
                        webbybonus = str(tree.xpath(scrapebonus))
                        if feed == 'spiceworkswebby':
                            webbybonus = str(webbybonus.split("BONUS: ", 1)[1])
                        for r in (("\\r", ""), ("\\n", ""), ("']", ""), ("]", ""), ('"', ''), (" '", ""), ("['", ""), ("[", "")):
                            webbybonus = webbybonus.replace(*r)
                        webbybonus = unicode_string_cleanup(webbybonus)
                    except IndexError:
                        webbybonus = ''
                    if webbybonus != '':
                        dispmsg.append('BONUS: ' + webbybonus)

        elif feed_type == 'daily':

            timehour = eval("feeds." + feed + ".hour")
            timeminute = eval("feeds." + feed + ".minute")
            scrapetimezone = eval("feeds." + feed + ".timezone")

            dailytz = pytz.timezone(scrapetimezone)
            nowtime = datetime.datetime.now(dailytz)
            tomorrow = nowtime + datetime.timedelta(days=1)
            dailytime = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, int(timehour), int(timeminute), 0, 0)
            dailytime = dailytz.localize(dailytime)
            timeuntil = (dailytime - nowtime).total_seconds()

            if displayifnotnew or (nowtime.hour == int(timehour) and nowtime.minute == int(timeminute)):

                scrapetitle = eval("feeds." + feed + ".title")
                title = str(tree.xpath(scrapetitle))
                for r in (("\\t", ""), ("\\n", ""), ("['", ""), ("']", ""), ("]", "")):
                    title = title.replace(*r)
                if title == "[]" or title == '':
                    title = "No Book Today"
                title = unicode_string_cleanup(title)
                dispmsg.append(title)

                titleappend = 1

                timecompare = get_timeuntil(now, dailytime)
                dispmsg.append("{Next " + timecompare + "}")

                dispmsg.append("URL: " + url)

        elif feed_type == 'scrape':

            scrapetime = eval("feeds." + feed + ".time")

            scrapedtime = str(tree.xpath(scrapetime))
            for r in (("['", ""), ("']", ""), ("\\n", ""), ("\\t", ""), ("@ ", "")):
                scrapedtime = scrapedtime.replace(*r)
            scrapedtime = parser.parse(str(scrapedtime)).replace(tzinfo=pytz.UTC)

            lastbuildcurrent = get_database_value(bot, bot.nick, feed + '_lastbuildcurrent') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            lastbuildcurrent = parser.parse(str(lastbuildcurrent))

            if displayifnotnew or scrapedtime > lastbuildcurrent:

                titleappend = 1

                scrapetitle = eval("feeds." + feed + ".title")
                scrapedtitle = str(tree.xpath(scrapetitle))
                for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
                    scrapedtitle = scrapedtitle.replace(*r)
                scrapedtitle = unicode_string_cleanup(scrapedtitle)
                dispmsg.append(scrapedtitle)

                scrapelink = eval("feeds." + feed + ".link")
                scrapedlink = str(tree.xpath(scrapelink))
                for r in (("['", ""), ("']", "")):
                    scrapedlink = scrapedlink.replace(*r)
                scrapedlinkprecede = eval("feeds." + feed + ".linkprecede")
                if scrapedlinkprecede != 'noprecede':
                    scrapedlink = str(scrapedlinkprecede + scrapedlink)
                dispmsg.append(scrapedlink)

            if not displayifnotnew:
                set_database_value(bot, bot.nick, feed + '_lastbuildcurrent', str(scrapedtime))

        elif feed_type == 'json':

            prefix = eval("feeds." + feed + ".prefix")
            searchterm = eval("feeds." + feed + ".searchterm")
            suffix = eval("feeds." + feed + ".suffix")

            # if str(searchterm).startswith("http"):
            #    searchtermpage = requests.get(searchterm, headers={'Accept': 'text/plain'})
            #    searchterm = searchtermpage.content

            # combinedjson = str(url + prefix + searchterm + suffix)
            # bot.say(str(combinedjson))

            # verify_ssl = bot.config.core.verify_ssl
            # data = requests.get(combinedjson, verify=verify_ssl).json()
            # bot.say(str(data))

            # title = data.get('title')
            # bot.say(str(title))

            # titleappend = 1

            # contentpage = requests.get(combinedjson)
            # result = contentpage.content
            # jsonload = json.loads(result)
            # jsonpart = jsonload['joke']

            # contentpage = requests.get(combinedjson, headers={'Accept': 'text/plain'})
            # content = contentpage.content
            # bot.say(str(jsonload))

            # lastbuildcurrent = get_database_value(bot, bot.nick, feed + '_lastbuildcurrent') or

            # if not displayifnotnew:
            #    set_database_value(bot, bot.nick, feed + '_lastbuildcurrent', str(lastBuildXML))

        if titleappend:
            dispmsg.insert(0, "[" + displayname + "]")

    return dispmsg


# rss feeds list
def feeds_configs(bot, feeds):
    feeds.list = []
    for feed_dir_type in os.listdir(feeds_file_path):
        feed_type_file_path = os.path.join(feeds_file_path, feed_dir_type)
        for feed in os.listdir(feed_type_file_path):

            # Add to main list
            feeds.list.append(feed)

            # Every feed gets a class
            current_feed = class_create(feed)
            exec("feeds." + feed + " = current_feed")

            # file name
            exec("feeds." + feed + ".feed_filename = feed")

            # get file path
            feedfile = os.path.join(feed_type_file_path, feed)
            exec("feeds." + feed + ".file_path = feedfile")

            # Read configuration
            config = ConfigParser.ConfigParser()
            config.read(feedfile)
            for each_section in config.sections():
                for (each_key, each_val) in config.items(each_section):
                    exec("feeds." + feed + "." + each_key + " = each_val")

    return feeds


def hashave(mylist):
    if len(mylist) > 1:
        hashave = 'have'
    else:
        hashave = 'has'
    return hashave
