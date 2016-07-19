from pypeg2 import *


class DQuotedText:
    grammar = '"', attr('text', re.compile(r"[a-zA-Z\s_+-/*']*")), '"'


class SQuotedText:
    grammar = "'", attr('text', re.compile(r'[a-zA-Z\s_+-/*"]*')), "'"


class UnquotedText:
    grammar = attr('text')


class AbsoluteArgument:
    grammar = attr('text', [UnquotedText, DQuotedText, SQuotedText])


class RedirectedArgument:
    pass


class Argument:
    grammar = attr('content', [RedirectedArgument, AbsoluteArgument])


class Command:
    grammar = attr('command'), [attr('args', csl(Argument, separator='')), '']


RedirectedArgument.grammar = '<(', attr('command', Command), ')'


class PrivateMessage:
    grammar = 'From', attr('name'), ':', attr('message', restline)


class TerminalCommand:
    grammar = attr('content', Command)

