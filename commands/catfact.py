import requests
import textwrap

from devbot import chat


def call(message, name, protocol, cfg, commands):
    requ = requests.get('https://catfacts-api.appspot.com/api/facts')
    json = requ.json()
    if json['success'] == 'true':
        fact = json['facts'][0]
        prefix = '/msg ' + name + ' '
        chat.say('/g GlobalChat')
        if message.lower() != '' and commands['catfacts'].getboolean('allowglobal'):
            prefix = ''
            chat.say('/g ' + message)
        chat.say_wrap(prefix, fact)
    else:
        chat.say('/msg ' + name + ' Error getting cat fact.')
        chat.say('/g GlobalChat')
        chat.say('Someone reddit mail /u/Amelorate this:')
        chat.say_wrap(requ.text)
