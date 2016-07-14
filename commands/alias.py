from devbot import chat


def call(message, name, protocol, cfg, commands):
    if message == '':
        chat.say('/r ' + commands['help']['alias'].format('alias'), protocol)
        return

    aliases = ''
    for tupl in commands['regex'].items():
        if tupl[1] == message:
            aliases = aliases + tupl[0] + ', '
    if aliases == '':
        chat.say('/r Sorry, there is no command by that name.', protocol)
    else:
        chat.say('/r ' + aliases, protocol)

