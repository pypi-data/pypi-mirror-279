import usb.core

usb_vendor = 0x0483
usb_product = 0x5720

out_ep = 0x03
in_ep = 0x81


def get_volcora_dev():
    dev = usb.core.find(idVendor=usb_vendor, idProduct=usb_product)

    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)

    dev.set_configuration()
    dev.reset()

    return dev


def get_volcora_printer():
    dev = get_volcora_dev()
    return lambda d: dev.write(out_ep, d)
