import configparser
import os.path
import sys
import re

from pydoc import locate

from quarry.net.client import ClientProtocol, ClientFactory
from quarry.mojang.profile import Profile

CONFIG_FILE = 'config.cfg'
COMMAND_FILE = 'commands.cfg'
COMMANDS = configparser.ConfigParser()
COMMANDS.read(COMMAND_FILE)

class DevotedBotClientProtocol(ClientProtocol):
    def packet_keep_alive(self, buff):
        identifier = buff.unpack_varint(signed=True)
        self.send_packet('keep_alive', self.buff_type.pack_varint(identifier, signed=True))

    def packet_update_health(self, buff):
        health = buff.unpack('f')
        food = buff.unpack_varint()
        saturation = buff.unpack('f')

        if health <= 0:
            self.send_packet('client_status', self.buff_type.pack_varint(0))
            print('Died, respawning...')

    def packet_disconnect(self, buff):
        message = buff.unpack_chat()
        print('Disconnected for reason: ', message)
        sys.exit(1)

    def packet_chat_message(self, buff):
        chat = buff.unpack_chat()
        position = buff.unpack("b")
        if position == 0:
            self.logger.info(':: ' + chat)
            result = handle_chat(chat, self)
        elif position == 1:
            self.logger.info(':=: ' + chat)
            handle_chat(chat, self)
        elif position == 2:
            self.logger.info(':_: ' + chat)
        else:
            self.logger.warning('Unhandled chat position: ' + position + ' skipping.')
            return


class DevotedBotClientFactory(ClientFactory):
    protocol = DevotedBotClientProtocol


class ChatMessageTooLongError(Exception):
    pass


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
    cfg = configparser.ConfigParser()
    if os.path.isfile(CONFIG_FILE):
        cfg.read(CONFIG_FILE)
    else:
        generate_config_file(CONFIG_FILE, cfg)

    profile = Profile()
    factory = DevotedBotClientFactory()
    if not cfg['auth'].getboolean('auth'):
        profile.login_offline(cfg['auth']['username'])
        factory.profile = profile
    else:
        def login_ok(data):
            factory.connect(cfg['server']['ip'], int(cfg['server']['port']))

        def login_failed(err):
            print('login failed:', err.value)
            factory.stop()
            sys.exit(1)

        factory.profile = profile
        deferred = profile.login(cfg['auth']['username'], cfg['auth']['password'])
        deferred.addCallbacks(login_ok, login_failed)
        factory.run()


def handle_chat(message, protocol):
    if re.match(r'From Amelorate: say', message):
        say(message[20:], protocol)
        return True
    match = re.match(r'From .*:\s', message)
    if match:
        name = message[5:].split(': ')[0]
        message = message[match.end():]
        print(name)
        for command in COMMANDS['regex'].keys():
            if re.match(command, message):
                locate('commands.' + COMMANDS['regex'][command] + '.call')(message, name, protocol)
                return True
        say('/r Sorry, that command was not recognized as valid.', protocol)
        return False
    else:
        return False


def say(message, protocol):
    if len(message) >= 100:
        raise ChatMessageTooLongError
    protocol.send_packet("chat_message", protocol.buff_type.pack_string(message))


if __name__ == '__main__':
    main()
