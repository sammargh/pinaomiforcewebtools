# pinaomiforcewebtools
pinaomiforcewebtools is a software package that is an approach of freeing piforcetools and naomiweb from needing pre-made images as well as raspbian-agnostic versioning so long as python3 is supported on the platform. This software supports a Raspberry Pi 2 with WIFI dongle and optional LCD plate or a Raspberry Pi 3.


## Getting Started
You will need the following items to use pinaomiforcewebtools:
 1. A Raspberry Pi - http://www.raspberrypi.org with WIFI capabilities
 2. A copy of the latest version of raspbian LITE - https://www.raspberrypi.org/downloads/raspbian/
 3. A SD Card
 4. A Naomi or Naomi 2
 5. A Netdimm with a zero-key security PIC installed.
 6. A crossover cable

## Installation

 1. Follow the steps to prepare your sd card with raspbian - [
https://www.raspberrypi.org/documentation/installation/installing-images/](https://www.raspberrypi.org/documentation/installation/installing-images/)
 2. Once completed download this repository via clone or download > download zip
 3. Unzip the repository to the boot folder that is mounted from the sd card so you have x:\pinaomiforcewebtools-master\
 4. Open x:\pinaomiforcewebtools-master\install.sh and modify the variables at the top to match your configuration setup see sample below for further information
 5. Put sd card into Raspberry Pi, plug into monitor and add a keyboard
 6. Power the Raspberry Pi on and once you receive a login prompt login with the default credentials (pi/raspberry)
 7. Run the command "sudo /boot/pinaomiforcewebtools-master/install.sh"
 8. The Raspberry Pi will reboot twice and the software is configured. Once completed use a SFTP client to copy roms into the roms directory.

## Sample configuration

	# CONFIGURATION SECTION
	ETH0="192.168.0.1/24" # ETH0 ip on rpi to communicate with DIMM
	WIFI_AP="mywifi" # WIFI AP name
	WIFI_PASS="super password"  # WIFI AP password
	WIFI_COUNTRY="US"     # Country for WIFI see https://en.wikipedia.org/wiki/ISO_3166-1 for Alpha 2 code
	LCD_BOARD=1           # 1 for yes 0 for no
	NEW_LCD_BOARD=0       # Is this a newer or older with LCD board? 1 for
                      	# newer-style, 0 for older-style that cannot change
                      	# background color
	NEW_LCD_COLOR=(0,0,1) # (Red, Green, Blue) set to BLUE, can only use 1 or 0
	# END CONFIGURATION SECTION
In this sample configuration my Naomi DIMM is set to 192.168.0.2 so I am setting my Raspberry Pi to 192.168.0.1 to communicate over ethernet. The /24 is necessary so please do not remove it. My wireless access point is "mywifi" with the password "super password". I live in the US (country is required for Raspberry Pi 3 users) and have an older-style LCD board on my Raspberry Pi 2 that I wish to be configured.


## Troubleshooting

After the software is installed you can use "ifconfig wlan0" from login to obtain the wireless ip for your Raspberry Pi. Once you have this you can use Filezilla or a similar client to load the games into the roms directory. Simply put the ip in your client with pi/raspberry as the login to copy roms over. Once roms are loaded reboot the Raspberry Pi and it should start functioning. You can navigate to the naomiweb interface by going to http://<wifiip> in your browser.

## Credit

Thanks to debugmode for his triforce tools script, travistyoj for his work on piforcetools and tugpoat for his work on naomiweb. Darksoft as well for the atomiswave converts and anyone I forgot.
