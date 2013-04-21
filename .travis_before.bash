#!/bin/bash

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

export DISPLAY=:99.0
sh -e /etc/init.d/xvfb start

sudo apt-get install libxss1 xdg-utils -y
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update
sudo apt-get install google-chrome-stable
wget https://chromedriver.googlecode.com/files/chromedriver_linux32_26.0.1383.0.zip -O chromedriver.zip
unzip chromedriver.zip
sudo cp chromedriver /usr/local/bin
sudo chmod 755 /usr/local/bin/chromedriver

# Remove after 4814 is resolved
# http://code.google.com/p/selenium/issues/detail?id=4814
#wget http://download.cdn.mozilla.net/pub/mozilla.org/firefox/releases/19.0/linux-i686/en-US/firefox-19.0.tar.bz2
#tar -xjf firefox-19.0.tar.bz2
#export PATH=./firefox:$PATH

wget http://selenium.googlecode.com/files/selenium-server-standalone-2.32.0.jar -O selenium-server.jar
java -jar selenium-server.jar > /dev/null &
