# Janus

Janus is an argument-parsing library for Python designed for building elegant command-line interfaces. Its features include:

* Long-form boolean flags with single-character shortcuts: `--flag`, `-f`.

* Long-form string, integer, and floating-point options with
  single-character shortcuts: `--option <arg>`, `-o <arg>`.

* Condensed short-form options: `-abc <arg> <arg>`.

* Automatic `--help` and `--version` flags.

* Support for multivalued options.

* Support for git-style command interfaces with arbitrarily-nested commands.

See the [documentation][docs] for details.

[docs]: http://mulholland.xyz/docs/janus/