from devbot.chat import Chat
from devbot import DevCommand
from os import listdir
from os.path import isfile, join


class MainCommand(DevCommand):
    def main(self, args: [str], stdout: Chat, name: str):
        if len(args) == 1:
            commandfiles = [f for f in listdir('commands/') if isfile(join('commands/', f))]
            cmdlist = []
            for cmd in commandfiles:
                # Turn filenames into command names and remove __init__.py.
                if cmd == '__init__.py':
                    continue
                split = cmd.split('.')
                split = split[:-1]  # Remove file extension.
                name = '.'.join(split)
                cmdlist.append(name)
            message = ', '.join(cmdlist)
            stdout.say('Use `help [command]` to get help on a specific command.')
            stdout.say(message)
            return
        try:
            commandmod = __import__('commands.' + args[1], fromlist=['*'])
            stdout.say(commandmod.WIKI)
        except AttributeError:
            stdout.say('Sorry, the command `{}` does not have a wiki page.'.format(args[1]))
        except ImportError:
            stdout.say('Sorry, there was not a command by the name of `{}` to get help on.'.format(args[1]))
