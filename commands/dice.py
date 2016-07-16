import dice

from devbot import chat, time_limit, TimeoutException
from devbot.exception import ChatMessageTooLongError


def call(message, name, protocol, cfg, commands):
    with time_limit(3):
        # noinspection PyBroadException
        try:
            result = dice.roll(message)
            chat.say('/msg {} {}'.format(name, str(result)))
        except ChatMessageTooLongError:
            chat.say('/msg {} Sorry, that dicestring gave too many numbers.'.format(name))
        except TimeoutException:
            chat.say('/msg {} Sorry, that dice roll took too long to execute.'.format(name))
        except Exception as e:
            chat.say('/msg {} Sorry, there was a error in that dice roll:'.format(name))
            if str(e) != '':
                chat.say_wrap('/msg {} '.format(name), str(e))
