WRAPPED_SINGLE_QUOTE = '\"\'\"'
WRAPPED_DOUBLE_QUOTE = "\'\"\'"
XPATH_START = '//*[text()=concat('


class XpathConcatBuildTest(unittest.TestCase):
    def test_build_xpath_concat_normal(self):
        """Given a string with no escape characters
        When I build a concat xpath
        Then the xpath string is correctly built
        """
        result = _build_xpath_concat('No quotation marks.')
        expected = "{}'No quotation marks.', \"\")]".format(XPATH_START)
        self.assertEqual(result, expected)

    def test_build_xpath_concat_double_quote(self):
        """Given a string with double quotes
        When I build a concat xpath
        Then the xpath string is correctly built
        """
        result = _build_xpath_concat('Denis \"Snake\" Bélanger')
        expected = "{}'Denis ',{},'Snake',{},' Bélanger', \"\")]".format(
            XPATH_START, WRAPPED_DOUBLE_QUOTE, WRAPPED_DOUBLE_QUOTE,
        )
        self.assertEqual(result, expected)

    def test_build_xpath_concat_single_quote(self):
        """Given a string with single quotes
        When I build a concat xpath
        Then the xpath string is correctly built
        """
        result = _build_xpath_concat('Text with a single \' quotation mark.')
        expected = "{}\"Text with a single \",{},\"quotation mark.\", \"\")]".format(
            XPATH_START, WRAPPED_SINGLE_QUOTE,
        )
        self.assertEqual(result, expected)

    def test_build_xpath_concat_multiple_types(self):
        """Given a string with double quotes and single quotes
        When I build a concat xpath
        Then the xpath string is correctly built
        """
        result = _build_xpath_concat('Text with a single \' quotation mark and double " quotation mark.')
        expected = "{}\"Text with a single \",{},\" quotation mark and double \",{},\' quotation mark.\', \"\")]".format(
            XPATH_START, WRAPPED_SINGLE_QUOTE, WRAPPED_DOUBLE_QUOTE,
        )
        self.assertEqual(result, expected)

    def test_build_xpath_concat_nested(self):
        """Given a string with double quotes around a single quote
        When I build a concat xpath
        Then the xpath string is correctly built
        """
        result = _build_xpath_concat('A "real ol\' mess" of text.')
        expected = "{}\'A \',{},\"real ol\",{},\" mess\",{},\' of text.\', \"\")]".format(
            XPATH_START, WRAPPED_DOUBLE_QUOTE, WRAPPED_SINGLE_QUOTE, WRAPPED_DOUBLE_QUOTE,
        )
        self.assertEqual(result, expected)
