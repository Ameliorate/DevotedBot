from devbot.chat import Chat, group_message, del_chat_hook, chat_hook
from devbot import DevCommand
from devbot.argparse import BooleanFlag, ContentFlag, parse_flags
from devbot.parse import *

import re


class MainCommand(DevCommand):
    def main(self, args: [str], stdout: Chat, name: str):
        flags, rest_args = parse_flags(args[1:], {'interactive': BooleanFlag('i', 'interactive'),
                                              'sign': BooleanFlag('s', 'sign'),
                                              'channel': ContentFlag('c', 'channel')})
        if flags['channel'] is None:
            flags['channel'] = 'GlobalChat'
        if flags['interactive']:
            regex = r'From {}: *.'.format(name)

            def hook(msg: str):
                pm = p.parse(msg, PrivateMessage)
                if pm.name == name:
                    if re.match(r'exit|quit|e|q', pm.message, re.IGNORECASE):
                        del_chat_hook(regex)
                        stdout.say('Exited interactive say')
                    elif flags['sign']:
                        group_message(flags['channel'], "``{}'' -{}".format(pm.message, name))
                    else:
                        group_message(flags['channel'], "``{}''".format(pm.message))
                    return True
                else:
                    return False
            chat_hook(regex, hook)
            stdout.say('Entered interactive say. Use the command `e` to exit.')
            return
        to_say = ''
        for i, word in enumerate(rest_args):
            to_say = to_say + word + ' '
        to_say = to_say.strip()
        if flags['sign']:
            group_message(flags['channel'], "``{}'' -{}".format(to_say, name))
        else:
            group_message(flags['channel'], "``{}''".format(to_say))

