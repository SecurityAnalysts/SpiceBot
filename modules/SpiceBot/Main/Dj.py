import sopel.module
import random
import urllib
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

party = 'https://raw.githubusercontent.com/SpiceBot/SpiceBot/master/Text-Files/jukebox_party.txt'
friday = 'https://raw.githubusercontent.com/SpiceBot/SpiceBot/master/Text-Files/jukebox_friday.txt'


@sopel.module.commands('dj')
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
    if not trigger.group(2):
        playlist = party
    else:
        query = trigger.group(2).replace(' ', '20%')
        query = str(query)
        playlist = getplaylist(query)
        if playlist == party:
            osd(bot, trigger.sender, 'say', 'You have selected the Party Playlist')
    song = getsong(playlist)
    if song:
        osd(bot, trigger.sender, 'say', trigger.nick + ' puts a nickel in the jukebox and it starts to play ' + song)
    else:
        osd(bot, trigger.sender, 'say', 'The jukebox starts playing ' + 'Never Gonna Give You Up')


def getsong(playlist):
    htmlfile = urllib.urlopen(playlist)
    lines = htmlfile.read().splitlines()
    mysong = random.choice(lines)
    if not mysong or mysong == '\n':
        mysong = getsong()
        return mysong


def getplaylist(query):
    if query == 'party':
        myplaylist = party
    elif query == 'friday':
        myplaylist = friday
    else:
        myplaylist = party
    return myplaylist
