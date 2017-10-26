# gimbal-controller
<h1>Gimbal controller</h1>

I wrote this script with the purpouse to control a Gimbal mounting a SimbleBGC controller.
For example, you can type a sequence of commands to turining on/off motors, rotate the camera on the three axes, play music with the internal beeper (and so on) without having to use the GUI.

Communications rely on serial protocol.
I already defined a set of default commands that you can use for testing; you can refer to the official Serial API documentation (https://www.basecamelectronics.com/serialapi/) to add new commands and create your custom scripts.

