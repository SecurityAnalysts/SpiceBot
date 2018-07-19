#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# pylama:ignore=W,E201,E202,E203,E221,E222,w292

"""
OSD
"""


# How Many characters to put on the display
osd_limit = 420

"""
Commands
"""


# Valid Command Types
rpg_valid_command_types = ['admin']

# Admin Commands
rpg_commands_valid_admin = ['admin']

"""
Map System
"""


rpg_valid_directions = ['north','south','east','west']


"""
Error messages System
"""


rpg_error_list = ['admin','commands']

rpg_error_admin = [
                    "Only bot admins may utilize the -a switch."
]

rpg_error_commands = [
                    "You may only run a command once at a time using the multicom feature."
]
