from devbot.chat import Chat, command
from devbot import DevCommand


class MainCommand(DevCommand):
    def main(self, args: [str], stdout: Chat):
        to_say = ''
        for i, word in enumerate(args):
            if i != 0:
                to_say = to_say + word + ' '
        to_say = to_say.strip()
        command("/g GlobalChat ``{}''".format(to_say))
