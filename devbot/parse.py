from pypeg2 import *


class DQuotedText:
    grammar = '"', attr('text', re.compile(r"[\w\-!?%@#$^&*()\[\]']*")), '"'


class SQuotedText:
    grammar = "'", attr('text', re.compile(r'[\w\-!?%@#$^&*()\[\]"]*')), "'"


class UnquotedText:
    grammar = attr('text', re.compile(r'[\w\-!?%@#$^&*()\[\]]+'))


class AbsoluteArgument:
    grammar = attr('text', [DQuotedText, SQuotedText, UnquotedText])


class RedirectedArgument:
    pass


class Argument:
    grammar = attr('content', [RedirectedArgument, AbsoluteArgument])


class Command:
    grammar = attr('command'), [attr('args', maybe_some(Argument, blank)), '']
    args = None


RedirectedArgument.grammar = '<(', attr('command', Command), ')'


class PrivateMessage:
    grammar = 'From', attr('name'), ':', attr('message', restline)


class TerminalCommand:
    grammar = attr('content', Command)

