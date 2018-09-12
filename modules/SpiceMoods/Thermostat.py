#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from collections import OrderedDict
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
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    triggerargsarray = spicemanip(bot, triggerargsarray, 'lower')

    tempcommand = spicemanip(bot, triggerargsarray, 1) or 0

    currenttemp = get_database_value(bot, botcom.channel_current, 'temperature') or 32
    currentscale = get_database_value(bot, botcom.channel_current, 'temperature_scale') or 'fahrenheit'

    if not tempcommand or tempcommand in temp_scales or tempcommand in temp_scales_short:
        if tempcommand in temp_scales or tempcommand in temp_scales_short:
            if tempcommand in temp_scales_short:
                tempcommand = spicemanip(bot, [tempcommand, temp_scales_short, temp_scales], 'index')
            tempconvert = tempcommand
        else:
            tempconvert = spicemanip(bot, temp_scales, 'random')
        currenttemp = temperature(bot, currenttemp, currentscale, tempconvert)
        tempcond = temp_condition(bot, currenttemp, tempconvert)
        osd(bot, botcom.channel_current, 'say', "The current temperature in " + botcom.channel_current + " is " + str(currenttemp) + "° " + str(tempconvert.title()) + ". " + tempcond)
        return

    missingarray = []

    number = spicemanip(bot, [x for x in triggerargsarray if str(x).isdigit], 1) or 0
    if not number:
        missingarray.append("number")

    tempscale = spicemanip(bot, [x for x in triggerargsarray if x in temp_scales or x in temp_scales_short], 1) or 0
    if not tempscale:
        missingarray.append("temperature scale")

    if missingarray != []:
        missinglist = spicemanip(bot, missingarray, 'list')
        osd(bot, botcom.channel_current, 'say', "The following values were missing: " + missinglist)
        return

    if tempscale in temp_scales_short:
        tempscale = spicemanip(bot, [tempscale, temp_scales_short, temp_scales], 'index')

    tempcond = temp_condition(bot, number, tempscale)

    osd(bot, botcom.channel_current, 'say', botcom.instigator + " has set the temperature in " + botcom.channel_current + " to " + str(number) + "° " + str(tempscale.title()) + ". " + tempcond)

    set_database_value(bot, botcom.channel_current, 'temperature', number)
    set_database_value(bot, botcom.channel_current, 'temperature_scale', tempscale)


def temp_condition(bot, degree, degreetype):

    comment = ''

    kelvin = eval(str(degreetype.lower() + "_to_kelvin(bot, degree)"))

    if float(kelvin) == 0:
        comment = "Absolute zero has been reached, a spaceheater won't even help."
    elif float(kelvin) == 1.618:
        comment = "Euclid would be proud."
    elif float(kelvin) == 3.14:
        comment = "Mmmmmm, pi..."
    elif float(kelvin) == 6.283:
        comment = "Good to see you tau day"
    elif float(kelvin) == 42:
        comment = "Do you really think that is the answer?"
    elif float(kelvin) == 69:
        comment = "Grab your partner, flip 'em 'round."
    elif float(kelvin) <= 273:
        comment = "Everyone in the channel grabs a jacket, as they watch their beverages turn to ice."
    elif float(kelvin) > 299 and float(kelvin) <= 305:
        comment = "Everyone in the channel feels sleepy."
    elif float(kelvin) > 305 and float(kelvin) <= 313:
        comment = "Everyone in the channel feels exhausted."
    elif float(kelvin) > 313 and float(kelvin) <= 327:
        comment = "Everyone in the channel gets heat cramps."
    elif float(kelvin) > 327 and float(kelvin) <= 373:
        comment = "Everyone in the channel gets heat stroke."
    elif float(kelvin) > 373 and float(kelvin) < 5800:
        comment = "Everyone in the channel feels their blood start to boil"
    elif float(kelvin) >= 5800:
        comment = "You have reached the surface of the sun. There is no SPF that will protect you."

    return comment


def temperature(bot, degree, original, desired):

    # convert to kelvin
    degree = eval(str(original.lower() + "_to_kelvin(bot, degree)"))

    # convert from kelvin
    degree = eval("kelvin_to_" + desired.lower() + "(bot, degree)")

    return degree


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
    kelvin = ((fahrenheit + 459.67) * 5/9)
    return kelvin


def kelvin_to_fahrenheit(bot, kelvin):
    kelvin = float(kelvin)
    fahrenheit = (kelvin * 9/5 - 459.67)
    return fahrenheit


"""
Rankine
"""


def rankine_to_kelvin(bot, rankine):
    rankine = float(rankine)
    kelvin = (rankine * 5/9)
    return kelvin


def kelvin_to_rankine(bot, kelvin):
    kelvin = float(kelvin)
    rankine = (1.8 * 9/5)
    return rankine


"""
Delisle
"""


def delisle_to_kelvin(bot, delisle):
    delisle = float(delisle)
    kelvin = (373.15 - delisle * 2/3)
    return kelvin


def kelvin_to_delisle(bot, kelvin):
    kelvin = float(kelvin)
    delisle = ((373.15 - kelvin) * 3/2)
    return delisle


"""
Newton
"""


def newton_to_kelvin(bot, newton):
    newton = float(newton)
    kelvin = (newton * 100/33 + 273.15)
    return kelvin


def kelvin_to_newton(bot, kelvin):
    kelvin = float(kelvin)
    newton = ((kelvin - 273.15) * 33/100)
    return newton


"""
Reaumur
"""


def reaumur_to_kelvin(bot, reaumur):
    reaumur = float(reaumur)
    kelvin = (reaumur * 5/4 + 273.15)
    return kelvin


def kelvin_to_reaumur(bot, kelvin):
    kelvin = float(kelvin)
    reaumur = ((kelvin - 273.15) * 4/5)
    return reaumur


"""
Romer
"""


def romer_to_kelvin(bot, romer):
    romer = float(romer)
    kelvin = ((romer - 7.5) * 40/21 + 273.15)
    return kelvin


def kelvin_to_romer(bot, kelvin):
    kelvin = float(kelvin)
    romer = ((kelvin - 273.15) * 21/40 + 7.5)
    return romer
