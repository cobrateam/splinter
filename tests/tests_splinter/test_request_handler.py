# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from splinter.request_handler.status_code import StatusCode


@pytest.fixture()
def valid_status_code():
    return StatusCode(200, "OK")


def test_should_receive_an_url_and_get_a_success_response(valid_status_code):
    assert valid_status_code.is_success()


def test_should_compare_app_index_with_404_and_get_false(valid_status_code):
    assert valid_status_code != 404
