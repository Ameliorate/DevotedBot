import textwrap

from devbot.exception import ChatMessageTooLongError


def say(message, protocol):
    if len(message) >= 100:
        raise ChatMessageTooLongError
    protocol.send_packet("chat_message", protocol.buff_type.pack_string(message))


def say_wrap(prefix, message, protocol):
    max_len = 100 - len(prefix)
    wrap = textwrap.wrap(message, max_len)
    for msg in wrap:
        say(prefix + msg, protocol)