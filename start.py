import configparser
import os.path
import sys


CONFIG_FILE = 'config.cfg'


def generate_config_file(name, config):
    config['auth'] = {'username': 'USERNAME',
                      'password': 'PASSWORD',
                      'auth': 'true'}
    with open(name, 'w') as configfile:
        configfile.write('# Config automatically generated. Delete this file to reset.\n\n')
        config.write(configfile)
    print('Config file generated. Edit the username and password fields to set up an account.')
    sys.exit()

cfg = configparser.ConfigParser()
if os.path.isfile(CONFIG_FILE):
    cfg.read(CONFIG_FILE)
else:
    generate_config_file(CONFIG_FILE, cfg)
