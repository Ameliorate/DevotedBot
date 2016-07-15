import dice

from devbot import chat
from devbot.exception import ChatMessageTooLongError


def call(message, name, protocol, cfg, commands):
    # noinspection PyBroadException
    try:
        result = dice.roll(message)
        chat.say('/r ' + str(result), protocol)
    except ChatMessageTooLongError:
        chat.say('/r Sorry, that dicestring gave too many numbers.', protocol)
    except Exception as e:
        chat.say('/r Sorry, there was a error in that dice roll:', protocol)
        if str(e) != '':
            chat.say_wrap('/r ', str(e), protocol)
