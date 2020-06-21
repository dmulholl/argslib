#!/usr/bin/env python3
import argslib

def main():
    # Instantiate an ArgParser instance.
    parser = argslib.ArgParser()
    parser.helptext = "Usage: example..."
    parser.version = "1.0"

    # Register a command 'boo'. The command can have its own helptext, flags, and options.
    cmd_parser = parser.command("boo")
    cmd_parser.helptext = "Usage: example boo..."
    cmd_parser.flag("foo f")
    cmd_parser.option("bar b")

    # If the command is found, the callback function will be called.
    cmd_parser.callback = cmd_boo

    # Parse the command line arguments.
    parser.parse()
    print(parser)

def cmd_boo(cmd_name, cmd_parser):
    print("------------ boo! ------------")
    print(cmd_parser)
    print("------------------------------\n")

if __name__ == "__main__":
    main()
