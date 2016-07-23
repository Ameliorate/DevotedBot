import signal
import pypeg2

from contextlib import contextmanager
from devbot.chat import Chat
from devbot.parse import *
from configparser import ConfigParser
from threading import Thread


class DevCommand:
    def __init__(self, args: [str], command_cfg: ConfigParser, stdout: Chat, name: str):
        self.command_cfg = command_cfg
        self.main(args, stdout, name)

    def main(self, args: [str], stdout: Chat, name: str):
        raise NotImplementedError('Command is an abstract base class')


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
    message_parsed = pypeg2.parse(message_parsed, PrivateMessage)
    print('{}: {}'.format(message_parsed.name, message_parsed.message))
    cmd = pypeg2.parse(message_parsed.message, TerminalCommand)
    return cmd, message_parsed


def run_command(cmd: TerminalCommand, stdout: Chat, command_cfg: ConfigParser, name: str):
    if type(cmd.content) == Command:
        arglist = []
        if cmd.content.args is not None:
            for arg in cmd.content.args:
                if type(arg.content) == AbsoluteArgument:
                    arglist.append(arg.content.text.text)
                elif type(arg.content) == RedirectedArgument:
                    raise NotImplementedError('redirected arguments are not yet implemented')
        arglist = [cmd.content.command] + arglist
        try:
            commandmod = __import__('commands.' + cmd.content.command, fromlist=['*'])
        except ImportError:
            stdout.say('There was no command by the name `{}`'.format(cmd.content.command))
            return
        Thread(target=commandmod.MainCommand, name=cmd.content.command,
               args=(arglist, command_cfg, stdout, name)).start()
    # Room for things like pipes that are implemented in TerminalCommand.
    return False
