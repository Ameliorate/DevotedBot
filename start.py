import configparser
import os.path
import sys
import re

from quarry.net.client import ClientProtocol, ClientFactory
from quarry.mojang.profile import Profile

from pypeg2 import parse

from devbot import chat, parse_pm, run_command
from devbot.parse import PrivateMessage

CONFIG_FILE = 'config.cfg'
CONFIG = configparser.ConfigParser()
COMMAND_FILE = 'commands.cfg'
COMMANDS = configparser.ConfigParser()
COMMANDS.read(COMMAND_FILE)


class DevotedBotClientProtocol(ClientProtocol):
    def packet_keep_alive(self, buff):
        identifier = buff.unpack_varint(signed=True)
        self.send_packet('keep_alive', self.buff_type.pack_varint(identifier, signed=True))
        global COMMANDS
        COMMANDS = configparser.ConfigParser()
        COMMANDS.read(COMMAND_FILE)
        chat.process_chat(self)
        # Packing Client Settings packet
        buffer = self.buff_type.pack_string('en_GB') + \
                 self.buff_type.pack('b', 1) + \
                 self.buff_type.pack_varint(0, signed=True) + \
                 self.buff_type.pack('?', True) + \
                 self.buff_type.pack('B', 0x01 | 0x02 | 0x04 | 0x08 | 0x10 | 0x20 | 0x40) + \
                 self.buff_type.pack_varint(1)
        self.send_packet('client_settings', buffer)

    def packet_update_health(self, buff):
        health = buff.unpack('f')
        food = buff.unpack_varint()
        saturation = buff.unpack('f')

        if health <= 0:
            self.send_packet('client_status', self.buff_type.pack_varint(0))
            chat.GroupChat('GlobalChat').say('Please do not kill DevotedBot.')
            print('Died, respawning...')

    def packet_disconnect(self, buff):
        message = buff.unpack_chat()
        print('Disconnected for reason:', message)
        factory.stop()

    def packet_chat_message(self, buff):
        chat = buff.unpack_chat()
        position = buff.unpack("b")
        if position == 0:
            print(':: ' + chat)
        elif position == 1:
            result = handle_chat(chat, self)
            if not result:
                print(':=: ' + chat)
        elif position == 2:
            print(':_: ' + chat)
        else:
            self.logger.warning('Unhandled chat position: ' + position + ' skipping.')
            return


class DevotedBotClientFactory(ClientFactory):
    protocol = DevotedBotClientProtocol


factory = DevotedBotClientFactory()


def generate_config_file(name, config):
    config['auth'] = {'username': 'USERNAME',
                      'password': 'PASSWORD',
                      'auth': 'true'}
    config['server'] = {'ip': 'play.devotedmc.com',
                        'port': '25565'}
    with open(name, 'w') as configfile:
        configfile.write('# Config automatically generated. Delete this file to reset.\n\n')
        config.write(configfile)
    print('Config file generated. Edit the username and password fields to set up an account.')
    sys.exit()


def main():
    if os.path.isfile(CONFIG_FILE):
        CONFIG.read(CONFIG_FILE)
    else:
        generate_config_file(CONFIG_FILE, CONFIG)

    profile = Profile()
    if not CONFIG['auth'].getboolean('auth'):
        profile.login_offline(CONFIG['auth']['username'])
        factory.profile = profile
    else:
        def login_ok(data):
            factory.connect(CONFIG['server']['ip'], int(CONFIG['server']['port']))

        def login_failed(err):
            print('login failed:', err.value)
            factory.stop()
            sys.exit(1)

        factory.profile = profile
        deferred = profile.login(CONFIG['auth']['username'], CONFIG['auth']['password'])
        deferred.addCallbacks(login_ok, login_failed)
        factory.run()


def handle_chat(message, protocol):
    """
    :return: Weather or not the chat message was a valid command
    """
    message = message.strip()
    any_chat_hook_ran = False
    # noinspection PyProtectedMember
    for hook in chat._CHAT_HOOKS.keys():
        if re.match(hook, message):
            # noinspection PyProtectedMember
            for to_run in chat._CHAT_HOOKS[hook]:
                any_chat_hook_ran = True
                result = to_run(message)
                if result:
                    return True
    if any_chat_hook_ran:
        return True
    if message == 'You are already chatting in that group.':
        return True
    elif re.match(r'From Amelorate: ssh', message):
        chat.command(message[20:])
        return True

    match = re.match(r'From .*:\s', message)
    if match:
        try:
            parsed_full, pm = parse_pm(message)
        except SyntaxError as e:
            pm = parse(message, PrivateMessage)
            chat.PrivateMessage(pm.name).say(
                'There was a syntax error in your command: {} (character {})'.format(str(e), e.offset))
            return True
        print(':c: {}: {}'.format(pm.name, pm.message))
        try:
            run_command(parsed_full, chat.PrivateMessage(pm.name), COMMANDS, pm.name)
        except NotImplementedError as e:
            chat.PrivateMessage(pm.name).say('Not Implemented: {}'.format(str(e)))
        return True
    else:
        return False


if __name__ == '__main__':
    main()
