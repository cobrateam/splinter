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

	wget http://goo.gl/PJUZfa -O selenium-server.jar
	java -jar selenium-server.jar > /dev/null 2>&1 &
	sleep 1
fi

if [ "${DRIVER}" = "tests/test_webdriver_firefox.py" ]; then
    sleep 1

    wget https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
    mkdir geckodriver
    tar -xzf geckodriver-v0.11.1-linux64.tar.gz -C geckodriver
    export PATH=$PATH:$PWD/geckodriver

    curl "https://download.mozilla.org/?product=firefox-latest&lang=en-US&os=linux64" -L > firefox.tbz2
    bzip2 -dc firefox.tbz2 | tar xvf -
    mv ./firefox $HOME
    export PATH=$HOME/firefox:$PATH
    echo "envs"
    echo $PATH
    echo "envs"
fi

if [ "${DRIVER}" = "tests/test_webdriver_chrome.py" ]; then
    sleep 1

    FILE=`mktemp`; wget "http://chromedriver.storage.googleapis.com/2.20/chromedriver_linux64.zip" -qO $FILE && unzip $FILE chromedriver -d ~; rm $FILE; chmod 777 ~/chromedriver;
    export PATH=$HOME:$PATH
fi
