import os
import re

import pluginapi


NAME = "HelloWorld"

_TABLE_FILE = os.path.dirname(__file__) + "/table.txt"

_message_tracker = None
_table = {}


def initialize(skype):
    global _message_tracker
    _message_tracker = pluginapi.MessageTracker(skype, "RecentChats", "RecentMessages")
    load_table()


def execute(skype):
    global _message_tracker, _table
    unread_messages = _message_tracker.get_unread_messages()
    for msg in unread_messages:
        body = msg.Body.encode('ascii', 'replace')

        cmd = re.match("^!(\w+)$", body)
        if cmd:
            cmd = cmd.group(1).lower()
            value = _table.get(cmd, None)
            if value is not None:
                msg.Chat.SendMessage(cmd + ": " + str(_table[cmd]))

        cmd = re.match("^(\w+)\+\+$", body)
        if cmd:
            cmd = cmd.group(1).lower()
            value = _table.get(cmd, None)
            if value is not None and type(value) == int:
                _table[cmd] += 1
            elif not value:
                _table[cmd] = 1
            msg.Chat.SendMessage(cmd + ": " + str(_table[cmd]))

        cmd = re.match("^(\w+)\-\-$", body)
        if cmd:
            cmd = cmd.group(1).lower()
            value = _table.get(cmd, None)
            if value is not None and type(value) == int:
                _table[cmd] -= 1
            elif not value:
                _table[cmd] = 1
            msg.Chat.SendMessage(cmd + ": " + str(_table[cmd]))


def kill(skype):
    save_table()


def load_table():
    global _table
    with open(_TABLE_FILE, 'r') as table_file:
        for line in table_file.readlines():
            key, value = line.split()[:2]
            value = int(value)
            _table[key] = value


def save_table():
    global _table
    with open(_TABLE_FILE, 'w') as table_file:
        for key, value in _table.items():
            table_file.write("{0} {1}\n".format(key, value))


if __name__ == '__main__':
    pass
