#!/bin/bash

# Copyright 2016 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

set -ev

if [ "${DRIVER}" = "tests/test_djangoclient.py" ]; then
  pip install -q Django==${DJANGO_VERSION}
fi

if [ "${DRIVER}" = "tests/test_webdriver_remote.py" ]; then
  sleep 1

  wget https://selenium-release.storage.googleapis.com/3.10/selenium-server-standalone-3.10.0.jar -O selenium-server.jar
	java -jar selenium-server.jar > /dev/null 2>&1 &
	sleep 1
fi

if [ "${DRIVER}" = "tests/test_webdriver_chrome.py" ] || [ "${DRIVER}" = "tests/test_webdriver.py" ]; then
    sleep 1

    FILE=`mktemp`; wget "https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip" -qO $FILE && unzip $FILE chromedriver -d ~; rm $FILE; chmod 777 ~/chromedriver;
    export PATH=$HOME:$PATH
fi

