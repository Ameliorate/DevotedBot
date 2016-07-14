import requests
import textwrap

from devbot import chat


def call(message, name, protocol, cfg, commands):
    requ = requests.get('https://catfacts-api.appspot.com/api/facts')
    json = requ.json()
    if json['success'] == 'true':
        fact = json['facts'][0]
        wrap = textwrap.wrap(fact, 90)
        for text in wrap:
            chat.say('/r ' + text, protocol)
    else:
        chat.say('/r Error getting cat fact.', protocol)
        chat.say('/g GlobalChat', protocol)
        chat.say('Someone mail /u/Amelorate this:', protocol)
        wrap = textwrap.wrap(requ.text, width=100)
        for text in wrap:
            chat.say(text, protocol)
