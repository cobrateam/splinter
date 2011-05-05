    >>> from optparse import OptionParser
    >>> import os
    >>> from cStringIO import StringIO

    >>> import nose.config

All commandline options to fall back to values configured in
configuration files.  The configuration lives in a single section
("nosetests") in each configuration file.

    >>> support = os.path.join(os.path.dirname(__file__), "support",
    ...                        "config_defaults")

    >>> def error(msg):
    ...     print "error: %s" % msg

    >>> def get_parser():
    ...     parser = OptionParser()
    ...     parser.add_option(
    ...         "-v", "--verbose",
    ...         action="count", dest="verbosity",
    ...         default=1)
    ...     parser.add_option(
    ...         "--verbosity", action="store", dest="verbosity",
    ...         type="int")
    ...     return nose.config.ConfiguredDefaultsOptionParser(parser,
    ...                                                       "nosetests",
    ...                                                       error)

    >>> def parse(args, config_files):
    ...     argv = ["nosetests"] + list(args)
    ...     return get_parser().parseArgsAndConfigFiles(argv, config_files)


Options on the command line combine with the defaults from the config
files and the options' own defaults (here, -v adds 1 to verbosity of 3
from a.cfg).  Config file defaults take precedence over options'
defaults.

    >>> options, args = parse([], [])
    >>> options.verbosity
    1
    >>> options, args = parse([], os.path.join(support, "a.cfg"))
    >>> options.verbosity
    3
    >>> options, args = parse(["-v"], os.path.join(support, "a.cfg"))
    >>> options.verbosity
    4

Command line arguments take precedence

    >>> options, args = parse(["--verbosity=7"], os.path.join(support, "a.cfg"))
    >>> options.verbosity
    7

Where options appear in several config files, the last config file wins

    >>> files = [os.path.join(support, "b.cfg"), os.path.join(support, "a.cfg")]
    >>> options, args = parse([], files)
    >>> options.verbosity
    3


Invalid values should cause an error specifically about configuration
files (not about a commandline option)

    >>> options, arguments = parse([], StringIO("""\
    ... [nosetests]
    ... verbosity = spam
    ... """))
    error: Error reading config file '<???>': option 'verbosity': invalid integer value: 'spam'

Unrecognised option in nosetests config section

    >>> options, args = parse([], StringIO("[nosetests]\nspam=eggs\n"))
    error: Error reading config file '<???>': no such option 'spam'

If there were multiple config files, the error message tells us which
file contains the bad option name or value

    >>> options, args = parse([], [os.path.join(support, "a.cfg"),
    ...                            os.path.join(support, "invalid_value.cfg"),
    ...                            os.path.join(support, "b.cfg")])
    ... # doctest: +ELLIPSIS
    error: Error reading config file '...invalid_value.cfg': option 'verbosity': invalid integer value: 'spam'


Invalid config files

(file-like object)

    >>> options, args = parse([], StringIO("spam"))
    error: Error reading config file '<???>': File contains no section headers.
    file: <???>, line: 1
    'spam'

(filename)

    >>> options, args = parse([], os.path.join(support, "invalid.cfg"))
    ... # doctest: +ELLIPSIS
    error: Error reading config file '...invalid.cfg': File contains no section headers.
    file: ...invalid.cfg, line: 1
    'spam\n'

(filenames, length == 1)

    >>> options, args = parse([], [os.path.join(support, "invalid.cfg")])
    ... # doctest: +ELLIPSIS
    error: Error reading config file '...invalid.cfg': File contains no section headers.
    file: ...invalid.cfg, line: 1
    'spam\n'

(filenames, length > 1)

If there were multiple config files, the error message tells us which
file is bad

    >>> options, args = parse([], [os.path.join(support, "a.cfg"),
    ...                            os.path.join(support, "invalid.cfg"),
    ...                            os.path.join(support, "b.cfg")])
    ... # doctest: +ELLIPSIS
    error: Error reading config file '...invalid.cfg': File contains no section headers.
    file: ...invalid.cfg, line: 1
    'spam\n'


Missing config files don't deserve an error or warning

(filename)

    >>> options, args = parse([], os.path.join(support, "nonexistent.cfg"))
    >>> print options.__dict__
    {'verbosity': 1}

(filenames)

    >>> options, args = parse([], [os.path.join(support, "nonexistent.cfg")])
    >>> print options.__dict__
    {'verbosity': 1}


The same goes for missing config file section ("nosetests")

    >>> options, args = parse([], StringIO("[spam]\nfoo=bar\n"))
    >>> print options.__dict__
    {'verbosity': 1}
