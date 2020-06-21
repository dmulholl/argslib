#!/usr/bin/env python3
import argslib

def main():
    # Instantiate an ArgParser instance.
    parser = argslib.ArgParser()
    parser.helptext = "Usage: example..."
    parser.version = "1.0"

    # Register a flag and a string-valued option.
    parser.flag("foo f")
    parser.option("bar b")

    # Parse the command line arguments.
    parser.parse()
    print(parser)

if __name__ == "__main__":
    main()
