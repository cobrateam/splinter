# -*- coding: utf-8 -*-

# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import sys
import unittest
from six.moves.urllib import parse

from splinter import Browser
from .base import BaseBrowserTests
from .fake_webapp import EXAMPLE_APP


sys.path.append('tests/fake_django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
try:
    # Django >= 1.7 needs setup
    django.setup()
except AttributeError:
    pass


class DjangoClientDriverTest(BaseBrowserTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        components = parse.urlparse(EXAMPLE_APP)
        cls.browser = Browser('django', wait_time=0.1, client_SERVER_NAME=components.hostname,
                              client_SERVER_PORT=components.port)

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(self):
        self.browser.quit()

    def test_should_support_with_statement(self):
        with Browser('django') as internet:
            self.assertIsNotNone(internet)

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'mockfile.txt'
        )
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').click()

        html = self.browser.html
        assert 'text/plain' in html
        assert open(file_path, 'rb').read().decode('utf-8') in html

    def test_forward_to_none_page(self):
        "should not fail when trying to forward to none"
        browser = Browser('django')
        browser.visit(EXAMPLE_APP)
        browser.forward()
        self.assertEqual(EXAMPLE_APP, browser.url)
        browser.quit()

    def test_cant_switch_to_frame(self):
        "zope.testbrowser should not be able to switch to frames"
        with self.assertRaises(NotImplementedError) as cm:
            self.browser.get_iframe('frame_123')
            self.fail()

        e = cm.exception
        self.assertEqual("django doesn't support frames.", e.args[0])

    def test_simple_type(self):
        """
        zope.testbrowser won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.type('query', 'with type method')

    def test_simple_type_on_element(self):
        """
        django won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name('query').type('with type method')

    def test_slowly_typing(self):
        """
        django won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.type('query', 'with type method', slowly=True)

    def test_slowly_typing_on_element(self):
        """
        django won't support type method
        on element because it doesn't interac with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            query = self.browser.find_by_name('query')
            query.type('with type method', slowly=True)

    def test_cant_mouseover(self):
        "django should not be able to put the mouse over the element"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_css('#visible').mouse_over()

    def test_cant_mouseout(self):
        "django should not be able to mouse out of an element"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_css('#visible').mouse_out()

    def test_links_with_nested_tags_xpath(self):
        links = self.browser.find_by_xpath('//a/span[text()="first bar"]/..')
        self.assertEqual(
            len(links), 1,
            'Found not exactly one link with a span with text "BAR ONE". %s' % (
                map(lambda item: item.outer_html, links)))

    def test_finding_all_links_by_non_ascii_text(self):
        "should find links by non ascii text"
        non_ascii_encodings = {
            'pangram_pl': u'Jeżu klątw, spłódź Finom część gry hańb!',
            'pangram_ja': u'天 地 星 空',
            'pangram_ru': u'В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!',
            'pangram_eo': u'Laŭ Ludoviko Zamenhof bongustas freŝa ĉeĥa manĝaĵo kun spicoj.',
        }
        for key, text in non_ascii_encodings.items():
            link = self.browser.find_link_by_text(text)
            self.assertEqual(key, link['id'])

    def test_redirection(self):
        """
        when visiting /redirected, browser should be redirected to /redirected-location?come=get&some=true
        browser.url should be updated
        """
        self.browser.visit('{}redirected'.format(EXAMPLE_APP))
        assert 'I just been redirected to this location.' in self.browser.html
        self.assertEqual('{}redirect-location?come=get&some=true'.format(EXAMPLE_APP), self.browser.url)
