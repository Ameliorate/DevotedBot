from random import choice

from devbot import chat

ANSWERS = (
    "Definitely",
    "Yes",
    "Probably",
    "Mabye",
    "Probably Not",
    "No",
    "Definitely Not",
    "I don't know",
    "Ask Later",
    "I'm too tired",
)


def call(message, name, protocol, cfg, commands):
    chat.say('/msg {} {}'.format(name, choice(ANSWERS)))
