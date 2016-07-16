import dice

from devbot import chat, time_limit, TimeoutException
from devbot.exception import ChatMessageTooLongError


def call(message, name, protocol, cfg, commands):
    with time_limit(3):
        # noinspection PyBroadException
        try:
            result = dice.roll(message)
            chat.say('/msg ' + name + ' ' + str(result))
        except ChatMessageTooLongError:
            chat.say('/msg ' + name + ' Sorry, that dicestring gave too many numbers.')
        except TimeoutException:
            chat.say('/msg {} Sorry, that dice roll took too long to execute.'.format(name))
        except Exception as e:
            chat.say('/msg ' + name + ' Sorry, there was a error in that dice roll:')
            if str(e) != '':
                chat.say_wrap('/msg ' + name + ' ', str(e))
