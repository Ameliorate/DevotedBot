from devbot import chat


def call(message, name, protocol, cfg, commands):
    if message == '':
        chat.say('/r ' + commands['help']['alias'].format('alias'))
        return

    aliases = ''
    for tupl in commands['regex'].items():
        if tupl[1] == message:
            aliases = aliases + tupl[0] + ', '
    if aliases == '':
        chat.say('/msg {} Sorry, there is no command by that name.'.format(name))
    else:
        chat.say('/msg {} {}'.format(name, aliases))

