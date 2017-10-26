# Gimbal controller

I wrote this script with the purpouse to control a Gimbal mounting a SimbleBGC controller.\n
For example, you can type a sequence of commands to turn motors on/off, rotate the camera on the three axes, play music with the internal beeper (and so on) without having to use the GUI.

Communications rely on serial protocol.\n
I already defined a set of default commands that you can use for testing; you must refer to the official Serial API documentation (https://www.basecamelectronics.com/serialapi/) to define new commands and create your custom scripts.

