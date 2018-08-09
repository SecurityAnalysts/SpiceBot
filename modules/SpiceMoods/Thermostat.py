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
temp_scales_short = ['k', 'c', 'f', 'ra', 'ro', 'n', 'd', 're']


@sopel.module.commands('thermostat', 'temp')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'thermostat')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    triggerargsarray = get_trigger_arg(bot, triggerargsarray, 'lower')

    tempcommand = get_trigger_arg(bot, triggerargsarray, 1) or 0

    currenttemp = get_database_value(bot, botcom.channel_current, 'temperature') or 32
    currentscale = get_database_value(bot, botcom.channel_current, 'temperature_scale') or 'fahrenheit'

    if not tempcommand or tempcommand in temp_scales or tempcommand in temp_scales_short:
        if tempcommand in temp_scales or tempcommand in temp_scales_short:
            if tempcommand in temp_scales_short:
                tempcommand = array_compare(bot, tempcommand, temp_scales_short, temp_scales)
            tempconvert = tempcommand
        else:
            tempconvert = get_trigger_arg(bot, temp_scales, 'random')
        currenttemp = temperature(bot, currenttemp, currentscale, tempconvert)
        tempcond = temp_condition(bot, currenttemp, tempconvert)
        osd(bot, botcom.channel_current, 'say', "The current temperature in " + botcom.channel_current + " is " + str(currenttemp) + "° " + str(tempconvert.title()) + ". " + tempcond)
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

    tempcond = temp_condition(bot, number, tempscale)

    osd(bot, botcom.channel_current, 'say', botcom.instigator + " has set the temperature in " + botcom.channel_current + " to " + str(number) + "° " + str(tempscale.title()) + ". " + tempcond)


def temp_condition(bot, degree, degreetype):

    comment = ''

    kelvin = eval(str(degreetype.lower() + "_to_kelvin(bot, degree)"))

    if int(kelvin) == 0:
        comment = "Absolute zero has been reached, a spaceheater won't even help."
    elif int(kelvin) <= 273:
        comment = "Everyone in the channel grabs a jacket, as they watch their beverages turn to ice."
    elif int(kelvin) > 299 and int(kelvin) <= 305:
        comment = "Everyone in the channel feels sleepy."
    elif int(kelvin) > 305 and int(kelvin) <= 313:
        comment = "Everyone in the channel feels exhausted."
    elif int(kelvin) > 313 and int(kelvin) <= 327:
        comment = "Everyone in the channel gets heat cramps."
    elif int(kelvin) > 327 and int(kelvin) <= 373:
        comment = "Everyone in the channel gets heat stroke."
    elif int(kelvin) > 373 and int(kelvin) < 5800:
        comment = "Everyone in the channel feels their blood start to boil"
    elif int(kelvin) >= 5800:
        comment = "You have reached the surface of the sun. There is no SPF that will protect you."

    return comment


def temperature(bot, degree, original, desired):
    temperature = 0

    kelvin = eval(str(original.lower() + "_to_kelvin(bot, degree)"))
    temperature = eval("kelvin_to_" + str(desired.lower() + "(bot, kelvin)"))

    return temperature


"""
Kelvin
"""


def kelvin_to_kelvin(bot, kelvin):
    kelvin = float(kelvin)
    return kelvin


"""
Celsius
"""


def celsius_to_kelvin(bot, celsius):
    celsius = float(celsius)
    kelvin = (celsius + 273.15)
    return kelvin


def kelvin_to_celsius(bot, kelvin):
    kelvin = float(kelvin)
    celsius = (kelvin - 273.15)
    return celsius


"""
Fahrenheit
"""


def fahrenheit_to_kelvin(bot, fahrenheit):
    fahrenheit = float(fahrenheit)
    kelvin = ((fahrenheit + 459.67) / 1.8)
    return kelvin


def kelvin_to_fahrenheit(bot, kelvin):
    kelvin = float(kelvin)
    fahrenheit = (1.8 * kelvin + 459.67)
    return fahrenheit


"""
Rankine
"""


def rankine_to_kelvin(bot, rankine):
    rankine = float(rankine)
    kelvin = (rankine / 1.8)
    return kelvin


def kelvin_to_rankine(bot, kelvin):
    kelvin = float(kelvin)
    rankine = (1.8 * kelvin)
    return rankine


"""
Delisle
"""


def delisle_to_kelvin(bot, delisle):
    delisle = float(delisle)
    kelvin = (373.15 - (2/3) * delisle)
    return kelvin


def kelvin_to_delisle(bot, kelvin):
    kelvin = float(kelvin)
    delisle = (1.5 * (373.15 - kelvin))
    return delisle


"""
Newton
"""


def newton_to_kelvin(bot, newton):
    newton = float(newton)
    kelvin = ((100 / 33) * newton + 273.15)
    return kelvin


def kelvin_to_newton(bot, kelvin):
    kelvin = float(kelvin)
    newton = (0.33 * (kelvin - 273.15))
    return newton


"""
Reaumur
"""


def reaumur_to_kelvin(bot, reaumur):
    reaumur = float(reaumur)
    kelvin = (1.25 * reaumur + 273.15)
    return kelvin


def kelvin_to_reaumur(bot, kelvin):
    kelvin = float(kelvin)
    reaumur = (0.8 * (kelvin - 273.15))
    return reaumur


"""
Romer
"""


def romer_to_kelvin(bot, romer):
    romer = float(romer)
    kelvin = ((40 / 21) * (romer - 7.5) + 273.15)
    return kelvin


def kelvin_to_romer(bot, kelvin):
    kelvin = float(kelvin)
    romer = ((21 / 40) * (kelvin - 273.15) + 7.5)
    return romer
