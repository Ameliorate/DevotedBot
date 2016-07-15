import textwrap
import queue

from devbot.exception import ChatMessageTooLongError

CHAT_QUEUE = queue.Queue()


def say(message):
    if len(message) >= 100:
        raise ChatMessageTooLongError
    CHAT_QUEUE.put(message)


def say_wrap(prefix, message):
    max_len = 99 - len(prefix)
    wrap = textwrap.wrap(message, max_len)
    for msg in wrap:
        say(prefix + msg)


def process_chat(protocol):
    try:
        message = CHAT_QUEUE.get_nowait()
        protocol.send_packet("chat_message", protocol.buff_type.pack_string(message))
    except queue.Empty:
        pass
