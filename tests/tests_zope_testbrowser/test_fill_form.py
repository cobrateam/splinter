# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest


def test_fill_form_missing_values(browser, app_url):
    """Missing values should raise an error."""
    browser.visit(app_url)
    with pytest.raises(LookupError):
        browser.fill_form(
            {"query": "new query", "missing_form": "doesn't exist"},
        )
