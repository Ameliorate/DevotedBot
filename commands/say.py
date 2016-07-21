from devbot.chat import Chat
from devbot import DevCommand


class MainCommand(DevCommand):
    def main(self, args: [str], stdout: Chat, cmdout: Chat):
        to_say = ''
        for i, word in enumerate(args):
            if i != 0:
                to_say = to_say + word + ' '
        to_say = to_say.strip()
        cmdout.say("/g GlobalChat ``{}''".format(to_say))
