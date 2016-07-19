import signal

from contextlib import contextmanager
from devbot.parse import *
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


def run_command(cmd: TerminalCommand) -> bool:
    if cmd.content.__class__ == Command:
        arglist = []
        if cmd.content.args is not None:
            for arg in cmd.content.args:
                if arg.content.__class__ == AbsoluteArgument:
                    arglist.append(arg.content.text.text)
                elif arg.content.__class__ == RedirectedArgument:
                    raise NotImplementedError('redirected arguments are not yet implemented')
        print(arglist)
        raise NotImplementedError('running commands is not yet implemented')
    # Room for things like pipes that are implemented in TerminalCommand.
    return False
