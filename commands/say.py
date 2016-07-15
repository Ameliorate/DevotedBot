from devbot import chat


def call(message, name, protocol, cfg, commands):
    chat.say('/g GlobalChat')
    chat.say('"' + message + '"')
