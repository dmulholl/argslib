# ------------------------------------------------------------------------------
# Janus: a minimalist argument-parsing library.
# ------------------------------------------------------------------------------

import sys


# Library version number.
__version__ = "1.3.0"


# Print a message to stderr and exit with a non-zero error code.
def exit_error(msg):
    sys.exit("Error: %s." % msg)


# Deprecated exception name. Will be removed in v2.0.
class Error(Exception):
    pass


# Exception raised when an invalid API call is attempted. (Invalid user input
# does not raise an exception; instead the application exits with an error
# message.)
class ArgParserError(Error):
    pass


# Internal class for storing option data. Option type is one of 'bool',
# 'string', 'int', or 'float'.
class Option:

    def __init__(self, opt_type):
        self.type = opt_type
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

    def next(self):
        self.index += 1
        return self.args[self.index - 1]

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
        self.helptext = helptext

        # Application version.
        self.version = version

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
            for name, opt in sorted(self.options.items()):
                lines.append("  %s: (%r) %s" % (name, opt.fallback, opt.values))
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
        helptext = self.helptext.strip() if self.helptext else ""
        sys.stdout.write(helptext + "\n")
        sys.exit()

    # Print the parser's version string and exit.
    def exit_version(self):
        version = self.version.strip() if self.version else ""
        sys.stdout.write(version + "\n")
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

    # Returns the number of times the specified option has been found.
    def count(self, name):
        option = self.options.get(name)
        if option:
            return len(option.values)
        else:
            raise ArgParserError("'%s' is not a registered option" % name)

    # Returns true if the specified option was found while parsing.
    def found(self, name):
        return self.count(name) > 0

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

    # Deprecated. Will be removed in v2.0.
    def len_list(self, name):
        return self.count(name)

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
        is_first_arg = True

        while stream.has_next():
            arg = stream.next()

            if arg == "--":
                while stream.has_next():
                    self.arguments.append(stream.next())

            elif arg.startswith("--"):
                if "=" in arg:
                    self._handle_equals_opt("--", arg[2:])
                else:
                    self._handle_long_opt(arg[2:], stream)

            elif arg.startswith("-"):
                if arg == '-' or arg[1].isdigit():
                    self.arguments.append(arg)
                elif "=" in arg:
                    self._handle_equals_opt("-", arg[1:])
                else:
                    self._handle_short_opt(arg[1:], stream)

            elif is_first_arg and arg in self.commands:
                self.command = arg
                cmd_parser = self.commands[arg]
                cmd_parser._parse_stream(stream)
                cmd_parser.callback(cmd_parser)

            elif is_first_arg and arg == "help":
                if stream.has_next():
                    name = stream.next()
                    if name in self.commands:
                        self.commands[name].exit_help()
                    else:
                        exit_error("'%s' is not a recognised command" % name)
                else:
                    exit_error("the help command requires an argument")

            else:
                self.arguments.append(arg)

            is_first_arg = False

    # Parse an option of the form --name=value or -n=value.
    def _handle_equals_opt(self, prefix, arg):
        name, value = arg.split("=", maxsplit=1)
        option = self.options.get(name)

        if option is None:
            exit_error("%s%s is not a recognised option" % (prefix, name))
        elif option.type == "bool":
            exit_error("invalid format for boolean flag %s%s" % (prefix, name))
        elif value == "":
            exit_error("missing argument for %s%s" % (prefix, name))

        option.try_set(value)

    # Parse a long-form option, i.e. an option beginning with a double dash.
    def _handle_long_opt(self, arg, stream):
        if arg in self.options:
            option = self.options[arg]
            if option.type == "bool":
                option.values.append(True)
            elif stream.has_next():
                option.try_set(stream.next())
            else:
                exit_error("missing argument for --%s" % arg)
        elif arg == "help" and self.helptext is not None:
            self.exit_help()
        elif arg == "version" and self.version is not None:
            self.exit_version()
        else:
            exit_error("--%s is not a recognised option" % arg)

    # Parse a short-form option, i.e. an option beginning with a single dash.
    def _handle_short_opt(self, arg, stream):
        for char in arg:
            option = self.options.get(char)
            if option is None:
                if char == "h" and self.helptext:
                    self.exit_help()
                elif char == "v" and self.version:
                    self.exit_version()
                else:
                    exit_error("-%s is not a recognised option" % char)

            if option.type == "bool":
                option.values.append(True)
            elif stream.has_next():
                option.try_set(stream.next())
            else:
                exit_error("missing argument for -%s" % char)
