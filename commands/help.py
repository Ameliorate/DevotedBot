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
        chat.say('/r Use `help [command]` to get help on a specific command.', protocol)
        chat.say('/r ' + listmsg, protocol)
        return

    for regex in commands['regex'].keys():
        if re.match(regex, message):
            chat.say('/r ' + commands['help'][commands['regex'][regex]].format(message), protocol)
            return
    chat.say('/r help: Sorry, there was not a command by that name to get help on.', protocol)
