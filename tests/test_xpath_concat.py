# -*- coding: utf-8 -*-

from splinter.driver.xpath_utils import _concat_xpath_from_str


WRAPPED_SINGLE_QUOTE = '\"\'\"'
WRAPPED_DOUBLE_QUOTE = "\'\"\'"
XPATH_START = '//*[text()=concat('


def test_build_xpath_concat_normal():
    """Given a string with no escape characters
    When I build a concat xpath
    Then the xpath string is correctly built
    """
    result = _concat_xpath_from_str('No quotation marks.')
    expected = "{}'No quotation marks.', \"\")]".format(XPATH_START)
    assert result == expected


def test_build_xpath_concat_double_quote():
    """Given a string with double quotes
    When I build a concat xpath
    Then the xpath string is correctly built
    """
    result = _concat_xpath_from_str('Denis \"Snake\" Bélanger')
    expected = "{}'Denis ',{},'Snake',{},' Bélanger', \"\")]".format(
        XPATH_START, WRAPPED_DOUBLE_QUOTE, WRAPPED_DOUBLE_QUOTE,
    )
    assert result == expected


def test_build_xpath_concat_single_quote():
    """Given a string with single quotes
    When I build a concat xpath
    Then the xpath string is correctly built
    """
    result = _concat_xpath_from_str('Text with a single \' quotation mark.')
    expected = "{}\"Text with a single \",{},\" quotation mark.\", \"\")]".format(
        XPATH_START, WRAPPED_SINGLE_QUOTE,
    )
    assert result == expected


def test_build_xpath_concat_multiple_types():
    """Given a string with double quotes and single quotes
    When I build a concat xpath
    Then the xpath string is correctly built
    """
    result = _concat_xpath_from_str('Text with a single \' quotation mark and double " quotation mark.')
    expected = "{}\"Text with a single \",{},\" quotation mark and double \",{},\' quotation mark.\', \"\")]".format(
        XPATH_START, WRAPPED_SINGLE_QUOTE, WRAPPED_DOUBLE_QUOTE,
    )
    assert result == expected


def test_build_xpath_concat_nested():
    """Given a string with double quotes around a single quote
    When I build a concat xpath
    Then the xpath string is correctly built
    """
    result = _concat_xpath_from_str('A "real ol\' mess" of text.')
    expected = "{}\'A \',{},\"real ol\",{},\" mess\",{},\' of text.\', \"\")]".format(
        XPATH_START, WRAPPED_DOUBLE_QUOTE, WRAPPED_SINGLE_QUOTE, WRAPPED_DOUBLE_QUOTE,
    )
    assert result == expected
