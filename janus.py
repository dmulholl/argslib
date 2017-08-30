# ----------------------------------------------------------------------------
# Janus: a minimalist argument-parsing library designed for building elegant
# command line interfaces.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# ----------------------------------------------------------------------------

import sys


# Library version number.
__version__ = "0.1.1"


# Print a message to stderr and exit with a non-zero error code.
def exit_error(msg):
    sys.exit("Error: %s." % msg)


# Exception raised when an invalid API call is attempted. (Invalid user input
# does not raise an exception; instead the application exits with an error
# message.)
class ArgParserError(Exception):
    pass


# Internal class for storing option data. Option type is one of 'bool',
# 'string', 'int', or 'float'.
class Option:

    def __init__(self, typestring):
        self.type = typestring
        self.found = False
        self.values = []
        self.fallback = None

    @property
    def value(self):
        if self.values:
            return self.values[-1]
        else:
            return self.fallback

    def try_set(self, arg):
        if self.type == "string":
            self.values.append(arg)
        elif self.type == "int":
            try:
                self.values.append(int(arg))
            except ValueError:
                exit_error("cannot parse '%s' as an integer" % arg)
        elif self.type == "float":
            try:
                self.values.append(float(arg))
            except ValueError:
                exit_error("cannot parse '%s' as a floating-point value" % arg)


# Internal class for making a list of arguments available as a stream.
class ArgStream:

    def __init__(self, args):
        self.args = list(args)
        self.length = len(self.args)
        self.index = 0

    # Returns the next argument from the stream.
    def next(self):
        self.index += 1
        return self.args[self.index - 1]

    # Returns true if the stream contains at least one more element.
    def has_next(self):
        return self.index < self.length


# An ArgParser instance is responsible for registering options and commands
# and parsing the input array of raw arguments. Note that every registered
# command recursively receives an ArgParser instance of its own.
class ArgParser:

    # Specifying a string of help text activates the automatic --help flag.
    # Specifying a version string activates the automatic --version flag.
    def __init__(self, helptext=None, version=None):

        # Help text for the application or command.
        self.helptext = helptext.strip() if helptext else None

        # Application version number as a string.
        self.version = version.strip() if version else None

        # Stores registered Option instances indexed by name.
        self.options = {}

        # Stores positional arguments parsed from the input stream.
        self.arguments = []

        # Stores registered command parsers indexed by command name.
        self.commands = {}

        # Stores a command parser's registered callback function.
        self.callback = None

        # Stores the command name, if a command was found while parsing.
        self.command = None

        # Stores a reference to a command parser's parent parser.
        self.parent = None

    # Enable dictionary/list-style access to options and arguments.
    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            return self.arguments[key]
        else:
            return self.get(key)

    # List all options and arguments for debugging.
    def __str__(self):
        lines = []

        lines.append("Options:")
        if self.options:
            for name, option in sorted(self.options.items()):
                lines.append("  %s: %s" % (name, option.values))
        else:
            lines.append("  [none]")

        lines.append("\nArguments:")
        if self.arguments:
            for arg in self.arguments:
                lines.append("  %s" % arg)
        else:
            lines.append("  [none]")

        lines.append("\nCommand:")
        if self.command:
            lines.append("  %s" % self.command)
        else:
            lines.append("  [none]")

        return "\n".join(lines)

    # Print the parser's help text and exit.
    def exit_help(self):
        sys.stdout.write(self.helptext + "\n")
        sys.exit()

    # Print the parser's version string and exit.
    def exit_version(self):
        sys.stdout.write(self.version + "\n")
        sys.exit()

    # ----------------------------------------------------------------------
    # Register options.
    # ----------------------------------------------------------------------

    # Register a boolean option with a default value of false.
    def new_flag(self, name):
        option = Option("bool")
        option.fallback = False
        for alias in name.split():
            self.options[alias] = option

    # Register a string option.
    def new_str(self, name, fallback=None):
        option = Option("string")
        option.fallback = fallback
        for alias in name.split():
            self.options[alias] = option

    # Register an integer option.
    def new_int(self, name, fallback=None):
        option = Option("int")
        option.fallback = fallback
        for alias in name.split():
            self.options[alias] = option

    # Register a floating-point option.
    def new_float(self, name, fallback=None):
        option = Option("float")
        option.fallback = fallback
        for alias in name.split():
            self.options[alias] = option

    # ----------------------------------------------------------------------
    # Get option values.
    # ----------------------------------------------------------------------

    # Returns true if the specified option was found while parsing.
    def found(self, name):
        option = self.options.get(name)
        if option:
            return option.found
        else:
            raise ArgParserError("'%s' is not a registered option" % name)

    # Returns the value of the specified option.
    def get(self, name):
        option = self.options.get(name)
        if option:
            return option.value
        else:
            raise ArgParserError("'%s' is not a registered option" % name)

    # Returns the specified option's list of values.
    def get_list(self, name):
        option = self.options.get(name)
        if option:
            return option.values
        else:
            raise ArgParserError("'%s' is not a registered option" % name)

    # Returns the length of the specified option's list of values.
    def len_list(self, name):
        option = self.options.get(name)
        if option:
            return len(option.values)
        else:
            raise ArgParserError("'%s' is not a registered option" % name)

    # ----------------------------------------------------------------------
    # Commands.
    # ----------------------------------------------------------------------

    # Register a command with its associated help text and callback function.
    def new_cmd(self, name, helptext, callback):
        parser = ArgParser(helptext)
        parser.parent = self
        parser.callback = callback
        for alias in name.split():
            self.commands[alias] = parser
        return parser

    # Returns true if the parser has found a command.
    def has_cmd(self):
        return self.command is not None

    # Returns the command name, if the parser has found a command, otherwise
    # returns None.
    def get_cmd_name(self):
        return self.command

    # Returns the command parser instance, if the parser has found a command,
    # otherwise returns None.
    def get_cmd_parser(self):
        return self.commands.get(self.command, None)

    # Returns a command parser's parent parser.
    def get_parent(self):
        return self.parent

    # ----------------------------------------------------------------------
    # Positional arguments.
    # ----------------------------------------------------------------------

    # Returns true if at least one positional argument has been found.
    def has_args(self):
        return len(self.arguments) > 0

    # Returns the number of positional arguments.
    def num_args(self):
        return len(self.arguments)

    # Returns the positional arguments as a list of strings.
    def get_args(self):
        return self.arguments

    # Convenience function: attempts to parse and return the positional
    # arguments as a list of integers.
    def get_args_as_ints(self):
        ints = []
        for arg in self.arguments:
            try:
                ints.append(int(arg))
            except ValueError:
                exit_error("cannot parse '%s' as an integer" % arg)
        return ints

    # Convenience function: attempts to parse and return the positional
    # arguments as a list of floats.
    def get_args_as_floats(self):
        floats = []
        for arg in self.arguments:
            try:
                floats.append(float(arg))
            except ValueError:
                exit_error("cannot parse '%s' as a float" % arg)
        return floats

    # ----------------------------------------------------------------------
    # Parse arguments.
    # ----------------------------------------------------------------------

    # Parse a list of string arguments. We default to parsing the command
    # line arguments, skipping the application path.
    def parse(self, args=sys.argv[1:]):
        self._parse_stream(ArgStream(args))

    # Parse a stream of string arguments.
    def _parse_stream(self, stream):
        parsing = True
        is_first_arg = True

        # Loop while we have arguments to process.
        while stream.has_next():

            # Fetch the next argument from the stream.
            arg = stream.next()

            # If parsing has been turned off, simply add the argument to the
            # list of positionals.
            if not parsing:
                self.arguments.append(arg)

            # If we encounter a '--' argument, turn off option-parsing.
            elif arg == "--":
                parsing = False

            # Is the argument a long-form option?
            elif arg.startswith("--"):
                self._parse_long_opt(arg[2:], stream)

            # Is the argument a short-form option?
            elif arg.startswith("-"):
                if arg == '-' or arg[1].isdigit():
                    self.arguments.append(arg)
                else:
                    self._parse_short_opt(arg[1:], stream)

            # Is the argument a registered command?
            elif is_first_arg and arg in self.commands:
                self.command = arg
                cmd_parser = self.commands[arg]
                cmd_parser._parse_stream(stream)
                cmd_parser.callback(cmd_parser)

            # Is the argument the automatic 'help' command?
            elif is_first_arg and arg == "help":
                if stream.has_next():
                    name = stream.next()
                    if name in self.commands:
                        self.commands[name].exit_help()
                    else:
                        exit_error("'%s' is not a recognised command" % name)
                else:
                    exit_error("the help command requires an argument")

            # Add the argument to our list of positionals.
            else:
                self.arguments.append(arg)

            is_first_arg = False

    # Parse an option of the form --name=value or -n=value.
    def _parse_equals_opt(self, prefix, arg):
        name, value = arg.split("=", maxsplit=1)
        option = self.options.get(name)

        if option is None:
            exit_error("%s%s is not a recognised option" % (prefix, name))
        elif option.type == "bool":
            exit_error("invalid format for boolean flag %s%s" % (prefix, name))
        elif value == "":
            exit_error("missing argument for %s%s" % (prefix, name))

        option.found = True
        option.try_set(value)

    # Parse a long-form option, i.e. an option beginning with a double dash.
    def _parse_long_opt(self, arg, stream):

        # Do we have an option of the form --name=value?
        if "=" in arg:
            self._parse_equals_opt("--", arg)

        # Is the argument a registered option name?
        elif arg in self.options:
            option = self.options[arg]
            option.found = True
            if option.type == "bool":
                option.values.append(True)
            elif stream.has_next():
                option.try_set(stream.next())
            else:
                exit_error("missing argument for --%s" % arg)

        # Is the argument the automatic --help flag?
        elif arg == "help" and self.helptext is not None:
            self.exit_help()

        # Is the argument the automatic --version flag?
        elif arg == "version" and self.version is not None:
            self.exit_version()

        # The argument is not a recognised option name.
        else:
            exit_error("--%s is not a recognised option" % arg)

    # Parse a short-form option, i.e. an option beginning with a single dash.
    def _parse_short_opt(self, arg, stream):

        # Do we have an option of the form -n=value?
        if "=" in arg:
            self._parse_equals_opt("-", arg)
            return

        # We examine each character individually to support condensed options
        # with trailing arguments: -abc foo bar. If we don't recognise the
        # character as a registered option name, we check for an automatic
        # -h or -v flag before exiting.
        for char in arg:
            option = self.options.get(char)
            if option is None:
                if char == "h" and self.helptext:
                    self.exit_help()
                elif char == "v" and self.version:
                    self.exit_version()
                else:
                    exit_error("-%s is not a recognised option" % char)

            option.found = True
            if option.type == "bool":
                option.values.append(True)
            elif stream.has_next():
                option.try_set(stream.next())
            else:
                exit_error("missing argument for -%s" % char)
