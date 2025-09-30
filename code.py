# Copyright (c) 2025 ComputerL (@1ComputerL)
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

# this circuitpython code is meant to run on a pico but should work on any microcontroller with usb
# when connected to the typical windows computer, it opens an html file in the microcontroller's storage and displays it
# in microsoft edge on the computer

### IMPORTS ###
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import time

### OPEN HTML FILE ###
# wait for an annoying file manager window to pop up
time.sleep(12)

# create keyboard object (for entering keycodes)
kbd = Keyboard(usb_hid.devices)
# create layout object (for entering text)
layout = KeyboardLayoutUS(kbd)

# open a PowerShell window via Win+R
kbd.send(Keycode.GUI, Keycode.R)  # Win+R = Run dialog
# delay
time.sleep(1)
# (optional extra Enter if needed)
kbd.send(Keycode.ENTER)
# delay
time.sleep(1)
# enter the powershell command into the run dialouge
layout.write("powershell")
# delay
time.sleep(1)
# run the command
kbd.send(Keycode.ENTER)
# let powershell load for a few seconds
time.sleep(5)
# write the command to open 'index.html' on the circuitpython drive
layout.write("""Start-Process "msedge.exe" -ArgumentList @("--new-window","--start-fullscreen","file:///D:/index.html")""")
# delay 
time.sleep(0.5)
# enter the command
kbd.send(Keycode.ENTER)