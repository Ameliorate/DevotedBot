import textwrap
import queue

from devbot.exception import ChatMessageTooLongError

CHAT_QUEUE = queue.Queue()


class _Command:
    def __init__(self, message: str):
        self.message = message


class _ChannelMessage:
    def __init__(self, channel: str, message: str):
        self.channel = channel
        self.message = message


class _LocalMessage:
    def __init__(self, message: str):
        self.message = message


class _PrivateMessage:
    def __init__(self, person: str, message: str):
        self.person = person
        self.message = message


class Chat:
    def say(self, message):
        raise NotImplementedError('Chat.say is a abstract method')


class Command(Chat):
    def say(self, message):
        if len(message) >= 100:
            raise ChatMessageTooLongError('Message too long')
        CHAT_QUEUE.put(_Command(message))


class GroupChat(Chat):
    def __init__(self, group: str):
        self.group = group

    def say(self, message):
        CHAT_QUEUE.put(_ChannelMessage(self.group, message))


class PrivateChat(Chat):
    def __init__(self, person):
        self.person = person

    def say(self, message):
        CHAT_QUEUE.put(_PrivateMessage(self.person, message))


class LocalChat(Chat):
    def say(self, message):
        CHAT_QUEUE.put(_LocalMessage(message))


def process_chat(protocol):
    try:
        message = CHAT_QUEUE.get_nowait()
        if message.__class__ == _LocalMessage:
            protocol.send_packet("chat_message", protocol.buff_type.pack_string('/e'))
            wrap = textwrap.wrap(message.message, 99)
            for msg in wrap:
                protocol.send_packet("chat_message", protocol.buff_type.pack_string(msg))
        elif message.__class__ == _Command:
            protocol.send_packet("chat_message", protocol.buff_type.pack_string(message.message))
        elif message.__class__ == _PrivateMessage:
            protocol.send_packet("chat_message", protocol.buff_type.pack_string('/e'))
            wrap = textwrap.wrap(message.message, 99 - len('/m {} '.format(message.person)))
            for msg in wrap:
                protocol.send_packet("chat_message",
                                     protocol.buff_type.pack_string('/m {} {}'.format(message.person, msg)))
        elif message.__class__ == _ChannelMessage:
            protocol.send_packet("chat_message", protocol.buff_type.pack_string('/e'))
            wrap = textwrap.wrap(message.message, 99 - len('/g {} '.format(message.name)))
            for msg in wrap:
                protocol.send_packet("chat_message",
                                     protocol.buff_type.pack_string('/g {} {}'.format(message.name, msg)))
    except queue.Empty:
        pass
