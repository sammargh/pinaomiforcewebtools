#!/bin/bash

echo "Performing post-install now for pinaomiforcewebtools"

# General software installation necessary for functionality
apt-get update
apt-get -y upgrade
apt-get -y install python3 python3-pip python-dev
pip3 install netifaces bottle rpi.gpio adafruit-charlcd

# Cleanup
sed -i -e "s:/boot/pinaomiforcewebtools-master/postinstall.sh::" /etc/rc.local
echo "i2c-dev" >> /etc/modules
cp -r /boot/pinaomiforcewebtools-master/naomiweb /home/pi/

reboot
