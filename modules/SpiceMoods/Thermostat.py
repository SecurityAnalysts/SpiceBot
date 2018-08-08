#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid

temp_scales = ['kelvin', 'celsius', 'fahrenheit', 'rankine', 'romer', 'newton', 'delisle', 'reaumur']
temp_scales_short = ['K', 'C', 'F', 'Ra', 'Ro', 'N', 'D', 'Re']


@sopel.module.commands('thermostat')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    tempcommand = get_trigger_arg(bot, triggerargsarray, 1) or 0
    tempcommand = tempcommand.lower()

    currenttemp = get_database_value(bot, botcom.channel_current, 'temperature') or 32
    currentscale = get_database_value(bot, botcom.channel_current, 'temperature_scale') or 'fahrenheit'

    if not tempcommand or tempcommand in temp_scales or tempcommand in temp_scales_short:
        if tempcommand in temp_scales or tempcommand in temp_scales_short:
            if tempcommand in temp_scales_short:
                tempcommand = array_compare(bot, tempcommand, temp_scales_short, temp_scales)
            tempconvert = tempcommand
        else:
            tempconvert = get_trigger_arg(bot, temp_scales, 'random')
        if tempconvert != currentscale:
            currenttemp = temperature(bot, currenttemp, currentscale, tempconvert)
        osd(bot, botcom.channel_current, 'say', "The current temperature in " + botcom.channel_current + " is " + str(currenttemp) + "° " + str(tempconvert.title()) + ".")
        return

    missingarray = []

    number = get_trigger_arg(bot, [x for x in triggerargsarray if str(x).isdigit], 1) or 0
    if not number:
        missingarray.append("number")

    tempscale = get_trigger_arg(bot, [x for x in triggerargsarray if x in temp_scales or x in temp_scales_short], 1) or 0
    if not tempscale:
        missingarray.append("temperature scale")

    if missingarray != []:
        missinglist = get_trigger_arg(bot, missingarray, 'list')
        osd(bot, botcom.channel_current, 'say', "The following values were missing: " + missinglist)
        return

    if tempscale in temp_scales_short:
        tempscale = array_compare(bot, tempscale, temp_scales_short, temp_scales)

    set_database_value(bot, botcom.channel_current, 'temperature', number)
    set_database_value(bot, botcom.channel_current, 'temperature_scale', tempscale)

    osd(bot, botcom.channel_current, 'say', botcom.instigator + " has set the temperature in " + botcom.channel_current + " to " + str(number) + "° " + str(tempscale) + ".")


def temperature(bot, degree, original, desired):
    temperature = 0

    if original != 'kelvin':
        kelvin = eval(str(original.lower() + "_to_kelvin(bot, degree)"))
    else:
        kelvin = degree

    if desired != 'kelvin':
        temperature = eval("kelvin_to_" + str(desired.lower() + "(bot, degree)"))
    else:
        temperature = kelvin

    return temperature


"""
Celsius
"""


def celsius_to_kelvin(bot, degree):
    celsius = float(degree)
    kelvin = (celsius + 273)
    return kelvin


def kelvin_to_celsius(bot, degree):
    kelvin = float(degree)
    celsius = (kelvin - 273)
    return celsius


"""
Fahrenheit
"""


def fahrenheit_to_kelvin(bot, degree):
    fahrenheit = float(degree)
    kelvin = ((5/9) * (fahrenheit - 32) + 273)
    return kelvin


def kelvin_to_fahrenheit(bot, degree):
    kelvin = float(degree)
    fahrenheit = (1.8 * (kelvin - 273) + 32)
    return fahrenheit


"""
Rankine
"""


def rankine_to_kelvin(bot, degree):
    rankine = float(degree)
    kelvin = (rankine * (5/9))
    return kelvin


def kelvin_to_rankine(bot, degree):
    kelvin = float(degree)
    rankine = (kelvin * (9/5))
    return rankine


"""
Delisle
"""


def delisle_to_kelvin(bot, degree):
    delisle = float(degree)
    kelvin = (373 - (delisle * (2/3)))
    return kelvin


def kelvin_to_delisle(bot, degree):
    kelvin = float(degree)
    delisle = ((373 - kelvin) * (3/2))
    return delisle


"""
Newton
"""


def newton_to_kelvin(bot, degree):
    newton = float(degree)
    kelvin = (newton * (100/33) + 273)
    return kelvin


def kelvin_to_newton(bot, degree):
    kelvin = float(degree)
    newton = ((kelvin - 273) * (33/100))
    return newton


"""
Reaumur
"""


def reaumur_to_kelvin(bot, degree):
    reaumur = float(degree)
    kelvin = (reaumur * (5/4) + 273)
    return kelvin


def kelvin_to_reaumur(bot, degree):
    kelvin = float(degree)
    reaumur = ((kelvin - 273) * (4/5))
    return reaumur


"""
Romer
"""


def romer_to_kelvin(bot, degree):
    romer = float(degree)
    kelvin = ((romer - 7.5) * (40/21) + 273)
    return kelvin


def kelvin_to_romer(bot, degree):
    kelvin = float(degree)
    romer = ((kelvin - 273) * (21/40) + 7.5)
    return romer
