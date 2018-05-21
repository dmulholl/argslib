---
title: Home
meta title: Janus &mdash; an argument-parsing library for Python
meta description: >
    Janus is a minimalist argument-parsing library designed for building elegant command-line interfaces.
---

Janus is an argument-parsing library designed for building elegant command-line interfaces.



### Features

* Long-form boolean flags with single-character shortcuts: `--flag`, `-f`.

* Long-form string, integer, and floating-point options with
  single-character shortcuts: `--option <arg>`, `-o <arg>`.

* Condensed short-form options: `-abc <arg> <arg>`.

* Automatic `--help` and `--version` flags.

* Support for multivalued options.

* Support for git-style command interfaces with arbitrarily-nested commands.



### Installation

Install Janus from the Python package index using `pip`:

    $ pip install libjanus

Alternatively, you can incorporate the single, public-domain `janus.py` file directly into your application. Janus has no external dependencies.

Janus requires Python 3.0 or later.



### Links

* [Github Homepage](https://github.com/dmulholland/janus)
* [Sample Application](https://github.com/dmulholland/janus/blob/master/example)
* [Online Documentation](https://darrenmulholland.com/docs/janus/)



### License

This work has been placed in the public domain.
