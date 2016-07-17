from devbot import chat


def call(message: str, name, protocol, cfg, commands):
    if message is '':
        chat.say('/msg {} {}'.format(name, commands['help']['globaladd'].format('globaladd')))
        return
    if ' ' in message:
        chat.say('/msg {} Sorry, that was not a valid player name: It contains spaces.'.format(name))
        return
    chat.say('/msg {} Invited {} to GlobalChat'.format(name, message))
    chat.say(
        '/msg {} You have been invited to global chat. Use /g GlobalChat to enter, and /e to exit.'.format(
            message))
    chat.say('/nlip GlobalChat {}'.format(message))
