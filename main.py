#!/home/pi/src/diy-cec/env/bin/python3

import cec
import time

def main():
    cec.init('RPI')
    print('Ready')

    cec.add_callback(onEvent(cec.list_devices()), cec.EVENT_COMMAND)

    while True:
        time.sleep(9e8)

def mapDevices(devices):
    return {devices[i].osd_string: devices[i] for i in devices}

def onEvent(devices):
    def callback(event, cmd):
        initiator_device_osd = devices[cmd['initiator']].osd_string
        print('event', event, 'cmd', cmd, cmd['initiator'])

        if initiator_device_osd == 'TV':
            if cmd['opcode'] == cec.CEC_OPCODE_GIVE_DEVICE_POWER_STATUS:
                turnOnReceiver(devices)
            elif cmd['opcode'] == cec.CEC_OPCODE_STANDBY:
                turnOffReceiver(devices)

    return callback

def turnOnReceiver(devices):
    mapped = mapDevices(devices)
    mapped['RX-V377'].power_on()

    cec.transmit(
        cec.CECDEVICE_BROADCAST,
        cec.CEC_OPCODE_SYSTEM_AUDIO_MODE_REQUEST,
        b'\x00\x00'
    )

def turnOffReceiver(devices):
    mapped = mapDevices(devices)
    mapped['RX-V377'].standby()

if __name__ == '__main__':
    main()
