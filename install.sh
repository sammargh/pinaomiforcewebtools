#!/bin/bash

ETH0="192.168.0.1/24" # ETH0 ip on rpi to communicate with DIMM
WIFI_AP="accesspoint" # WIFI AP name
WIFI_PASS="password"  # WIFI AP password
WIFI_COUNTRY="US"     # Country for WIFI see https://en.wikipedia.org/wiki/ISO_3166-1 for Alpha 2 code
LCD_BOARD=1           # 1 for yes 0 for no
NEW_LCD_BOARD=0       # Is this a newer or older with LCD board? 1 for 
                      # newer-style, 0 for older-style that cannot change 
                      # background color
NEW_LCD_COLOR=(0,0,1) # (Red, Green, Blue) set to BLUE, can only use 1 or 0

echo "Setting up raspbian environment for static ethernet and wifi"

# Clear out exit 0 on rc.local temporarily
sed -i -e "s/exit 0//" /etc/rc.local

mkdir /home/pi/roms
cp -r /boot/pinaomiforcewebtools-master/naomiweb /home/pi/
cp -r /boot/pinaomiforcewebtools-master/piforcetools /home/pi/

# Config file pre-flight
mkdir /home/pi/tmp-dimm
cp /boot/pinaomiforcewebtools-master/conf/* /home/pi/tmp-dimm
sed -i -e "s:^static ip_address=:static ip_address=${ETH0}:" /home/pi/tmp-dimm/dhcpcd.conf
sed -i -e "s/accessid/${WIFI_AP}/" /home/pi/tmp-dimm/wpa_supplicant.conf
sed -i -e "s/password/${WIFI_PASS}/" /home/pi/tmp-dimm/wpa_supplicant.conf
sed -i -e "s/US/${WIFI_COUNTRY}/" /home/pi/tmp-dimm/wpa_supplicant.conf

# Config file placement
cp /home/pi/tmp-dimm/dhcpcd.conf /etc/dhcpcd.conf
cp /home/pi/tmp-dimm/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf 
echo "cd /home/pi/naomiweb && python3 /home/pi/naomiweb/site.py &" >> /etc/rc.local

if [ $LCD_BOARD -eq 1 ]; then
	echo "python3 /home/pi/piforcetools/piforcetools.py &" >> /etc/rc.local
	cp -r /boot/pinaomiforcewebtools-master/piforcetools /home/pi/
fi

# Fix GPIO on rpi /boot/config.txt
mount -o remount,rw /boot
sed -i -e "s/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/" /boot/config.txt

# Set SSH to load on boot
systemctl enable ssh

# Fix up LCD screen on rpi2 piforcetools
if [ $NEW_LCD_BOARD -eq 1 ]; then
	sed -i -e "s/# lcd.set_color(LCD.BLUE)/lcd.set_color(${NEW_LCD_COLOR})/" /home/pi/piforcetools/piforcetools.py
fi

echo "Software has been loaded! Rebooting twice in 5 seconds!"
sleep 5

# Fix rc.local and prep for postinstall
echo "/boot/pinaomiforcewebtools-master/postinstall.sh" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local
reboot
