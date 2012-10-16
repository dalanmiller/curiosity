import os
import importlib
import time
import traceback

import Skype4Py

import settings


def discover_plugins():
    plugins = []
    folders = list(os.walk(settings.PLUGINS_FOLDER))[1:]
    for folder in folders:
        try:
            module_name = folder[0] + "." + settings.PLUGIN_MODULE_NAME
            module_name = module_name.replace("\\", ".")
            plugin = importlib.import_module(module_name)
            plugins.append(plugin)
            print "{0} @ {1}".format(plugin.NAME, module_name)
        except ImportError as e:
            print "{0}: {1}".format(e.message, module_name)
    return plugins


def init_plugins(plugins, skype):
    for plugin in plugins:
        try:
            plugin.initialize(skype)
        except AttributeError as e:
            print "{0}: {1}".format(plugin.NAME, e.message)


def exec_plugins(plugins, skype):
    for plugin in plugins:
        try:
            plugin.execute(skype)
        except Exception as e:
            print "{0}: {1}".format(plugin.NAME, e)
            print traceback.format_exc()


def kill_plugins(plugins, skype):
    for plugin in plugins:
        try:
            plugin.kill(skype)
        except AttributeError as e:
            print "{0}: {1}".format(plugin.NAME, e.message)


def main():
    try:
        print "Connecting to Skype..."
        skype = Skype4Py.Skype()
        print "Attaching..."
        skype.Attach()
        print "Connected!"
    except Exception as e:
        print e
        exit()
    print

    user = skype.CurrentUser
    print "Connected with user:"
    print "{0:<10} {1}".format("Handle", user.Handle)
    print "{0:<10} {1}".format("Full name", user.FullName)
    print "{0:<10} {1}".format("Status", user.OnlineStatus)
    print

    print "Discovering plugins..."
    plugins = discover_plugins()
    print "{0} plugins discovered.\n".format(len(plugins))

    print "Initializing plugins..."
    init_plugins(plugins, skype)
    print "Plugins initialized.\n"

    print "Begin monitoring..."
    print "Press Ctrl+C to quit.\n"

    try:
        while 1:
            start_time = time.clock()
            exec_plugins(plugins, skype)
            end_time = time.clock()
            time_taken = end_time - start_time
            if time_taken < settings.POLL_INTERVAL:
                time.sleep(settings.POLL_INTERVAL - time_taken)
            # print "Execution time: {0} s".format(time_taken)
    except KeyboardInterrupt as e:
        print "Execution interrupted!"
        print

    print "Killing plugins..."
    kill_plugins(plugins, skype)
    print "All plugins dead."

if __name__ == '__main__':
    main()
