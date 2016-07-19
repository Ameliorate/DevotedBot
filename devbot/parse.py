from pypeg2 import *


class PrivateMessage:
    grammar = 'From', attr('name'), ':', attr('message', restline)
