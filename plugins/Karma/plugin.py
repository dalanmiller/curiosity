import os
import re
import pluginapi


NAME = "Karma"

_message_tracker = None

_TABLE_FILE = os.path.dirname(__file__) + "/table.txt"
_table = {}


def _get_karma(value):
    karma = _table.get(value, None)
    if karma is not None:
        return value + ": " + str(karma)


def _inc_karma(value):
    karma = _table.get(value, None)
    if karma is not None and type(karma) == int:
        _table[value] += 1
    elif not karma:
        _table[value] = 1
    return value + ": " + str(_table[value])


def _dec_karma(value):
    karma = _table.get(value, None)
    if karma is not None and type(karma) == int:
        _table[value] -= 1
    elif not karma:
        _table[value] = -1
    return value + ": " + str(_table[value])


def _load_table():
    global _table
    with open(_TABLE_FILE, 'r') as table_file:
        for line in table_file.readlines():
            key, value = line.split()[:2]
            value = int(value)
            _table[key] = value


def _save_table():
    global _table
    with open(_TABLE_FILE, 'w') as table_file:
        for key, value in _table.items():
            table_file.write("{0} {1}\n".format(key, value))


def initialize(skype):
    global _message_tracker
    _message_tracker = pluginapi.MessageTracker(skype, "RecentChats", "RecentMessages")
    _load_table()


def execute(skype):
    global _message_tracker, _table
    unread_messages = _message_tracker.get_unread_messages()
    for msg in unread_messages:
        body = msg.Body.encode('ascii', 'replace')
        commands = {
            "^!(\w+)$": _get_karma,
            "^(\w+)\+\+$": _inc_karma,
            "^(\w+)\-\-$": _dec_karma,
        }
        for command, function in commands.items():
            match = re.match(command, body)
            if match:
                reply = function(match.group(1).lower())
                if reply:
                    msg.Chat.SendMessage(reply)


def kill(skype):
    _save_table()


if __name__ == '__main__':
    pass
