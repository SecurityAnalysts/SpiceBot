# Modules
This folder contains all the modules the bot uses.

Modules located in the IT, Bot, and Tools folders do not pass through the prerun check.

All other modules pass through a prerun check found in BotShared.py.
This is to verify that the command is enabled in that channel, and that the user that triggered it has the bot enabled.

Any modules located in the development folder have no effect on the "master" channels (#spiceworks and ##spicebot).<br>
These are only loaded by Spicebotdev in ##spicebottest, not by Spicebot itself. Think of this like the 'beta' release.

Any fully functional modules are located in the relevant category folder.<br>
For example, duels and casino are found in the Games folder, while the "Nelson" command is in the Memes folder.
