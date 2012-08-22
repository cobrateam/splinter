# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class PopupWindowsTest(object):

    def test_can_work_on_popups(self):
        ''' Can work on pop-up windows and switch back to the parent '''
        parent_window = self.browser.current_window # Save the parent window
        self.browser.find_by_id("open-popup").first.click()

        for window in self.browser.windows:
            self.browser.switch_to_window(window) # Switch to a different window (the pop-up)
            # Check if this is the one we want by comparing the title
            if self.browser.title == "Pop-up Window":
                break
            # Most of the times there are only two windows - the parent and the pop-up
            # In this case the following condition also does the trick
            # if window != browser.parent_window:
            #     break

        value = self.browser.find_by_tag('h1').first.value
        self.assertEqual(value, 'Pop-up Example Header') # Proves we can interact with the popup
        self.browser.find_by_id("close-popup").first.click()

        self.browser.switch_to_window(parent_window) # Switch to the main window again
        value = self.browser.find_by_tag('h1').first.value
        self.assertEqual(value, 'Example Header') # Proves we can interact with the parent
