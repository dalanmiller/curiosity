## Curiosity Skype bot
![Curiosity Skype bot](https://raw.github.com/gediminasz/curiosity/master/stuff/curiosity-avatar.jpg)

### General

Curiosity is a very simplistic Skype bot writted in Python using **Skype4Py** module. Although imperfect, it has a very easy tu use plugin system, so a working plugin can be created in a matter of minutes.

To run Curiosity, execute command `python curiosity.py`.

You can stop the bot by pressing `Ctrl + C`.

### Plugins

A plugin template can be found in `plugins/template` folder. There you can find `plugin.py` module which is imported by `curiosity.py`. A working plugin should have these functions implemented (or at least have them `pass`):

* `initialize(skype)` A function called once after the plugin is imported. This can be used to load a data file, for example.
* `execute(skype)` Called periodically in an infinite loop, invoking plugin's execution.
* `kill(skype)` Called once after the user presses `Ctrl + C`, forcing the bot to exit from an infinite loop. This can be used to close and save a data file, for example.

### pluginapi

A plugin can also import `pluginapi` module which is (or will be) a collection. For now it provides `MessageTracker` class which helps a plugin to discover its unread messages. You can find an example of `MessageTracker` usage in `plugins/template/plugin.py` example.