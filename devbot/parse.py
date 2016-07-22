import pypeg2 as p


class DQuotedText:
    grammar = '"', p.attr('text', p.re.compile(r"[\w\-!?%@#$^&*()\[\]']*")), '"'


class SQuotedText:
    grammar = "'", p.attr('text', p.re.compile(r'[\w\-!?%@#$^&*()\[\]"]*')), "'"


class UnquotedText:
    grammar = p.attr('text', p.re.compile(r'[\w\-!?%@#$^&*()\[\]]+'))


class AbsoluteArgument:
    grammar = p.attr('text', [DQuotedText, SQuotedText, UnquotedText])


class RedirectedArgument:
    command = None
    grammar = None


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

