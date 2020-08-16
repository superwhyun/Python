import pymodbus
import serial

from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.server.asynchronous import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import (ModbusRtuFramer,
                                  ModbusAsciiFramer,
                                  ModbusBinaryFramer)
# from custom_message import CustomModbusRequest

# import logging
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)


# client = ModbusClient(method="rtu", port="/dev/ttyUSB0", stopbits = 1, bytesize = 8, parity='N', baudrate = 9600)

UNIT = 0x1

def write_modbus_rtu(id=1, addr=10, value=1, unit=0x01):
    client = ModbusClient(method="rtu", port="/dev/tty.usbserial-AK066TL5", stopbits = 1, bytesize = 8, parity='N', baudrate = 9600)
    connection = client.connect()
    if(connection is not True): print('ModbusClient connection error')

    rq=client.write_register(1, 10, unit=UNIT)
    assert(not rq.isError())

    client.close()    


def read_modbus_rtu():

    client = ModbusClient(method="rtu", port="/dev/tty.usbserial-AK066TL5", stopbits = 1, bytesize = 8, parity='N', baudrate = 9600)
    connection = client.connect()
    if(connection is not True): print('ModbusClient connection error')

    rr = client.read_holding_registers(address=1, count=1, unit=UNIT)
    # assert(not rr.isError())
    print(rr)

    client.close()    


def sniff_modbus_rtu():
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [17]*100)
    )

    store.register(fc=301, fx='cm', datablock=ModbusSequentialDataBlock(0, [17] * 100))
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'ETRI'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'None'
    identity.ProductName = 'Sniffer'
    identity.ModelName = 'LabSlave'
    identity.MajorMinorRevision = '0.0.1'

    StartSerialServer(context, identity=identity, port="/dev/tty.usbserial-AK066TL5", framer=ModbusRtuFramer)

    



def looo_read_modbus_rtu_message():

    client = ModbusClient(method="rtu", port="/dev/tty.usbserial-AK066TL5", stopbits = 1, bytesize = 8, parity='N', baudrate = 9600)
    connection = client.connect()
    if(connection is not True): print('ModbusClient connection error')

    while True:
        try:
            rr = client.read_input_registers(address=1, count=1, unit=1)
            break
        except ValueError:
            print('{} has some error'.format(rr))
        else:
            print('Error: ', type(rr))

    client.close()       

        # print(rr.registers[0] / 100.0)


   

import argparse   

if __name__ == "__main__":


    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--mode", required=True, help="client/server")
    # ap.add_argument("-i", "--image", required=True, help="input image to apply neural style transfer to")
    args = vars(ap.parse_args())

    if(args['mode']=='server'):
        sniff_modbus_rtu()
    elif(args['mode']=='client'):
        read_modbus_rtu()
