class MessageTracker:
    def get_unread_messages(self):
        """Returns a list of unread messages from all chats (self.chat_list_attr).
        """
        unread_messages = []
        for chat in getattr(self.skype, self.chat_list_attr):
            try:
                self.last_timestamps[chat.Name]
            except KeyError:    # Unknown chat timestamp
                self._new_timestamp(chat)
                continue
            for message in list(getattr(chat, self.message_list_attr))[::-1]:
                if message.Timestamp <= self.last_timestamps[chat.Name]:
                    break
                else:
                    unread_messages.append(message)
            self._new_timestamp(chat)
        return unread_messages

    def _new_timestamp(self, chat):
        """Internal method.
        """
        if getattr(chat, self.message_list_attr):
            self.last_timestamps[chat.Name] = getattr(chat, self.message_list_attr)[-1].Timestamp
        else:   # No messages in chat
            self.last_timestamps[chat.Name] = 0

    def __init__(self, skype, chat_list_attr, message_list_attr):
        """It's probably best to construct a MessageTracker object in your
        initialize(skype) function. Example (recommended) use:
            mt = pluginapi.MessageTracker(skype, "RecentChats", "RecentMessages")
            um = mt.get_unread_messages()
        Parameters:
            skype               (Skype) the Skype object
            chat_list_attr      (string) which skype attribute to access chats through (e.g. "RecentChats")
            message_list_attr   (string) which chat attribute to access messages through (e.g. "RecentMessages")
        """
        self.skype = skype
        self.chat_list_attr = chat_list_attr
        self.message_list_attr = message_list_attr

        self.last_timestamps = {}
        for chat in getattr(self.skype, self.chat_list_attr):
            self._new_timestamp(chat)
