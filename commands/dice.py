import dice

from devbot import chat
from devbot.exception import ChatMessageTooLongError


def call(message, name, protocol, cfg, commands):
    # noinspection PyBroadException
    try:
        result = dice.roll(message)
        chat.say('/msg ' + name + ' ' + str(result))
    except ChatMessageTooLongError:
        chat.say('/msg ' + name + ' Sorry, that dicestring gave too many numbers.')
    except Exception as e:
        chat.say('/msg ' + name + ' Sorry, there was a error in that dice roll:')
        if str(e) != '':
            chat.say_wrap('/msg ' + name + ' ', str(e))
