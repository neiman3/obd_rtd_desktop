import serial
import threading
import time
from time import sleep

def connect_device(addr):
    try:
        device = serial.Serial(addr, 9600)
        return device
    except serial.SerialException:
        print("Device not connected.")
        return None
    except KeyboardInterrupt:
        return None

def rsend(device: serial.Serial, call):
    if device is None:
        return None
    try:
        device.flushInput()
        device.flushOutput()

        device.write(call)

        sleep(0.5)

        while device.inWaiting():
            response = device.readline()
            print("Got data: " + str(response))

    except Exception as e:
        print ("Communication interrupted " + str(e))


def send(device: serial.Serial, call):
    if device is None:
        return None
    try:
        device.flushInput()
        device.flushOutput()
        device.write(call)
    except Exception as e:
        print("Error" + str(e))

def receive_all_waiting_data(device):
    response = []
    try:
        while device.inWaiting():
            response.append(clean_string(device.readline()))
            if len(response) > 24:
                break
    except Exception as e:
        print("Connection interrupted: "+ str(e))
    return response


def clean_string(string):
    return str(string)[2:-5]


if __name__ == "__main__":
    device_address = "/dev/cu.wchusbserial1441310"
    ardu = connect_device(device_address)
    sleep(0.25)
    ardu.flushOutput()
    ardu.flushInput()




