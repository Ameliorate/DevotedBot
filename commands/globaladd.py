from devbot import chat


def call(message: str, name, protocol, cfg, commands):
    if ' ' in message:
        chat.say('/msg {} Sorry, that was not a valid player name: It contains spaces.'.format(name))
        return
    chat.say_wrap('/msg {}',
                  'You have been added to global chat. Use /g GlobalChat to speak in the group, and /e to exit.'.format(
                      message))
    chat.say('/nlip GlobalChat {}'.format(message))
