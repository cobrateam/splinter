 #!/bin/bash
export DISPLAY=:99.0
sh -e /etc/init.d/xvfb start

wget https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb -o google-chrome.deb
sudo dpkg -i google-chrome.deb

sudo apt-get unzip
wget http://chromium.googlecode.com/files/chromedriver_linux32_18.0.1022.0.zip -O chromedriver.zip
unzip chromedriver.zip
chmod +x chromedriver
sudo cp chromedriver /usr/local/bin
sudo chmod 777 /usr/local/bin/chromedriver
