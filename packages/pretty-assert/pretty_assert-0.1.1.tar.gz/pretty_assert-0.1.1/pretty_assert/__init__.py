import functools
import inspect
import os
import shutil
import sys
from functools import wraps
from types import FrameType
from typing import Callable, Iterable, Optional

import icdiff
import pprintpp
from termcolor import colored

pformat = functools.partial(pprintpp.pformat, indent=2, width=1)
eprintln = functools.partial(print, file=sys.stderr)


def __get_lines_of_frame_source(frame: FrameType, start: int, end: int):
    """
    Get the lines of source code from a given frame between the specified start and end line numbers.

    Args:
        frame (FrameType): The frame object representing the source code.
        start (int): The starting line number.
        end (int): The ending line number (including).

    Returns:
        list: A list of source code lines between the specified start and end line numbers.
    """

    # source_lines start from 0
    # source_start_number is 0 if the frame contains the whole file;
    # source_start_number will be actual number (start from 1) if the frame contains part of the file.

    source_lines, source_start_number = inspect.getsourcelines(frame)
    if source_start_number == 0:
        source_start_number = 1
    return source_lines[start - source_start_number : end - source_start_number + 1]


class GlobalConfig:
    __slots__ = (
        "comment_message_color",
        "other_message_color",
        "code_color",
        "line_number_color",
        "comment_message_attrs",
        "file_path_color",
        "show_source_info",
        "classic_eq",
        "exit",
    )

    def __init__(
        self,
        comment_message_color="red",
        comment_message_attrs=["bold"],
        other_message_color=None,
        file_path_color=None,
        code_color="yellow",
        line_number_color="grey",
        exit=True,
        classic_eq=False,
        show_source_info=True,
    ):
        os.system("color")
        self.comment_message_color = comment_message_color
        self.comment_message_attrs = comment_message_attrs
        self.other_message_color = other_message_color
        self.file_path_color = file_path_color
        self.code_color = code_color
        self.line_number_color = line_number_color
        self.classic_eq = classic_eq
        self.exit = exit
        self.show_source_info = show_source_info


global_config = None


def init(
    comment_message_color="red",
    comment_message_attrs=["bold"],
    other_message_color: Optional[str] = None,
    file_path_color: Optional[str] = None,
    code_color="yellow",
    line_number_color="grey",
    classic_eq=False,
    exit=True,
    show_source_info=True,
):
    """
    Initialize the global config.

    Args:
        `comment_message_color` (str, optional): The color of the comment message. Defaults to "red".
        `comment_message_attrs` (list, optional): The attributes of the comment message. Defaults to ["bold"].
        `other_message_color` (str, optional): The color of the other message. Defaults to None.
        `file_path_color` (str, optional): The color of the file path. Defaults to None.
        `code_color` (str, optional): The color of the code. Defaults to "yellow".
        `line_number_color` (str, optional): The color of the line number. Defaults to "grey".
        `exit` (bool, optional): Whether to exit the program after the assertion. Defaults to True. If set to False, an AssertionError will be raised.
        `classic_eq` (bool, optional): Whether to use the classic equality check style (like `assert_gt`, `assert_lt`... do) for `assert_eq`. Defaults to False.
        `show_source_info` (bool, optional): Whether to show the source code information, including filename and code. Defaults to True.
    """
    global global_config
    global_config = GlobalConfig(
        comment_message_color=comment_message_color,
        comment_message_attrs=comment_message_attrs,
        other_message_color=other_message_color,
        file_path_color=file_path_color,
        code_color=code_color,
        line_number_color=line_number_color,
        exit=exit,
        classic_eq=classic_eq,
        show_source_info=show_source_info,
    )

    return global_config


def _get_or_init(**kwargs):
    global global_config
    if global_config is None:
        global_config = GlobalConfig(**kwargs)


def diff(a, b):
    COLS = shutil.get_terminal_size().columns - 13
    lines_a = pformat(a).splitlines()
    lines_b = pformat(b).splitlines()
    differ = icdiff.ConsoleDiff(
        cols=COLS,
        highlight=True,
        tabsize=2,
        strip_trailing_cr=True,
    )
    icdiff_lines = list(differ.make_table(lines_a, lines_b, context=True))
    return "\n".join(icdiff_lines)


def general_diff(a, b, leading="", middle=" ", trailing=""):
    return "".join(
        (
            colored(leading, global_config.other_message_color),
            " ",
            colored(pformat(a), "red"),
            colored(middle, global_config.other_message_color),
            colored(pformat(b), "green"),
            colored(trailing, global_config.other_message_color),
        )
    )


def pretty_wrapper(func, *args):
    @wraps(func)
    def wrapper(*args):
        _get_or_init()

        args_len = len(inspect.getfullargspec(func).args)
        result: bool = func(*args[:args_len])
        comment = args[-1] if len(args) > args_len else None
        if result:
            return result

        frame = inspect.currentframe().f_back
        filename = inspect.getfile(frame)
        frame_stack = inspect.stack()[1]
        start = frame_stack.positions.lineno
        end = frame_stack.positions.end_lineno
        source_code = __get_lines_of_frame_source(frame, start, end)

        if global_config.show_source_info:
            eprintln(
                colored(
                    f"{colored('Assertion Failed', attrs=['bold'])} in ",
                    global_config.other_message_color,
                ),
                colored(filename, global_config.file_path_color),
                ":",
                sep="`",
            )
            for line_index, line in enumerate(source_code):
                eprintln(
                    colored(line_index + start, global_config.line_number_color),
                    colored(line.rstrip(), global_config.code_color),
                    sep="  ",
                )

        if comment is not None:
            eprintln(
                colored("Comment:", global_config.other_message_color),
                colored(
                    comment,
                    global_config.comment_message_color,
                    attrs=global_config.comment_message_attrs,
                ),
                sep=" ",
            )
        if global_config.exit:
            sys.exit(1)
        else:
            raise AssertionError

    return wrapper


@pretty_wrapper
def assert_(a):
    if a:
        return True
    eprintln(general_diff(a, True, "Not True:", " is not "))
    return False


@pretty_wrapper
def assert_eq(a, b):
    if a == b:
        return True
    if global_config.classic_eq:
        eprintln(general_diff(a, b, "Found not equal:", " != "))
        return False
    eprintln(colored("Not equal:", global_config.other_message_color))
    eprintln(diff(a, b))
    return False


@pretty_wrapper
def assert_ne(a, b):
    if a != b:
        return True
    eprintln(general_diff(a, b, "Found equal:", " == "))
    return False


@pretty_wrapper
def assert_gt(a, b):
    if a > b:
        return True
    eprintln(general_diff(a, b, "Found not greater than:", " <= "))
    return False


@pretty_wrapper
def assert_lt(a, b):
    if a < b:
        return True
    eprintln(general_diff(a, b, "Found not less than:", " >= "))
    return False


@pretty_wrapper
def assert_ge(a, b):
    if a >= b:
        return True
    eprintln(general_diff(a, b, "Found less:", " < "))
    return False


@pretty_wrapper
def assert_le(a, b):
    if a <= b:
        return True
    eprintln(general_diff(a, b, "Found greater:", " > "))
    return False


@pretty_wrapper
def assert_in(a, b: Iterable):
    if a in b:
        return True
    eprintln(general_diff(a, b, "Found not in:", " is not in "))
    return False


@pretty_wrapper
def assert_not_in(a, b: Iterable):
    if a not in b:
        return True
    eprintln(general_diff(a, b, "Found in:", " in "))
    return False


@pretty_wrapper
def assert_is(a, b):
    if a is b:
        return True
    eprintln(general_diff(a, b, "Found not is:", " is not "))
    return False


@pretty_wrapper
def assert_is_not(a, b):
    if a is not b:
        return True
    eprintln(general_diff(a, b, "Found is:", " is "))
    return False


@pretty_wrapper
def assert_if(a, b, verify_func: Callable):
    if verify_func(a, b):
        return True
    eprintln(
        general_diff(a, b, "Not satisfied:", ", ", trailing=" not satisfy function")
    )
    return False
