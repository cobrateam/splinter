#!/bin/bash

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

export DISPLAY=:99.0
sh -e /etc/init.d/xvfb start

sudo apt-get install libxss1 xdg-utils
wget https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb -O google-chrome.deb
sudo dpkg -i google-chrome.deb

wget https://chromedriver.googlecode.com/files/chromedriver_linux32_21.0.1180.4.zip -O chromedriver.zip
unzip chromedriver.zip
sudo cp chromedriver /usr/local/bin
sudo chmod 755 /usr/local/bin/chromedriver

# Remove after 4814 is resolved
# http://code.google.com/p/selenium/issues/detail?id=4814
wget http://download.cdn.mozilla.net/pub/mozilla.org/firefox/releases/16.0/linux-i686/en-US/firefox-16.0.tar.bz2
tar -xjf firefox-16.0.tar.bz2
export PATH=./firefox:$PATH

wget http://selenium.googlecode.com/files/selenium-server-standalone-2.28.0.jar -O selenium-server.jar
java -jar selenium-server.jar > /dev/null &
sleep 20
