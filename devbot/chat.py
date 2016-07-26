import textwrap
import queue

from devbot.exception import ChatMessageTooLongError

from typing import Callable

_MESSAGE_QUEUE = queue.Queue()
_CHAT_HOOKS = {}


class Chat:
    def say(self, message):
        raise NotImplementedError('Chat.say is a abstract method')


class GroupChat(Chat):
    def __init__(self, group: str):
        self.group = group

    def say(self, message):
        wrap = textwrap.wrap(message, 99 - len('/g {} '.format(self.group)))
        for msg in wrap:
            _MESSAGE_QUEUE.put('/g {} {}'.format(self.group, msg))


class PrivateMessage(Chat):
    def __init__(self, person):
        self.person = person

    def say(self, message):
        wrap = textwrap.wrap(message, 99 - len('/m {} '.format(self.person)))
        for msg in wrap:
            _MESSAGE_QUEUE.put('/m {} {}'.format(self.person, msg))


class LocalChat(Chat):
    def say(self, message):
        _MESSAGE_QUEUE.put('/e')
        wrap = textwrap.wrap(message, 99)
        for msg in wrap:
            _MESSAGE_QUEUE.put(msg)


def process_chat(protocol):
    try:
        message = _MESSAGE_QUEUE.get_nowait()
        protocol.send_packet("chat_message", protocol.buff_type.pack_string(message))
    except queue.Empty:
        pass


def command(message):
    if len(message) >= 100:
        raise ChatMessageTooLongError
    _MESSAGE_QUEUE.put(message)


def command_wrap(prefix, message):
    max_len = 99 - len(prefix)
    wrap = textwrap.wrap(message, max_len)
    for msg in wrap:
        command(prefix + msg)


def private_message(person: str, message: str):
    command_wrap('/m {} '.format(person), message)


def group_message(group: str, message: str):
    command_wrap('/g {} '.format(group), message)


class _ChatHook:
    def __init__(self, regex, hook):
        self.regex = regex
        self.hook = hook

    def remove(self):
        _CHAT_HOOKS[self.regex].discard(self.hook)


def chat_hook(regex: str, hook: Callable[[str], bool]) -> _ChatHook:
    """
    Add a hook that'll be called every time the line of chat matches the given regex.
    :param regex: The regex the chat is matched against.
    :param hook: The function to be called. It is called with the chat message as it's only argument. If true is returned,
                 no other hooks are ran.
    """
    if regex in _CHAT_HOOKS:
        _CHAT_HOOKS[regex].add(hook)
        return _ChatHook(regex, hook)
    _CHAT_HOOKS[regex] = {hook}
    return _ChatHook(regex, 0)
