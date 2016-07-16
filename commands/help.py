import re

from devbot import chat


def call(message, name, protocol, cfg, commands):
    if message == '':
        commandlist = set()
        for tupl in commands['regex'].items():
            commandlist.add(tupl[1])

        listmsg = ''
        for cmd in commandlist:
            listmsg = listmsg + cmd + ', '
        chat.say('/msg {} Use `help [command]` to get help on a specific command.'.format(name))
        chat.say('/msg {} {}'.format(name, listmsg))
        return

    for regex in commands['regex'].keys():
        if re.match(regex, message):
            chat.say_wrap('/msg {} '.format(name), commands['help'][commands['regex'][regex]].format(message))
            return
    chat.say('/msg {} help: Sorry, there was not a command by that name to get help on.'.format(name))
