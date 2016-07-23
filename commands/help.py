from devbot.chat import Chat
from devbot import DevCommand


class MainCommand(DevCommand):
    def main(self, args: [str], stdout: Chat, name: str):
        try:
            commandmod = __import__('commands.' + args[1], fromlist=['*'])
            stdout.say(commandmod.WIKI)
        except AttributeError:
            stdout.say('Sorry, the command `{}` does not have a wiki page.'.format(args[1]))
        except ImportError:
            stdout.say('Sorry, there was not a command by the name of `{}` to get help on.'.format(args[1]))
