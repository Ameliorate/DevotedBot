import dice

from devbot import chat


def call(message, name, protocol, cfg, commands):
    # noinspection PyBroadException
    try:
        result = dice.roll(message)
        chat.say('/r ' + str(result), protocol)
    except Exception as e:
        chat.say('/r Sorry, there was a error in that dice roll:', protocol)
        if str(e) != '':
            chat.say('/r ' + str(e), protocol)
