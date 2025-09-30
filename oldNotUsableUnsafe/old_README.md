# pico-something
Experimenting with pico and computer communication for a semi-functional interface setup. Not for public use yet... still working on this, it's really fun lol.

So far I've learned how to
1. use circuitpython's hid libraries on pico to act as a usb keyboard and input commands into windows
2. write powershell scripts and then use the https://github.com/thisismyrobot/loaduck tool to convert them into rubber ducky text files. I strip text them these and copy the commands into my circuitpython code
3. I've learned that using circuitpython on pico for usb rubber duckies helps to make builds more dynamic. for example, I can control GPIO output AND enter commands with hid at the same time
4. From the ducky text files that the loaduck tool generates, I've learned how to hide powershell windows and enter commands with the pico behind the scenes
5. These minimal commands can download and execute .exe files from my github
6. I've learned to write python gui programs that I can convert into .exe files with pyinstaller

LLMs have guided me through the whole process, it's been a learning experience.
Again, this is a work in progress. Like, the whole repo is completely and totally unfinished.
