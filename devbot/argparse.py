from typing import Dict, Union
from enum import Enum

import re


class UnknownFlagError(Exception):
    pass


class Flag:
    """
    Base class of every flag class used in parsing args. This class is not a valid flag however.
    """

    def __init__(self, short_name: str, long_name: str):
        """
        :param short_name: The short version of the argument. Must be exactly one character.
        :param long_name: The long version of the argument. Can be any number of characters.
        """
        self.short = short_name
        self.long = long_name


class BooleanFlag(Flag):
    """
    A flag that is either present or isn't. Defaults to False if it isn't found while parsing.
    """


class ContentFlag(Flag):
    """
    A flag that expects some string after it. One array position is read if this flag appears as it's full form, or the
    rest of the array position is read if it is in it's short form. If it is not present, the value is null.
    """


def parse_flags(args: [str], parsedef: Dict[str, Flag]) -> (Dict[str, Union[str, bool]], [str]):
    """
    Parses an array of strings into a dictionary of arguments, and an array of strings that are not arguments.

    :param args: The arguments passed to the command, without any command name. The strings can contain whitespace,
                 which is ignored while parsing, unless it is after a ContentFlag.
    :param parsedef: The definition for how args should be parsed. The key is the name that the value will take in the
                     returned dictionary, and the value is the type that it will take. This can be either a BooleanFlag
                     for a bool, or a ContentFlag for a str.
    :return A tuple of a dictionary with the keys of parsedef, and the values replaced according to the values of
            parsedef. The str in the second position is the rest of the arguments that did not begin with a dash nor
            were after a ContentFlag.
    """
    short_map = {}
    long_map = {}
    for name, flag in parsedef.items():
        if type(flag) == Flag:
            raise TypeError('Flag is not an allowed flag in parsedef.')
        short_map[flag.short] = (name, flag)
        long_map[flag.long] = (name, flag)

    class Mode(Enum):
        parsearg = 1
        restargs = 2
        longcontentflag = 3

    mode = Mode.parsearg
    rest_args = []
    return_dict = {}
    for arg in args:
        if mode == Mode.parsearg:
            if arg == '--':
                mode = Mode.restargs
            elif re.match(r'-[^-]', arg):
                for i, short_arg in enumerate(list(arg[1:])):
                    if short_arg not in short_map:
                        raise UnknownFlagError('Unknown short flag -{}'.format(short_arg))
                    elif type(short_map[short_arg][1]) == BooleanFlag:
                        return_dict[short_map[short_arg][0]] = True
                    elif type(short_map[short_arg][1]) == ContentFlag:
                        return_dict[short_map[short_arg][0]] = arg[i + 2:]
                        break
            elif arg.startswith('--'):
                long_arg = arg[2:]
                if long_arg not in long_map:
                    raise UnknownFlagError('Unknown long flag --{}'.format(long_arg))
                elif type(long_map[long_arg][1]) == BooleanFlag:
                    return_dict[long_map[long_arg][0]] = True
                elif type(long_map[long_arg][1]) == ContentFlag:
                    mode = Mode.longcontentflag
            else:
                mode = Mode.restargs
                rest_args.append(arg)
        elif mode == Mode.restargs:
            rest_args.append(arg)
        elif mode == Mode.longcontentflag:
            # noinspection PyUnboundLocalVariable
            # This usage of long_arg is intentional, because this is executed only after a content longarg is parsed.
            return_dict[long_map[long_arg][0]] = arg
            mode = Mode.parsearg

    for name, flag in parsedef.items():
        if name not in return_dict:
            if type(flag) == BooleanFlag:
                return_dict[name] = False
            elif type(flag) == ContentFlag:
                return_dict[name] = None
    return return_dict, rest_args
