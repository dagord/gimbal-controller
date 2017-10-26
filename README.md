# Gimbal controller

I wrote this script with the purpouse to control a Gimbal mounting a SimbleBGC controller.  
For example, you can type a sequence of commands to turn motors on/off, rotate the camera on the three axes, play music with the internal beeper (and so on) without having to use the GUI.

Communications rely on serial protocol.  
I already defined a set of default commands that you can use for testing; you must refer to the official Serial API documentation (https://www.basecamelectronics.com/serialapi/) to define new commands and create your custom scripts.

Eg.
```
my_command = Command(id, description, wait_reponse, wait_response_timeout, data, data_format)
send_command(my_command)
```
where:  
- id: command id, as specified in official documentation  
- description: short custom description  
- wait_response: to be used when waiting for an answer from the Gimbal (boolean)  
- wait_response_timeout: specify a timeout for the answer (used only if wait_response is True)
- data: send optional parameters (in array format) according to the command to be executed
- data_format: "dec" or "hex"

