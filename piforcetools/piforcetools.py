#!/usr/bin/python
# Written by TravistyOJ (AKA Capaneus)

import os, collections, signal, sys, subprocess, socket
import triforcetools
import Adafruit_CharLCD as LCD
import netifaces
from time import sleep

ips = ["192.168.0.2", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5"] # Add or remove as many endpoints as you want
rom_dir = "/home/pi/roms/"  # Set absolute path of rom files ending with trailing /
commands = ["Ping Netdimm", "Change Target", "Display WIFI IP"]
categories = ["atomiswave", "naomi", "naomi2", "naomi_special", "commands"] # Add or remove categories that are unused
category_index = len(categories) - 1
chosen_category = 0
pressedButtons = []
curr_ip = 0

iterator = iter(commands)
selection = ""
mode = "commands"
previous = None
down = None
topofmenu = None

# Determine hardware revision and initialize LCD
revision = "unknown"
cpuinfo = open("/proc/cpuinfo", "r")
for line in cpuinfo:
    item = line.split(':', 1)
    if item[0].strip() == "Revision":
        revision = item[1].strip()
if revision.startswith('a'):
    lcd = LCD.Adafruit_CharLCDPlate(busnum = 1)
else:
    lcd = LCD.Adafruit_CharLCDPlate()
# lcd.begin(16, 2)

# SET YOUR DESIRED POWER ON LCD COLOR HERE.  'lcd.COLORNAME' where COLORNAME = RED, YELLOW, GREEN, TEAL, BLUE, VIOLET
# lcd.set_color(LCD.BLUE) # REMOVE COMMENT IF USING NEWER RGB LCD
lcd.message(" Piforce Tools\n    Ver. 1.6")
sleep(2)
lcd.clear()
lcd.message("Starting up...")

# Define a signal handler to turn off LCD before shutting down
def handler(signum = None, frame = None):
    lcd = LCD.Adafruit_CharLCDPlate()
    lcd.clear()
    lcd.stop()
    sys.exit(0)
signal.signal(signal.SIGTERM , handler)

def categorymessage(messagestring):
    lcd.message(messagestring)
    sleep(1)
    lcd.clear()

def populatemenu():
    global iterator
    global selection
    global mode
    global previous
    global down
    global topofmenu
    lcd.clear()
    if categories[chosen_category] == "atomiswave":
        if not down:
            categorymessage("Atomiswave")
        iterator  = iter(collections.OrderedDict(sorted(atomiswave.items(), key=lambda t: t[0])))
        mode = "atomiswave"
    elif categories[chosen_category] == "atomiswave_special":
        if not down:
            categorymessage("Atomiswave\n Special")
        iterator  = iter(collections.OrderedDict(sorted(atomiswave_special.items(), key=lambda t: t[0])))
        mode = "atomiswave_special"
    elif categories[chosen_category] == "naomi":
        if not down:
            categorymessage("Naomi")
        iterator  = iter(collections.OrderedDict(sorted(naomi.items(), key=lambda t: t[0])))
        mode = "naomi"
    elif categories[chosen_category] == "naomi2":
        if not down:
            categorymessage("Naomi 2")
        iterator  = iter(collections.OrderedDict(sorted(naomi2.items(), key=lambda t: t[0])))
        mode = "naomi2"
    elif categories[chosen_category] == "naomi_vertical":
        if not down:
            categorymessage("Naomi Vertical")
        iterator  = iter(collections.OrderedDict(sorted(naomi_vertical.items(), key=lambda t: t[0])))
        mode = "naomi_vertical"
    elif categories[chosen_category] == "naomi_special":
        if not down:
            categorymessage("Naomi Special")
        iterator  = iter(collections.OrderedDict(sorted(naomi_special.items(), key=lambda t: t[0])))
        mode = "naomi_special"
    elif categories[chosen_category] == "naomi_gun":
        if not down:
            categorymessage("Naomi Gun")
        iterator  = iter(collections.OrderedDict(sorted(naomi_gun.items(), key=lambda t: t[0])))
        mode = "naomi_gun"
    elif categories[chosen_category] == "chihiro":
        if not down:
            categorymessage("Chihiro")
        iterator  = iter(collections.OrderedDict(sorted(naomi_gun.items(), key=lambda t: t[0])))
        mode = "chihiro"
    elif categories[chosen_category] == "triforce":
        if not down:
            categorymessage("Triforce")
        iterator  = iter(collections.OrderedDict(sorted(naomi_gun.items(), key=lambda t: t[0])))
        mode = "triforce"
    elif categories[chosen_category] == "commands":
        if not down:
            categorymessage("Commands")
        iterator  = iter(commands)
        mode = "commands"
    if down:
        down = None
    topofmenu = True
    selection = next(iterator)
    lcd.message(selection)

# Function to put iterator at the top of the list so we may navigagte up in the menu
def resetiterator():
    global iterator
    if categories[chosen_category] == "atomiswave":
        iterator  = iter(collections.OrderedDict(sorted(atomiswave.items(), key=lambda t: t[0])))
    elif categories[chosen_category] == "atomiswave_special":
        iterator  = iter(collections.OrderedDict(sorted(atomiswave_special.items(), key=lambda t: t[0])))
    elif categories[chosen_category] == "naomi":
        iterator  = iter(collections.OrderedDict(sorted(naomi.items(), key=lambda t: t[0])))
    elif categories[chosen_category] == "naomi2":
        iterator  = iter(collections.OrderedDict(sorted(naomi2.items(), key=lambda t: t[0])))
    elif categories[chosen_category] == "naomi_vertical":
        iterator  = iter(collections.OrderedDict(sorted(naomi_vertical.items(), key=lambda t: t[0])))
    elif categories[chosen_category] == "naomi_special":
        iterator  = iter(collections.OrderedDict(sorted(naomi_special.items(), key=lambda t: t[0])))
    elif categories[chosen_category] == "naomi_gun":
        iterator  = iter(collections.OrderedDict(sorted(naomi_gun.items(), key=lambda t: t[0])))
    elif categories[chosen_category] == "chihiro":
        iterator  = iter(collections.OrderedDict(sorted(chihiro.items(), key=lambda t: t[0])))
    elif categories[chosen_category] == "triforce":
        iterator  = iter(collections.OrderedDict(sorted(triforce.items(), key=lambda t: t[0])))
    elif categories[chosen_category] == "commands":
        iterator  = iter(commands)

def iter_islast(iterable):
    resetiterator()
    it = iter(iterable)
    prev = next(it)
    for item in it:
        yield prev, False
        prev = item
    yield prev, True


# Try to import game list script, if it fails, signal error on LCD
for category in categories:
    try:
        if category == "atomiswave":
            from gamelist import atomiswave as templist
        elif category == "atomiswave_special":
            from gamelist import atomiswave_special as templist
        elif category == "naomi":
            from gamelist import naomi as templist
        elif category == "naomi2":
            from gamelist import naomi2 as templist
        elif category == "naomi_vertical":
            from gamelist import naomi_vertical as templist
        elif category == "naomi_special":
            from gamelist import naomi_special as templist
        elif category == 'naomi_gun':
            from gamelist import naomi_gun as templist
        elif category == 'chihiro':
            from gamelist import chihiro as templist
        elif category == 'triforce':
            from gamelist import triforce as templist
    except (SyntaxError, ImportError) as e:
        lcd.clear()
        lcd.message("Game List Error!\n  Check Syntax")
        sleep(5)
        templist = {}

    # Purge game dictionary of game files that can't be found
    if category != "commands":
        missing_games = []
        for key, value in templist.items():
            if not os.path.isfile(rom_dir+value):
                missing_games.append(key)
        for missing_game in missing_games:
            del templist[missing_game]

    # Category has been cleaned up, store into category name
    if category == "atomiswave":
        atomiswave = templist
    elif category == "atomiswave_special":
        atomiswave_special = templist
    elif category == "naomi":
        naomi = templist
    elif category == "naomi2":
        naomi2 = templist
    elif category == "naomi_vertical":
        naomi_vertical = templist
    elif category == "naomi_special":
        naomi_special = templist
    elif category == 'naomi_gun':
        naomi_gun = templist
    elif category == 'chihiro':
        chihiro = templist
    elif category == 'triforce':
        triforce = templist

lcd.clear()
populatemenu()

while True:

    # Handle SELECT
    if lcd.is_pressed(LCD.SELECT):
        if LCD.SELECT not in pressedButtons:
            pressedButtons.append(LCD.SELECT)
            previous = selection
            if selection is "Change Target":
                curr_ip += 1
                if curr_ip >= len(ips):
                    curr_ip = 0
                lcd.message("\n"+ips[curr_ip])
            elif selection is "Ping Netdimm":
                lcd.clear()
                lcd.message("Pinging\n"+ips[curr_ip])
                response = os.system("ping -c 1 "+ips[curr_ip])
                lcd.clear()
                if response == 0:
                    lcd.message("SUCCESS!")
                else:
                    lcd.message("Netdimm is\nunreachable!")
                sleep(2)
                lcd.clear()
                lcd.message(selection)
            elif selection is "Display WIFI IP":
                lcd.clear()
                lcd.message(netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr'])
                sleep(5)
                lcd.clear()
                lcd.message(selection)
            else:
                lcd.clear()
                lcd.message("Connecting...")

                try:
                    triforcetools.connect(ips[curr_ip], 10703)
                except:
                    lcd.clear()
                    lcd.message("Error:\nConnect Failed")
                    sleep(1)
                    lcd.clear()
                    lcd.message(selection)
                    continue

                lcd.clear()
                lcd.message("Sending...")
#                lcd.set_Cursor(10, 0)
#                lcd.ToggleBlink()

                triforcetools.HOST_SetMode(0, 1)
                triforcetools.SECURITY_SetKeycode("\x00" * 8)
                if categories[chosen_category] == "atomiswave":
                    triforcetools.DIMM_UploadFile(rom_dir+atomiswave[selection])
                elif categories[chosen_category] == "atomiswave_special":
                    triforcetools.DIMM_UploadFile(rom_dir+atomiswave_special[selection])
                elif categories[chosen_category] == "naomi":
                    triforcetools.DIMM_UploadFile(rom_dir+naomi[selection])
                elif categories[chosen_category] == "naomi2":
                    triforcetools.DIMM_UploadFile(rom_dir+naomi2[selection])
                elif categories[chosen_category] == "naomi_vertical":
                    triforcetools.DIMM_UploadFile(rom_dir+naomi_vertical[selection])
                elif categories[chosen_category] == "naomi_gun":
                    triforcetools.DIMM_UploadFile(rom_dir+naomi_gun[selection])
                elif categories[chosen_category] == "naomi_special":
                    triforcetools.DIMM_UploadFile(rom_dir+naomi_special[selection])
                elif categories[chosen_category] == "chihiro":
                    triforcetools.DIMM_UploadFile(rom_dir+chihiro[selection])
                elif categories[chosen_category] == "triforce":
                    triforcetools.DIMM_UploadFile(rom_dir+triforce[selection])
                triforcetools.HOST_Restart()
                triforcetools.TIME_SetLimit(10*60*1000)
                triforcetools.disconnect()

#                lcd.ToggleBlink()
                lcd.clear()
                lcd.message("Transfer\nComplete!")
                sleep(5)
                lcd.clear()
                lcd.message(selection)
    elif LCD.SELECT in pressedButtons:
        pressedButtons.remove(LCD.SELECT)

    # Handle LEFT
    if lcd.is_pressed(LCD.LEFT):
        if LCD.LEFT not in pressedButtons:
            pressedButtons.append(LCD.LEFT)
            if chosen_category == 0:
                chosen_category = category_index
            else:
                chosen_category = chosen_category - 1
            populatemenu()
    elif LCD.LEFT in pressedButtons:
        pressedButtons.remove(LCD.LEFT)

    # Handle RIGHT
    if lcd.is_pressed(LCD.RIGHT):
        if LCD.RIGHT not in pressedButtons:
            pressedButtons.append(LCD.RIGHT)
            if chosen_category == category_index:
                chosen_category = 0
            else:
                chosen_category = chosen_category + 1
            populatemenu()
    elif LCD.RIGHT in pressedButtons:
        pressedButtons.remove(LCD.RIGHT)

    # Handle UP
    if lcd.is_pressed(LCD.UP):
        if LCD.UP not in pressedButtons:
            pressedButtons.append(LCD.UP)
            currentitem = selection
            for n, islast in iter_islast(iterator):
                if islast:
                    lastitem = n
                else:
                    currentitem = n
            resetiterator()
            needle = next(iterator)
            if selection == needle:
                topofmenu = True
            if topofmenu:
                selection = lastitem
                previous = currentitem
                resetiterator()
            else:
                selection = previous
                previous = needle
                topofmenu = False
            while selection != needle and selection != previous and not topofmenu:
                previous = needle
                try:
                    needle = next(iterator)
                except StopIteration:
                    break
            topofmenu = False
            lcd.clear()
            lcd.message(selection)
    elif LCD.UP in pressedButtons:
        pressedButtons.remove(LCD.UP)

    # Handle DOWN
    if lcd.is_pressed(LCD.DOWN):
        if LCD.DOWN not in pressedButtons:
            pressedButtons.append(LCD.DOWN)
            previous = selection
            topofmenu = False
            try:
                selection = next(iterator)
            except StopIteration:
                down = True
                populatemenu()
            lcd.clear()
            lcd.message(selection)
    elif LCD.DOWN in pressedButtons:
        pressedButtons.remove(LCD.DOWN)
