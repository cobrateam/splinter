# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class StatusCode:
    def __init__(self, status_code: int, reason: str) -> None:
        #: A message for the response (example: Success)
        self.reason = reason
        #: Code of the response (example: 200)
        self.code = status_code

    def __eq__(self, other) -> bool:
        return self.code == other

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"{self.code} - {self.reason}"

    def is_success(self) -> bool:
        """
        Returns:
            bool: True if the response was succeed, otherwise, returns False.
        """
        return self.code < 400
