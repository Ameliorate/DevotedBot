import pypeg2 as p
import re


class DQuotedText:
    grammar = '"', p.attr('text', re.compile(r"[^\"]*")), '"'


class SQuotedText:
    grammar = "'", p.attr('text', re.compile(r'[^\']*')), "'"


class UnquotedText:
    grammar = p.attr('text', re.compile(r'[^\'\" ]+'))


class AbsoluteArgument:
    grammar = p.attr('text', [DQuotedText, SQuotedText, UnquotedText])


class RedirectedArgument:
    pass


class Argument:
    grammar = p.attr('content', [RedirectedArgument, AbsoluteArgument])


class Command:
    grammar = p.attr('command'), p.optional(p.blank, p.attr('args', p.some(Argument, p.blank)))
    args = None

RedirectedArgument.grammar = '<(', p.attr('command', Command), ')'


class PrivateMessage:
    grammar = 'From', p.attr('name'), ':', p.attr('message', p.restline)


class TerminalCommand:
    grammar = p.attr('content', Command)

