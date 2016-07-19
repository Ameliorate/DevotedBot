import signal

from contextlib import contextmanager
from devbot.parse import PrivateMessage, TerminalCommand
from pypeg2 import parse


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException('Timed out')
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def parse_pm(message_parsed: str) -> (TerminalCommand, PrivateMessage):
    message_parsed = parse(message_parsed, PrivateMessage)
    print('{}: {}'.format(message_parsed.name, message_parsed.message))
    cmd = parse(message_parsed.message, TerminalCommand)
    return cmd, message_parsed
