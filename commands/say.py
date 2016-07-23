from devbot.chat import Chat, group_message
from devbot import DevCommand
from devbot.argparse import BooleanFlag, ContentFlag, parse_flags


class MainCommand(DevCommand):
    def main(self, args: [str], stdout: Chat, name: str):
        flags, rest_args = parse_flags(args[1:], {'interactive': BooleanFlag('i', 'interactive'),
                                              'sign': BooleanFlag('s', 'sign'),
                                              'channel': ContentFlag('c', 'channel')})
        if flags['channel'] is None:
            flags['channel'] = 'GlobalChat'
        if flags['interactive']:
            raise NotImplementedError('Interactivity is not implemented.')
        to_say = ''
        for i, word in enumerate(rest_args):
            to_say = to_say + word + ' '
        to_say = to_say.strip()
        if flags['sign']:
            group_message(flags['channel'], "``{}'' -{}".format(to_say, name))
        else:
            group_message(flags['channel'], "``{}''".format(to_say))

