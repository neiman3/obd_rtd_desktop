# Neiman's Real Time Diagnostics

from typing import Any, Union, Generator

import usb.core
import usb.util
from time import sleep


def attatchDevice(vendor_id, product_id):
    if not (type(vendor_id) == type(product_id) == int):
        raise ValueError("Invalid vendor or product ID.")

    device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    return device


def connectToDeviceProcess():
    device: usb.core.Device
    vendor_id = 0x7523
    product_id = 0x1a86
    device = attatchDevice(vendor_id, product_id)
    while device is None:  # device is not connected still
        print("Waiting for USB device...", end="")
        sleep(1)
        device = attatchDevice(vendor_id, product_id)
        if device is not None:
            break
        for x in range(0, 5):
            print("(%d)..." % (5 - x), end="")
            sleep(1)
            device = attatchDevice(vendor_id, product_id)
            if device is not None:
                break
        print("")
        if device is not None:
            break
        else:
            # failed to connect
            print("The device could not be found. Please troubleshoot your connection and try again.")
            return False

    print("The %s is connected." % device.product)

    return device.product

    # Continue to config device
    device.set_configuration()
    configure_endpoint = device.get_active_configuration()
    intf = configure_endpoint[(0, 0)]
    endpoint = usb.util.find_descriptor(
        intf,
        custom_match= \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
    )

    assert endpoint is not None

