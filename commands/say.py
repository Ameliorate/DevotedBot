from devbot.chat import Chat, group_message, del_chat_hook, chat_hook
from devbot import DevCommand
from devbot.argparse import BooleanFlag, ContentFlag, parse_flags
from devbot.parse import *

import re
import time

WIKI = 'https://github.com/Ameliorate/DevotedBot/wiki/say'


class MainCommand(DevCommand):
    def main(self, args: [str], stdout: Chat, name: str):
        flags, rest_args = parse_flags(args[1:], {'interactive': BooleanFlag('i', 'interactive'),
                                                  'sign': BooleanFlag('s', 'sign'),
                                                  'channel': ContentFlag('c', 'channel'),
                                                  'name': ContentFlag('n', 'name')})
        if flags['channel'] is None:
            flags['channel'] = 'GlobalChat'
        if flags['name'] is not None:
            flags['sign'] = True
        if flags['name'] is None:
            flags['name'] = name
        if flags['interactive']:
            regex = r'From {}: *.'.format(name)

            def hook(msg: str) -> bool:
                pm = p.parse(msg, PrivateMessage)
                if pm.name == name:
                    if re.match(r'exit|quit|e|q', pm.message, re.IGNORECASE):
                        del_chat_hook(regex)
                        stdout.say('Exited interactive say')
                    elif flags['sign']:
                        group_message(flags['channel'], "``{}'' -{}".format(pm.message, flags['name']))
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
            group_message(flags['channel'], "``{}'' -{}".format(to_say, flags['name']))
        else:
            group_message(flags['channel'], "``{}''".format(to_say))

        def err_hook(msg: str) -> bool:
            stdout.say('There is no group with the name {}'.format(flags['channel']))
            return False

        chat_hook(r'There is no group with that name', err_hook)
        time.sleep(5)
        del_chat_hook(r'There is no group with that name')
