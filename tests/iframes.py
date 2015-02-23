# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class IFrameElementsTest(object):

    def test_can_work_on_iframes(self):
        """can work on iframes and switch back to the page"""
        with self.browser.get_iframe('iframemodal') as frame:
            value = frame.find_by_tag('h1').value
            self.assertEqual(value, 'IFrame Example Header')
        value = self.browser.find_by_tag('h1').value
        self.assertEqual('Example Header', value)
