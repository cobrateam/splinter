#!/bin/bash

# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

set -ev

if [ "${DRIVER}" = "tests/test_djangoclient.py" ]; then
    pip install -q Django==${DJANGO_VERSION}
fi

if [ "${DRIVER}" = "tests/test_webdriver_remote.py" ]; then
    wget http://goo.gl/PJUZfa -O selenium-server.jar
    java -jar selenium-server.jar > /dev/null 2>&1 &
    sleep 1
fi

if [ "${DRIVER}" = "tests/test_webdriver_phantomjs.py" ]; then
    git lfs pull
    tar -zxvf lib/phantomjs-2.1.1-linux-x86_64.tar.gz -C lib/phantomjs-2.1.1-linux-x86_64
    export PATH=$PWD/lib/phantomjs-2.1.1-linux-x86_64/bin:$PATH
fi

if [ "${DRIVER}" = "tests/test_webdriver_firefox.py" ]; then
    echo "Extracting firefox and setting PATH variable..."
    tar -xjf /tmp/firefox-43.0.tar.bz2 --directory /tmp
    export PATH="/tmp/firefox:$PATH"
    echo "Using firefox version `firefox --version`"
fi

if [ "${DRIVER}" = "tests/test_webdriver_chrome.py" ]; then
    FILE=`mktemp`; wget "http://chromedriver.storage.googleapis.com/2.20/chromedriver_linux64.zip" -qO $FILE && unzip $FILE chromedriver -d ~; rm $FILE; chmod 777 ~/chromedriver;
    
    export PATH=$HOME:$PATH
fi
