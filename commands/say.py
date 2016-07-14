from devbot import chat


def call(message, name, protocol):
    chat.say('/g GlobalChat', protocol)
    chat.say('"' + message[4:] + '"', protocol)
