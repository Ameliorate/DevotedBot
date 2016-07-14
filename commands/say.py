from devbot import chat


def call(message, name, protocol, cfg, commands):
    chat.say('/g GlobalChat', protocol)
    chat.say('"' + message + '"', protocol)
