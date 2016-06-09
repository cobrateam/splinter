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
    wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/46.0.1/linux-x86_64/en-US/firefox-46.0.1.tar.bz2 -O lib/firefox.tar.bz2
    tar jxf lib/firefox.tar.bz2 -C lib/firefox 
fi

if [ "${DRIVER}" = "tests/test_webdriver_chrome.py" ]; then
    sudo apt-get install -y python-software-properties
    sudo apt-add-repository "deb http://dl.google.com/linux/chrome/deb/ stable main"
    sudo sed -i s/deb-src.*google.*//g /etc/apt/sources.list
    wget -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo apt-get update -qq
    sudo apt-get install -y google-chrome-stable

    sudo chmod 1777 /dev/shm
    
    FILE=`mktemp`; wget "http://chromedriver.storage.googleapis.com/2.20/chromedriver_linux64.zip" -qO $FILE && unzip $FILE chromedriver -d ~; rm $FILE; chmod 777 ~/chromedriver;
    
    export PATH=$HOME:$PATH
fi
