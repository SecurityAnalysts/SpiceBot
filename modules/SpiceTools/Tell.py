#!/usr/bin/env python
# coding=utf-8
"""
tell.py - Sopel Tell and Ask Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://sopel.chat
"""

#  Small adjustments made to conform to other SpiceBot modules (opt-in)

from __future__ import unicode_literals, absolute_import, print_function, division

import os
import time
import threading
import sys
from sopel.tools import Identifier, iterkeys
from sopel.tools.time import get_timezone, format_time
from sopel.module import commands, nickname_commands, rule, priority, example
import sopel.module

moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

maximum = 4


# Load things to tell from file
def loadReminders(fn, lock):
    lock.acquire()  # Lock file access
    try:
        result = {}
        f = open(fn)  # open file
        for line in f:
            line = line.strip()
            if sys.version_info.major < 3:
                line = line.decode('utf-8')
            if line:
                try:
                    tellee, teller, verb, timenow, msg = line.split('\t', 4)  # split to key data
                except ValueError:
                    continue  # @@ hmm
                result.setdefault(tellee, []).append((teller, verb, timenow, msg))  # set data to return
        f.close()  # close file
    finally:
        lock.release()  # release lock
    return result  # return info


# write reminders to file
def dumpReminders(fn, data, lock):
    lock.acquire()  # lock file
    try:
        f = open(fn, 'w')  # open file with write access
        for tellee in iterkeys(data):  # go through everything
            for remindon in data[tellee]:
                line = '\t'.join((tellee,) + remindon)
                try:
                    to_write = line + '\n'
                    if sys.version_info.major < 3:
                        to_write = to_write.encode('utf-8')
                    f.write(to_write)  # store the data
                except IOError:
                    break
        try:
            f.close()  # close the file
        except IOError:
            pass
    finally:
        lock.release()  # release the lock
    return True


def setup(self):
    fn = self.nick + '-' + self.config.core.host + '.tell.db'
    self.tell_filename = os.path.join(self.config.core.homedir, fn)
    if not os.path.exists(self.tell_filename):
        try:
            f = open(self.tell_filename, 'w')
        except OSError:
            pass
        else:
            f.write('')
            f.close()
    self.memory['tell_lock'] = threading.Lock()
    self.memory['reminders'] = loadReminders(self.tell_filename, self.memory['tell_lock'])


@commands('tell', 'ask')
@nickname_commands('tell', 'ask')
@example('$nickname, tell Embolalia he broke something again.')
def execute_main(bot, trigger):
    """Give someone a message the next time they're seen"""
    teller = trigger.nick
    verb = trigger.group(1)

    if not trigger.group(3):
        bot.reply("%s whom?" % verb)
        return

    tellee = trigger.group(3).rstrip('.,:;')
    msg = trigger.group(2).lstrip(tellee).lstrip()
    message = str(trigger.group(0))

    if not msg:
        bot.reply("%s %s what?" % (verb, tellee))
        return

    tellee = Identifier(tellee)

    if not os.path.exists(bot.tell_filename):
        return

    if len(tellee) > 20:
        return bot.reply('That nickname is too long.')
    if tellee == bot.nick:
        return bot.reply("I'm here now, you can tell me whatever you want!")
    if tellee.lower() in [u.lower() for u in bot.users]:
        if not message.endswith('please'):
            if not message.startswith('please'):
                return bot.reply("Tell %s that yourself you lazy fuck, they're online now." % tellee)

    if tellee not in (Identifier(teller), bot.nick, 'me'):
        tz = get_timezone(bot.db, bot.config, None, tellee)
        timenow = format_time(bot.db, bot.config, tz, tellee)
        msg = msg.lstrip('please').rstrip('please').lstrip().rstrip()
        bot.memory['tell_lock'].acquire()
        try:
            if tellee not in bot.memory['reminders']:
                bot.memory['reminders'][tellee] = [(teller, verb, timenow, msg)]
            else:
                bot.memory['reminders'][tellee].append((teller, verb, timenow, msg))
        finally:
            bot.memory['tell_lock'].release()

        response = "I'll pass that on when %s is around." % tellee

        bot.reply(response)
    elif Identifier(teller) == tellee:
        osd(bot, trigger.sender, 'say', "You can %s yourself that. I'm not your fucking secretary." % verb)
    else:
        osd(bot, trigger.sender, 'say', "Hey, I'm not as stupid as Monty you know!")

    dumpReminders(bot.tell_filename, bot.memory['reminders'], bot.memory['tell_lock'])  # @@ tell


def getReminders(bot, channel, key, tellee):
    lines = []
    template = "%s: %s <%s> %s %s %s"
    today = time.strftime('%d %b', time.gmtime())

    bot.memory['tell_lock'].acquire()
    try:
        for (teller, verb, datetime, msg) in bot.memory['reminders'][key]:
            if datetime.startswith(today):
                datetime = datetime[len(today) + 1:]
            lines.append(template % (tellee, datetime, teller, verb, tellee, msg))

        try:
            del bot.memory['reminders'][key]
        except KeyError:
            osd(bot, channel, 'action', 'Er...')
    finally:
        bot.memory['tell_lock'].release()
    return lines


@rule('(.*)')
@priority('low')
def message(bot, trigger):

    tellee = trigger.nick
    channel = trigger.sender

    if not os.path.exists(bot.tell_filename):
        return

    reminders = []
    remkeys = list(reversed(sorted(bot.memory['reminders'].keys())))

    for remkey in remkeys:
        if not remkey.endswith('*') or remkey.endswith(':'):
            if tellee == remkey:
                reminders.extend(getReminders(bot, channel, remkey, tellee))
        elif tellee.startswith(remkey.rstrip('*:')):
            reminders.extend(getReminders(bot, channel, remkey, tellee))

    for line in reminders[:maximum]:
        osd(bot, trigger.sender, 'say', line)

    if reminders[maximum:]:
        osd(bot, trigger.sender, 'say', 'Further messages sent privately')
        for line in reminders[maximum:]:
            osd(bot, target, 'action', line)

    if len(bot.memory['reminders'].keys()) != remkeys:
        dumpReminders(bot.tell_filename, bot.memory['reminders'], bot.memory['tell_lock'])  # @@ tell
