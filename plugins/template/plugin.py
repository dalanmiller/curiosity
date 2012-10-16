import pluginapi


NAME = "TemplatePlugin"

_message_tracker = None


def initialize(skype):
    global _message_tracker
    _message_tracker = pluginapi.MessageTracker(skype, "RecentChats", "RecentMessages")


def execute(skype):
    global _message_tracker, _table
    unread_messages = _message_tracker.get_unread_messages()
    for msg in unread_messages:
        body = msg.Body.encode('ascii', 'replace')
        pass


def kill(skype):
    pass

if __name__ == '__main__':
    pass
