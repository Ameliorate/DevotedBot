import requests

from devbot.chat import Chat, group_message
from devbot import DevCommand


class MainCommand(DevCommand):
    def main(self, args: [str], stdout: Chat, name: str):
        requ = requests.get('https://catfacts-api.appspot.com/api/facts')
        json = requ.json()
        if json['success'] == 'true':
            fact = json['facts'][0]
            if len(args) != 1:
                group_message(args[1], fact)
            else:
                stdout.say(fact)
        else:
            stdout.say('Error getting cat fact.')
            group_message('GlobalChat', 'Someone reddit mail /u/Amelorate this:')
            group_message('GlobalChat', requ.text)
