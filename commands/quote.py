from random import choice

from devbot import chat

QUOTES = (
    ("PrideVGreed is the meanest meme.", "PrideVGreed"),
    ("ERROR ERROR ERROR", "PrideVGreed"),
    ("Fuck Wergo", "doughy-goods"),
    ("Yeah Gar", "Garking"),
    ("What do you mean? I never hated black people. Ooooh. I see what you mean. I hate niggers with a passion. REEEEEEEEEEEEEEEEEEEEEEEEEE.", "OurTrueLeader"),
    ('this is like saying" OTL is a cool guy, aside from the blatant racism and autism"', "bayernanhaenger"),
    ("My favourite colours are blue and light blue...", "bigbrainiac10"),
    ("If I pearl ron_paul I'm naming the post ron_pearl claimed post Garry Oak", "Soerxpso"),
    ("oh the door is gone", "kaiman")
)


def call(message, name, protocol, cfg, commands):
    quote = choice(QUOTES)
    full = '"{}" -{}'.format(quote[0], quote[1])
    chat.say_wrap('/msg {} '.format(name), full)
