#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# A simple application demonstrating Janus in action.
# ------------------------------------------------------------------------------

import janus


# This sample application will parse its own command-line arguments.
def main():

    # We instantiate an argument parser, optionally supplying help text and a
    # version string. Supplying help text activates an automatic --help flag,
    # supplying a version string activates an automatic --version flag.
    parser = janus.ArgParser("App Help", "Version 1.2.3")

    # Register a flag, --bool, with a single-character alias, -b. A flag is a
    # boolean option --- it's either present (true) or absent (false).
    parser.new_flag("bool b")

    # Register a string option, --string <arg>, with a single-character alias,
    # -s <arg>, and a custom fallback value.
    parser.new_str("string s", fallback="value")

    # Register an integer option, --int <arg>, with a single-character alias,
    # -i <arg>, and a custom fallback value.
    parser.new_int("int i", fallback=0)

    # Register a floating-point option, --float <arg>, with a single-character
    # alias, -f <arg>, and a custom fallback value.
    parser.new_float("float f", fallback=0.0)

    # Register a command 'foo', with an alias 'bar'. We need to supply the
    # command's help text and callback function.
    cmd_parser = parser.new_cmd("foo bar", "Command Help", callback)

    # Registering a command returns a new ArgParser instance dedicated to
    # parsing the command's arguments. We can register as many flags and
    # options as we like on this sub-parser. Note that the sub-parser can
    # reuse the parent's option names without interference.
    cmd_parser.new_flag("bool b")
    cmd_parser.new_int("int i")

    # Once all our options and commands have been registered we can call the
    # parser's parse() method with a list of argument strings. Only the root
    # parser's parse() method should be called --- command arguments will be
    # parsed automatically. The parse() method defaults to parsing the
    # application's command line arguments if no list is supplied.
    parser.parse()

    # We can now retrieve our option and argument values from the parser
    # instance. Here we simply dump the parser to stdout.
    print(parser)


# Callback method for the 'foo' command. This method will be called if the
# command is found. The method receives an ArgParser instance containing the
# command's parsed arguments. Here we simply dump it to stdout.
def callback(parser):
    print("---------- callback ----------")
    print(parser)
    print("------------------------------\n")


if __name__ == "__main__":
    main()
