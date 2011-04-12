import optparse
import unittest

import nose.plugins


class OptionProcessingTests(unittest.TestCase):

    def test_enable_plugin(self):
        class NamedPlugin(nose.plugins.Plugin):
            name = "jim-bob"
        def parse_options(env, args_in):
            plugin = NamedPlugin()
            parser = optparse.OptionParser()
            plugin.options(parser, env)
            options, args = parser.parse_args(args_in)
            return options
        options = parse_options({}, [])
        assert not options.enable_plugin_jim_bob, \
               "Plugin should not be enabled"
        options = parse_options({"NOSE_WITH_JIM_BOB": "1"}, [])
        assert options.enable_plugin_jim_bob, \
               "Plugin should be enabled"
        options = parse_options({}, ["--with-jim-bob"])
        assert options.enable_plugin_jim_bob, \
               "Plugin should be enabled"
        options = parse_options({"NOSE_WITH_JIM_BOB": "1"}, ["--with-jim-bob"])
        assert options.enable_plugin_jim_bob, \
               "Plugin should be enabled"


if __name__ == '__main__':
    unittest.main()
