# --------------------------------------------------------------------------
# Unit tests for the janus module. Run using pytest.
# --------------------------------------------------------------------------

import janus
import pytest


# --------------------------------------------------------------------------
# Boolean options.
# --------------------------------------------------------------------------


def test_bool_option_empty():
    parser = janus.ArgParser()
    parser.new_flag("bool")
    parser.parse([])
    assert parser.get("bool") == False


def test_bool_option_missing():
    parser = janus.ArgParser()
    parser.new_flag("bool")
    parser.parse(["foo", "bar"])
    assert parser.get("bool") == False


def test_bool_option_longform():
    parser = janus.ArgParser()
    parser.new_flag("bool")
    parser.parse(["--bool"])
    assert parser.get("bool") == True


def test_bool_option_shortform():
    parser = janus.ArgParser()
    parser.new_flag("bool b")
    parser.parse(["-b"])
    assert parser.get("bool") == True


def test_bool_option_dict_syntax():
    parser = janus.ArgParser()
    parser.new_flag("bool")
    parser.parse(["--bool"])
    assert parser["bool"] == True


# --------------------------------------------------------------------------
# Boolean lists.
# --------------------------------------------------------------------------


def test_bool_list_empty():
    parser = janus.ArgParser()
    parser.new_flag("bool")
    parser.parse([])
    assert parser.len_list("bool") == 0


def test_bool_list_longform():
    parser = janus.ArgParser()
    parser.new_flag("bool")
    parser.parse(["--bool", "--bool", "--bool"])
    assert parser.len_list("bool") == 3


def test_bool_list_shortform():
    parser = janus.ArgParser()
    parser.new_flag("bool b")
    parser.parse(["-b", "-bb"])
    assert parser.len_list("bool") == 3


def test_bool_list_mixed():
    parser = janus.ArgParser()
    parser.new_flag("bool b")
    parser.parse(["--bool", "-bb"])
    assert parser.len_list("bool") == 3


# --------------------------------------------------------------------------
# String options.
# --------------------------------------------------------------------------


def test_string_option_empty():
    parser = janus.ArgParser()
    parser.new_str("string", fallback="default")
    parser.parse([])
    assert parser.get("string") == "default"


def test_string_option_missing():
    parser = janus.ArgParser()
    parser.new_str("string", fallback="default")
    parser.parse(["foo", "bar"])
    assert parser.get("string") == "default"


def test_string_option_longform():
    parser = janus.ArgParser()
    parser.new_str("string", fallback="default")
    parser.parse(["--string", "value"])
    assert parser.get("string") == "value"


def test_string_option_shortform():
    parser = janus.ArgParser()
    parser.new_str("string s", fallback="default")
    parser.parse(["-s", "value"])
    assert parser.get("string") == "value"


def test_string_option_longform_equals():
    parser = janus.ArgParser()
    parser.new_str("string", fallback="default")
    parser.parse(["--string=value"])
    assert parser.get("string") == "value"


def test_string_option_shortform_equals():
    parser = janus.ArgParser()
    parser.new_str("string s", fallback="default")
    parser.parse(["-s=value"])
    assert parser.get("string") == "value"


def test_string_option_dict_syntax():
    parser = janus.ArgParser()
    parser.new_str("string", fallback="default")
    parser.parse(["--string", "value"])
    assert parser["string"] == "value"


def test_string_option_missing_value():
    parser = janus.ArgParser()
    parser.new_str("string", fallback="default")
    with pytest.raises(SystemExit):
        parser.parse(["--string"])


# --------------------------------------------------------------------------
# String lists.
# --------------------------------------------------------------------------


def test_string_list_empty():
    parser = janus.ArgParser()
    parser.new_str("string")
    parser.parse([])
    assert parser.len_list("string") == 0


def test_string_list_longform():
    parser = janus.ArgParser()
    parser.new_str("string")
    parser.parse(["--string", "foo", "bar", "--string", "baz"])
    assert parser.len_list("string") == 2
    assert parser.get_list("string")[0] == "foo"
    assert parser.get_list("string")[1] == "baz"


def test_string_list_shortform():
    parser = janus.ArgParser()
    parser.new_str("string s")
    parser.parse(["-s", "foo", "bar", "-s", "baz"])
    assert parser.len_list("string") == 2
    assert parser.get_list("string")[0] == "foo"
    assert parser.get_list("string")[1] == "baz"


def test_string_list_mixed():
    parser = janus.ArgParser()
    parser.new_str("string s")
    parser.parse(["--string", "foo", "bar", "-s", "baz"])
    assert parser.len_list("string") == 2
    assert parser.get_list("string")[0] == "foo"
    assert parser.get_list("string")[1] == "baz"


# --------------------------------------------------------------------------
# Integer options.
# --------------------------------------------------------------------------


def test_int_option_empty():
    parser = janus.ArgParser()
    parser.new_int("int", fallback=101)
    parser.parse([])
    assert parser.get("int") == 101


def test_int_option_missing():
    parser = janus.ArgParser()
    parser.new_int("int", fallback=101)
    parser.parse(["foo", "bar"])
    assert parser.get("int") == 101


def test_int_option_longform():
    parser = janus.ArgParser()
    parser.new_int("int", fallback=101)
    parser.parse(["--int", "202"])
    assert parser.get("int") == 202


def test_int_option_shortform():
    parser = janus.ArgParser()
    parser.new_int("int i", fallback=101)
    parser.parse(["-i", "202"])
    assert parser.get("int") == 202


def test_int_option_longform_equals():
    parser = janus.ArgParser()
    parser.new_int("int", fallback=101)
    parser.parse(["--int=202"])
    assert parser.get("int") == 202


def test_int_option_shortform_equals():
    parser = janus.ArgParser()
    parser.new_int("int i", fallback=101)
    parser.parse(["-i=202"])
    assert parser.get("int") == 202


def test_int_option_dict_syntax():
    parser = janus.ArgParser()
    parser.new_int("int", fallback=101)
    parser.parse(["--int", "202"])
    assert parser["int"] == 202


def test_int_option_missing_value():
    parser = janus.ArgParser()
    parser.new_int("int", fallback=101)
    with pytest.raises(SystemExit):
        parser.parse(["--int"])


def test_int_option_invalid_value():
    parser = janus.ArgParser()
    parser.new_int("int", fallback=101)
    with pytest.raises(SystemExit):
        parser.parse(["--int", "foo"])


def test_int_option_negative_value():
    parser = janus.ArgParser()
    parser.new_int("int", fallback=101)
    parser.parse(["--int", "-202"])
    assert parser.get("int") == -202


# --------------------------------------------------------------------------
# Integer lists.
# --------------------------------------------------------------------------


def test_int_list_missing():
    parser = janus.ArgParser()
    parser.new_int("int")
    parser.parse([])
    assert parser.len_list("int") == 0


def test_int_list_longform():
    parser = janus.ArgParser()
    parser.new_int("int")
    parser.parse(["--int", "123", "456", "--int", "789"])
    assert parser.len_list("int") == 2
    assert parser.get_list("int")[0] == 123
    assert parser.get_list("int")[1] == 789


def test_int_list_shortform():
    parser = janus.ArgParser()
    parser.new_int("int i")
    parser.parse(["-i", "123", "456", "-i", "789"])
    assert parser.len_list("int") == 2
    assert parser.get_list("int")[0] == 123
    assert parser.get_list("int")[1] == 789


def test_int_list_mixed():
    parser = janus.ArgParser()
    parser.new_int("int i")
    parser.parse(["--int", "123", "456", "-i", "789"])
    assert parser.len_list("int") == 2
    assert parser.get_list("int")[0] == 123
    assert parser.get_list("int")[1] == 789


# --------------------------------------------------------------------------
# Float options.
# --------------------------------------------------------------------------


def test_float_option_empty():
    parser = janus.ArgParser()
    parser.new_float("float", fallback=1.1)
    parser.parse([])
    assert parser.get("float") == 1.1


def test_float_option_missing():
    parser = janus.ArgParser()
    parser.new_float("float", fallback=1.1)
    parser.parse(["foo", "bar"])
    assert parser.get("float") == 1.1


def test_float_option_longform():
    parser = janus.ArgParser()
    parser.new_float("float", fallback=1.1)
    parser.parse(["--float", "2.2"])
    assert parser.get("float") == 2.2


def test_float_option_shortform():
    parser = janus.ArgParser()
    parser.new_float("float f", fallback=1.1)
    parser.parse(["-f", "2.2"])
    assert parser.get("float") == 2.2


def test_float_option_longform_equals():
    parser = janus.ArgParser()
    parser.new_float("float", fallback=1.1)
    parser.parse(["--float=2.2"])
    assert parser.get("float") == 2.2


def test_float_option_shortform_equals():
    parser = janus.ArgParser()
    parser.new_float("float f", fallback=1.1)
    parser.parse(["-f=2.2"])
    assert parser.get("float") == 2.2


def test_float_option_dict_syntax():
    parser = janus.ArgParser()
    parser.new_float("float", fallback=1.1)
    parser.parse(["--float", "2.2"])
    assert parser["float"] == 2.2


def test_float_option_missing_value():
    parser = janus.ArgParser()
    parser.new_float("float", fallback=1.1)
    with pytest.raises(SystemExit):
        parser.parse(["--float"])


def test_float_option_invalid_value():
    parser = janus.ArgParser()
    parser.new_float("float", fallback=1.1)
    with pytest.raises(SystemExit):
        parser.parse(["--float", "foo"])


def test_float_option_negative_value():
    parser = janus.ArgParser()
    parser.new_float("float", fallback=1.1)
    parser.parse(["--float", "-2.2"])
    assert parser.get("float") == -2.2


# --------------------------------------------------------------------------
# Float lists.
# --------------------------------------------------------------------------


def test_float_list_missing():
    parser = janus.ArgParser()
    parser.new_float("float")
    parser.parse([])
    assert parser.len_list("float") == 0


def test_float_list_longform():
    parser = janus.ArgParser()
    parser.new_float("float")
    parser.parse(["--float", "1.1", "2.2", "--float", "3.3"])
    assert parser.len_list("float") == 2
    assert parser.get_list("float")[0] == 1.1
    assert parser.get_list("float")[1] == 3.3


def test_float_list_shortform():
    parser = janus.ArgParser()
    parser.new_float("float f")
    parser.parse(["-f", "1.1", "2.2", "-f", "3.3"])
    assert parser.len_list("float") == 2
    assert parser.get_list("float")[0] == 1.1
    assert parser.get_list("float")[1] == 3.3


def test_float_list_mixed():
    parser = janus.ArgParser()
    parser.new_float("float f")
    parser.parse(["--float", "1.1", "2.2", "-f", "3.3"])
    assert parser.len_list("float") == 2
    assert parser.get_list("float")[0] == 1.1
    assert parser.get_list("float")[1] == 3.3


# --------------------------------------------------------------------------
# Multiple options.
# --------------------------------------------------------------------------


def test_multi_options_empty():
    parser = janus.ArgParser()
    parser.new_flag("bool1")
    parser.new_flag("bool2 b")
    parser.new_str("string1", fallback="default1")
    parser.new_str("string2 s", fallback="default2")
    parser.new_int("int1", fallback=101)
    parser.new_int("int2 i", fallback=202)
    parser.new_float("float1", fallback=1.1)
    parser.new_float("float2 f", fallback=2.2)
    parser.parse([])
    assert parser.get("bool1") == False
    assert parser.get("bool2") == False
    assert parser.get("string1") == "default1"
    assert parser.get("string2") == "default2"
    assert parser.get("int1") == 101
    assert parser.get("int2") == 202
    assert parser.get("float1") == 1.1
    assert parser.get("float2") == 2.2


def test_multi_options_longform():
    parser = janus.ArgParser()
    parser.new_flag("bool1")
    parser.new_flag("bool2 b")
    parser.new_str("string1", fallback="default1")
    parser.new_str("string2 s", fallback="default2")
    parser.new_int("int1", fallback=101)
    parser.new_int("int2 i", fallback=202)
    parser.new_float("float1", fallback=1.1)
    parser.new_float("float2 f", fallback=2.2)
    parser.parse([
        "--bool1",
        "--bool2",
        "--string1", "value1",
        "--string2", "value2",
        "--int1", "303",
        "--int2", "404",
        "--float1", "3.3",
        "--float2", "4.4",
    ])
    assert parser.get("bool1") == True
    assert parser.get("bool2") == True
    assert parser.get("string1") == "value1"
    assert parser.get("string2") == "value2"
    assert parser.get("int1") == 303
    assert parser.get("int2") == 404
    assert parser.get("float1") == 3.3
    assert parser.get("float2") == 4.4


def test_multi_options_shortform():
    parser = janus.ArgParser()
    parser.new_flag("bool1")
    parser.new_flag("bool2 b")
    parser.new_str("string1", fallback="default1")
    parser.new_str("string2 s", fallback="default2")
    parser.new_int("int1", fallback=101)
    parser.new_int("int2 i", fallback=202)
    parser.new_float("float1", fallback=1.1)
    parser.new_float("float2 f", fallback=2.2)
    parser.parse([
        "--bool1",
        "-b",
        "--string1", "value1",
        "-s", "value2",
        "--int1", "303",
        "-i", "404",
        "--float1", "3.3",
        "-f", "4.4",
    ])
    assert parser.get("bool1") == True
    assert parser.get("bool2") == True
    assert parser.get("string1") == "value1"
    assert parser.get("string2") == "value2"
    assert parser.get("int1") == 303
    assert parser.get("int2") == 404
    assert parser.get("float1") == 3.3
    assert parser.get("float2") == 4.4


# --------------------------------------------------------------------------
# Condensed short-form options.
# --------------------------------------------------------------------------


def test_condensed_options():
    parser = janus.ArgParser()
    parser.new_flag("bool b")
    parser.new_str("string s", fallback="default")
    parser.new_int("int i", fallback=101)
    parser.new_float("float f", fallback=1.1)
    parser.parse(["-bsif", "value", "202", "2.2"])
    assert parser["bool"] == True
    assert parser["string"] == "value"
    assert parser["int"] == 202
    assert parser["float"] == 2.2


# --------------------------------------------------------------------------
# Unrecognised options.
# --------------------------------------------------------------------------


def test_unrecognised_longform_option():
    parser = janus.ArgParser()
    with pytest.raises(SystemExit):
        parser.parse(["--foo"])


def test_unrecognised_shortform_option():
    parser = janus.ArgParser()
    with pytest.raises(SystemExit):
        parser.parse(["-f"])


# --------------------------------------------------------------------------
# Positional arguments.
# --------------------------------------------------------------------------


def test_positional_args_empty():
    parser = janus.ArgParser()
    parser.parse([])
    assert parser.has_args() == False


def test_positional_args():
    parser = janus.ArgParser()
    parser.parse(["foo", "bar"])
    assert parser.has_args() == True
    assert parser.num_args() == 2
    assert parser.get_args()[0] == "foo"
    assert parser.get_args()[1] == "bar"


def test_positional_args_list_syntax():
    parser = janus.ArgParser()
    parser.parse(["foo", "bar"])
    assert parser[0] == "foo"
    assert parser[1] == "bar"


def test_positional_args_as_ints():
    parser = janus.ArgParser()
    parser.parse(["1", "11"])
    assert parser.get_args_as_ints()[0] == 1
    assert parser.get_args_as_ints()[1] == 11


def test_positional_args_as_floats():
    parser = janus.ArgParser()
    parser.parse(["1.1", "11.1"])
    assert parser.get_args_as_floats()[0] == 1.1
    assert parser.get_args_as_floats()[1] == 11.1


# --------------------------------------------------------------------------
# Option parsing switch.
# --------------------------------------------------------------------------


def test_option_parsing_switch():
    parser = janus.ArgParser()
    parser.parse(["foo", "--", "--bar", "--baz"])
    assert parser.num_args() == 3


# --------------------------------------------------------------------------
# Commands.
# --------------------------------------------------------------------------


def test_command_absent():
    parser = janus.ArgParser()
    cmd_parser = parser.new_cmd("cmd", "helptext", lambda p: None)
    parser.parse([])
    assert parser.has_cmd() == False


def test_command_present():
    parser = janus.ArgParser()
    cmd_parser = parser.new_cmd("cmd", "helptext", lambda p: None)
    parser.parse(["cmd"])
    assert parser.has_cmd() == True
    assert parser.get_cmd_name() == "cmd"
    assert parser.get_cmd_parser() == cmd_parser


def test_command_with_options():
    parser = janus.ArgParser()
    cmd_parser = parser.new_cmd("cmd", "helptext", lambda p: None)
    cmd_parser.new_flag("bool")
    cmd_parser.new_str("string")
    cmd_parser.new_int("int")
    cmd_parser.new_float("float")
    parser.parse([
        "cmd",
        "foo", "bar",
        "--string", "value",
        "--int", "202",
        "--float", "2.2",
    ])
    assert parser.has_cmd() == True
    assert parser.get_cmd_name() == "cmd"
    assert parser.get_cmd_parser() == cmd_parser
    assert cmd_parser.has_args() == True
    assert cmd_parser.num_args() == 2
    assert cmd_parser["string"] == "value"
    assert cmd_parser["int"] == 202
    assert cmd_parser["float"] == 2.2
