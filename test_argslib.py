# ------------------------------------------------------------------------------
# Unit tests: run using pytest.
# ------------------------------------------------------------------------------

import argslib
import pytest


# ------------------------------------------------------------------------------
# Flags.
# ------------------------------------------------------------------------------


def test_flag_empty():
    parser = argslib.ArgParser()
    parser.flag("foo f")
    parser.parse([])
    assert parser.found("foo") == False
    assert parser.count("foo") == 0


def test_flag_missing():
    parser = argslib.ArgParser()
    parser.flag("foo f")
    parser.parse(["bar", "baz"])
    assert parser.found("foo") == False
    assert parser.count("foo") == 0


def test_flag_longform():
    parser = argslib.ArgParser()
    parser.flag("foo f")
    parser.parse(["--foo"])
    assert parser.found("foo") == True
    assert parser.count("foo") == 1


def test_flag_shortform():
    parser = argslib.ArgParser()
    parser.flag("foo f")
    parser.parse(["-f"])
    assert parser.found("foo") == True
    assert parser.count("foo") == 1


def test_flag_multiple():
    parser = argslib.ArgParser()
    parser.flag("foo f")
    parser.parse(["-fff", "--foo"])
    assert parser.found("foo") == True
    assert parser.count("foo") == 4


# ------------------------------------------------------------------------------
# Options.
# ------------------------------------------------------------------------------


def test_string_option_empty():
    parser = argslib.ArgParser()
    parser.option("foo f")
    parser.parse([])
    assert parser.value("foo") == None
    assert parser.found("foo") == False
    assert parser.count("foo") == 0


def test_string_option_missing():
    parser = argslib.ArgParser()
    parser.option("foo f")
    parser.parse(["bar", "baz"])
    assert parser.value("foo") == None
    assert parser.found("foo") == False
    assert parser.count("foo") == 0


def test_string_option_longform():
    parser = argslib.ArgParser()
    parser.option("foo f")
    parser.parse(["--foo", "bar"])
    assert parser.value("foo") == "bar"
    assert parser.found("foo") == True
    assert parser.count("foo") == 1


def test_string_option_shortform():
    parser = argslib.ArgParser()
    parser.option("foo f")
    parser.parse(["-f", "bar"])
    assert parser.value("foo") == "bar"
    assert parser.found("foo") == True
    assert parser.count("foo") == 1


def test_string_option_longform_equals():
    parser = argslib.ArgParser()
    parser.option("foo f")
    parser.parse(["--foo=bar"])
    assert parser.value("foo") == "bar"
    assert parser.found("foo") == True
    assert parser.count("foo") == 1


def test_string_option_shortform_equals():
    parser = argslib.ArgParser()
    parser.option("foo f")
    parser.parse(["-f=bar"])
    assert parser.value("foo") == "bar"
    assert parser.found("foo") == True
    assert parser.count("foo") == 1


def test_string_option_missing_value():
    parser = argslib.ArgParser()
    parser.option("foo f")
    with pytest.raises(SystemExit):
        parser.parse(["--foo"])


def test_string_option_multiple():
    parser = argslib.ArgParser()
    parser.option("foo f")
    parser.parse(["--foo", "bar", "-f", "baz", "-ff", "bam", "bif"])
    assert parser.value("foo") == "bif"
    assert parser.found("foo") == True
    assert parser.count("foo") == 4
    assert parser.values("foo")[0] == "bar"
    assert parser.values("foo")[3] == "bif"


def test_string_option_with_default():
    parser = argslib.ArgParser()
    parser.option("foo f", default="bar")
    parser.parse([])
    assert parser.value("foo") == "bar"
    assert parser.found("foo") == False
    assert parser.count("foo") == 0


def test_int_option():
    parser = argslib.ArgParser()
    parser.option("foo f", type=int)
    parser.parse(["--foo", "999"])
    assert parser.value("foo") == 999
    assert parser.found("foo") == True
    assert parser.count("foo") == 1


def test_int_option_with_default():
    parser = argslib.ArgParser()
    parser.option("foo f", type=int, default=101)
    parser.parse([])
    assert parser.value("foo") == 101
    assert parser.found("foo") == False
    assert parser.count("foo") == 0


def test_int_option_invalid_value():
    parser = argslib.ArgParser()
    parser.option("foo f", type=int)
    with pytest.raises(SystemExit):
        parser.parse(["--foo", "bar"])


def test_int_option_negative_value():
    parser = argslib.ArgParser()
    parser.option("foo f", type=int)
    parser.parse(["--foo", "-999"])
    assert parser.value("foo") == -999


def test_float_option():
    parser = argslib.ArgParser()
    parser.option("foo f", type=float)
    parser.parse(["--foo", "99.9"])
    assert parser.value("foo") == 99.9
    assert parser.found("foo") == True
    assert parser.count("foo") == 1


def test_float_option_with_default():
    parser = argslib.ArgParser()
    parser.option("foo f", type=float, default=10.1)
    parser.parse([])
    assert parser.value("foo") == 10.1
    assert parser.found("foo") == False
    assert parser.count("foo") == 0


def test_condensed_options():
    parser = argslib.ArgParser()
    parser.flag("x")
    parser.option("s")
    parser.option("i", type=int)
    parser.option("f", type=float)
    parser.parse(["-xsif", "strval", "99", "99.99"])
    assert parser.found("x") == True
    assert parser.value("s") == "strval"
    assert parser.value("i") == 99
    assert parser.value("f") == 99.99


# ------------------------------------------------------------------------------
# Unrecognised options.
# ------------------------------------------------------------------------------


def test_unrecognised_longform_option():
    parser = argslib.ArgParser()
    with pytest.raises(SystemExit):
        parser.parse(["--foo"])


def test_unrecognised_shortform_option():
    parser = argslib.ArgParser()
    with pytest.raises(SystemExit):
        parser.parse(["-f"])


# ------------------------------------------------------------------------------
# Positional arguments.
# ------------------------------------------------------------------------------


def test_positional_args_empty():
    parser = argslib.ArgParser()
    parser.parse([])
    assert len(parser.args) == 0


def test_positional_args():
    parser = argslib.ArgParser()
    parser.flag("foo")
    parser.option("bar")
    parser.parse(["--foo", "arg1", "--bar", "baz", "arg2"])
    assert len(parser.args) == 2
    assert parser.args[0] == "arg1"
    assert parser.args[1] == "arg2"


def test_option_parsing_switch():
    parser = argslib.ArgParser()
    parser.parse(["foo", "--", "--bar", "--baz"])
    assert len(parser.args) == 3


# ------------------------------------------------------------------------------
# Commands.
# ------------------------------------------------------------------------------


def test_command_with_options():
    parser = argslib.ArgParser()
    cmd_parser = parser.command("cmd")
    cmd_parser.flag("foo")
    cmd_parser.option("bar")
    parser.parse([
        "cmd",
        "--foo",
        "--bar", "barval",
        "arg1", "arg2",
    ])
    assert parser.command_name == "cmd"
    assert parser.command_parser.found("foo") == True
    assert parser.command_parser.value("bar") == "barval"
    assert len(parser.command_parser.args) == 2
