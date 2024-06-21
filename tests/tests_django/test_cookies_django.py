# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import time


def test_cookies_extra_parameters(browser):
    """Cookie can be created with extra parameters."""
    timestamp = int(time.time() + 120)
    browser.cookies.add({"sha": "zam"}, expires=timestamp)
    cookie = browser._browser.cookies["sha"]
    assert timestamp == cookie["expires"]
