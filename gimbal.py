#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gimbal.py
#
#  Copyright 2017 Matteo D'Agord <matteo.dagord@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# WARNING:
# the script must be execute as superuser in order to access USB port!

import serial
import time
import array
import sys


def to_hex(text_string):
    return str(''.join(map(lambda c:'\\x%02x'%c, map(ord, text_string))))


def parse_results():
    results = {}
    ser.read()

    command_id = ser.read().encode("hex")
    results['command_id'] = int(command_id, 16)

    data_size = ser.read().encode("hex")
    results['data_size'] = data_size
    data_size_converted = int(data_size, 16)

    data = ser.read(data_size_converted)
    results['data'] = data

    body_checksum = ser.read().encode("hex")
    results['body_checksum'] = body_checksum

    decoded_data = array.array("b", data)
    results['decoded_data'] = decoded_data
    return results


def send_command(command):
    beginning_hex = '\x3E'
    command_id_hex = chr(command.id)

    # show command id
    print "Command id: %s" % command.id

    # send beginning characher
    ser.write(beginning_hex)
    # send command id
    ser.write(chr(command.id))

    # check if command has data
    if command.data:
        # calculate and send data array length
        data_length = len(command.data)
        data_length_hex = chr(data_length)
        ser.write(data_length_hex)

        # calculate and send header checksum
        header_checksum = command.id + data_length
        header_checksum_hex = chr(header_checksum % 256)
        ser.write(header_checksum_hex)

        data_hex = ''
        ii = 0
        body_checksum = 0
        # parse data array
        while ii < data_length:

            if command.data_format == "dec":
                absolute_value = command.data[ii]
                if (command.data[ii] < 0):
                    command.data[ii] = 256 + command.data[ii]

                converted_parameter = chr(command.data[ii] % 256).encode("hex")

            else:
                absolute_value = int(command.data[ii], 16)
                converted_parameter = command.data[ii]

            data_hex += converted_parameter
            # increases body checksum
            body_checksum += int(absolute_value)
            ii += 1

        # send bytearray
        print "Data: %s" % data_hex
        ser.write(bytearray.fromhex(data_hex))
        print "Total bytes: %s" % body_checksum
        body_checksum_hex = chr(body_checksum % 256)

    else:
        data_length = 0
        data = 0
        data_hex = chr(data)
        body_checksum_hex = data_hex
        data_length_hex = chr(data_length)
        ser.write(data_length_hex)
        header_checksum = command.id + data_length
        header_checksum_hex = chr(header_checksum % 256)
        ser.write(header_checksum_hex)
        ser.write(data_hex)
        print "No data"

    # send body checksum
    ser.write(body_checksum_hex)

    # print composed command on screen
    command_to_send = (
                beginning_hex + command_id_hex + data_length_hex +
                header_checksum_hex + data_hex+body_checksum_hex
                )
    print "String sent: %s" % command_to_send

    if command.wait_response:
        print "----------------------"
        print "Waiting response..."
        time.sleep(command.wait_response_timeout)
        results = parse_results()
        print "Command id: s%" % results['command_id']
        print "Data s%" % results['decoded_data']

    print


class Command(object):

    def __init__(self, id, description, wait_response=False,
                 wait_response_timeout=0.5, data=None, data_format="hex"):
        self.id = id
        self.description = description
        self.wait_response = wait_response
        self.wait_response_timeout = wait_response_timeout
        self.data = data
        self.data_format = data_format

command_motors_on = Command(77, "CMD_MOTORS_ON")
command_motors_off = Command(109, "CMD_MOTORS_OFF")
command_board_info = Command(109, "CMD_BOARD_INFO", True, 0.5)
command_read_params = Command(82, "CMD_READ_PARAMS", True, 0.5, ["01"])
command_beep_sound = Command(89, "CMD_BEEP_SOUND", False, 0,
                             ["80", "00", "7D", "00", "00", "00",
                              "00", "00", "00", "00", "00", "00", "B8", "0B"])
command_control = Command(67, "CMD_CONTROL", True, 0.5,
                          [67, 67, 67, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
                          "dec")
command_execute_menu = Command(69, "CMD_EXECUTE_MENU", False, 0, [18])
command_reset = Command(114, "CMD_RESET")
command_auto_pid = Command(35, "CMD_AUTO_PID", False, 0,
                           ["01", "01", "ff", "00", "00", "00", "00", "00",
                            "00", "00", "00", "00", "00", "00", "00", "00",
                            "00", "00", "00"])

# tries to connect to device, scanning available usb ports (up to 100)
usb = 0
connected = 0
while usb < 100 and usb >= 0:
    try:
        ser = serial.serial('/dev/ttyUSB'+str(usb))  # opens serial port
        usb = -1
        connected = 1
    except:
        usb += 1

if connected == 0:
    print "Device not connected or not available!"
    print "(are you running script as superser?)"
    print
    sys.exit()
else:
    ser.baudrate = 115200
    print "Connected on: %s" % ser.name
    print "Device ready to work!"

# sends sample commands...
send_command(command_motors_on)
time.sleep(2)
send_command(command_control)
time.sleep(2)

print ""
