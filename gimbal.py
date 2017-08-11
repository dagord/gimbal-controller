# coding=utf-8

# script must be execute as superuser in order to access USB port

import serial
import time
import array


def to_hex(text_string):
    return str(''.join(map(lambda c:'\\x%02x'%c, map(ord, text_string))))


def parse_results():
    risposta = {}
    ser.read()

    command_id = ser.read().encode("hex")
    risposta['command_id'] = int(command_id, 16)

    data_size = ser.read().encode("hex")
    risposta['data_size'] = data_size
    data_size_converted = int(data_size, 16)

    # header_checksum = ser.read().encode("hex")

    data = ser.read(data_size_converted)
    risposta['data'] = data

    body_checksum = ser.read().encode("hex")
    risposta['body_checksum'] = body_checksum

    decoded_data = array.array("b", data)
    risposta['decoded_data'] = decoded_data
    return risposta


def send_command(parameters):
    beginning_hex = '\x3E'
    command_id_hex = chr(parameters['id'])

    # send beginning characher
    ser.write(beginning_hex)
    # send command id
    ser.write(command_id_hex)

    # check if command has data
    if 'data' in parameters:
        # calculate and send data array length
        data_length = len(parameters['data'])
        data_length_hex = chr(data_length)
        ser.write(data_length_hex)

        # calculate and send header checksum
        header_checksum = parameters['id'] + data_length
        header_checksum_hex = chr(header_checksum % 256)
        ser.write(header_checksum_hex)

        data_hex = ''
        ii = 0
        body_checksum = 0
        # parse data array
        while ii < data_length:
            # converts array item to a two-digit hex number, removing initial "0x"
            valore_assoluto = parameters['data'][ii]
            if (parameters['data'][ii] < 0):
                parameters['data'][ii] = 256 + parameters['data'][ii]
            # print parameters['data'][ii]
            # parametro_convertito = format(parameters['data'][ii], '02x').replace("0x", "")
            parametro_convertito = chr(parameters['data'][ii] % 256).encode("hex")

            print parametro_convertito
            data_hex += parametro_convertito + " "
            # increases body checksum
            body_checksum += int(valore_assoluto)
            ii += 1

        # send bytearray
        ser.write(bytearray.fromhex(data_hex))
        # ser.write(data_hex)
        print "Somma dei byte: "+str(body_checksum)
        body_checksum_hex = chr(body_checksum % 256)

    else:
        data_length = 0
        data = 0
        data_hex = chr(data)
        body_checksum_hex = data_hex
        data_length_hex = chr(data_length)
        ser.write(data_length_hex)
        header_checksum = parameters['id'] + data_length
        header_checksum_hex = chr(header_checksum % 256)
        ser.write(header_checksum_hex)
        ser.write(data_hex)

    # send body checksum
    ser.write(body_checksum_hex)

    # compone e invia il comando
    comando = (
                beginning_hex + command_id_hex + data_length_hex +
                header_checksum_hex + data_hex+body_checksum_hex
                )
    # ser.write(comando)

    # visualizza a schermo la stringa raw
    # print "Invio il comando: "+to_hex(comando)

    if 'wait_response' in parameters:
        print "----------------------"
        print "Attendo la risposta..."
        time.sleep(parameters['wait_response_timeout'])
        risposta = parse_results()
        print "Command id: "+str(risposta['command_id'])
        print "Data "+str(risposta['decoded_data'])


CMD_MOTORS_ON = {}
CMD_MOTORS_ON['id'] = 77

CMD_MOTORS_OFF = {}
CMD_MOTORS_OFF['id'] = 109

CMD_BOARD_INFO = {}
CMD_BOARD_INFO['id'] = 86
CMD_BOARD_INFO['wait_response'] = True
CMD_BOARD_INFO['wait_response_timeout'] = 0.5

CMD_READ_PARAMS = {}
CMD_READ_PARAMS['id'] = 82
CMD_READ_PARAMS['data'] = ["01"]
CMD_READ_PARAMS['wait_response'] = True
CMD_READ_PARAMS['wait_response_timeout'] = 0.5

CMD_BEEP_SOUND = {}
CMD_BEEP_SOUND['id'] = 89
CMD_BEEP_SOUND['data'] = [ "80", "00", "7D", "00", "00", "00", "00", "00", "00", "00", "00", "00", "B8", "0B"]
# CMD_BEEP_SOUND['wait_response'] = True
# CMD_BEEP_SOUND['wait_response_timeout'] = 0.5

CMD_CONTROL = {}
CMD_CONTROL['id'] = 67
# CMD_CONTROL['data'] = [ "01", "00", "d8", "00", "48", "00", "00", "00", "00", "00", "00", "00", "00" ]
CMD_CONTROL['data'] = [ 128,128,128, 0,0,0,1, 0,0,0,1, 0,0,0,1 ]
# CMD_CONTROL['data_format'] = "hex"
CMD_CONTROL['wait_response'] = True
CMD_CONTROL['wait_response_timeout'] = 0.5


CMD_EXECUTE_MENU = {}
CMD_EXECUTE_MENU['id'] = 69
CMD_EXECUTE_MENU['data'] = [18]

CMD_AUTO_PID = {}
CMD_AUTO_PID['id'] = 35
CMD_AUTO_PID['data'] = ["01", "01", "ff", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00"]
CMD_AUTO_PID['data_format'] = "hex"

# stabilisce la connessione: tenta di riconoscere la porta usb alla quale
# è connesso (fino a un massimo di 100)
usb = 0
while usb < 100 and usb >= 0:
    try:
        ser = serial.Serial('/dev/ttyUSB'+str(usb))  # open serial port
        usb = -1
    except:
        usb += 1

print "Connesso su: "+str(ser.name)
ser.baudrate = 115200

send_command(CMD_MOTORS_ON)
time.sleep(1)
send_command(CMD_EXECUTE_MENU)
time.sleep(2)
send_command(CMD_CONTROL)
# time.sleep(10)
# send_command(CMD_EXECUTE_MENU)
# time.sleep(2)
# send_command(CMD_MOTORS_OFF)

print ""