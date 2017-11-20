import sopel.module
import os
import sys
import re
from os.path import exists
import git 

script_dir = os.path.dirname(__file__)
log_path = "data/templog.txt"
log_pathc = "data/*.txt"
log_file_path = os.path.join(script_dir, log_path)

@sopel.module.require_admin
@sopel.module.require_privmsg
@sopel.module.commands('spicebotadmin')
def spicebotadmin(bot, trigger):
    for c in bot.channels:
        channel = c
    options = str("update, restart, debugreset, debug, pipinstall")
    service = bot.nick.lower()
    if not trigger.group(2):
        bot.say("Which Command Do You want To run?")
        bot.say("Options Are: " + options)
    else:
        commandused = trigger.group(3)
        if commandused == 'update':
            bot.msg(channel, trigger.nick + " commanded me to update from Github and restart. Be Back Soon!")
            update(bot, trigger)
            #cleandir(bot, trigger)
            #debuglogreset(bot, trigger)
            restart(bot, trigger, service)
        elif commandused == 'restart':
            bot.msg(channel, trigger.nick + " Commanded me to restart. Be Back Soon!")
            #cleandir(bot, trigger)
            #debuglogreset(bot, trigger)
            restart(bot, trigger, service)
        #elif commandused == 'debugreset':
            #debuglogreset(bot, trigger)
        elif commandused == 'debug':
            debugloglinenumberarray = []
            bot.action('Is Copying Log')
            os.system("sudo journalctl -u " + service + " >> " + log_file_path)
            bot.action('Is Filtering Log')
            search_phrase = "Welcome to Sopel. Loading modules..."
            ignorearray = ['COMMAND=/bin/journalctl','pam_unix(sudo:session): session opened for user root']
            mostrecentstartbot = 0
            with open(log_file_path) as f:
                line_num = 0
                for line in f:
                    line_num += 1
                    if search_phrase in line:
                        mostrecentstartbot = line_num
                line_num = 0
            with open(log_file_path) as fb:
                for line in fb:
                    line_num += 1
                    currentline = line_num
                    if int(currentline) >= int(mostrecentstartbot):
                        for x in ignorearray:
                            if x not in line:
                                bot.say(line)
            bot.action('Is Removing Log')
            os.system("sudo rm " + log_file_path)
        elif commandused == 'pipinstall':
            pippackage = trigger.group(4)
            if not pippackage:
                bot.say("You must specify a pip package")
            else:
                bot.say("attempting to install " + pippackage)
                os.system("sudo pip install " + pippackage)
                bot.say('Possibly done installing ' + pippackage)

def restart(bot, trigger, service):
    bot.say('Restarting Service...')
    os.system("sudo service " + str(service) + " restart")
    bot.say('If you see this, the service is hanging. Making another attempt.')

def update(bot, trigger):
    bot.say('Pulling From Github...')
    g = git.cmd.Git(script_dir)
    g.pull()
    
def cleandir(bot, trigger):
    bot.say('Cleaning Directory...')
    os.system("sudo rm " + script_dir + "/*.pyc")
    
def debuglogreset(bot, trigger):
    service = bot.nick.lower()
    bot.action('Is Copying Log')
    os.system("sudo journalctl -u " + service + " >> " + log_file_path)
    bot.action('Is Removing Log')
    os.system("sudo rm " + log_file_path)
