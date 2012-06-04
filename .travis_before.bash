#!/bin/bash

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

export DISPLAY=:99.0
sh -e /etc/init.d/xvfb start

sudo apt-get install libxss1 xdg-utils
wget https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb -O google-chrome.deb
sudo dpkg -i google-chrome.deb

wget http://chromium.googlecode.com/files/chromedriver_linux32_18.0.1022.0.zip -O chromedriver.zip
unzip chromedriver.zip
sudo cp chromedriver /usr/local/bin
sudo chmod 777 /usr/local/bin/chromedriver
