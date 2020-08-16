#!/usr/bin/env python
"""
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus.

It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
# from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.client.sync import ModbusUdpClient as ModbusClient

import pymodbus
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1


def run_sync_client():

    iteration_counter=0
    success_counter=0
    fail_counter=0
    client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=1,
                        baudrate=115200)
    client.connect()
    while(iteration_counter < 10000):
    
        time.sleep(2)
        try:


            log.debug("Write to a holding register and read back")
            rq = client.write_register(1, 10, unit=UNIT)
            rr = client.read_holding_registers(1, 1, unit=UNIT)
            assert(not rq.isError())     # test that we are not an error
            # assert(rr.registers[0] == 10)       # test the expected value

            log.debug("Write to multiple holding registers and read back")
            rq = client.write_registers(1, [10]*8, unit=UNIT)

            time.sleep(0.5) # 이것을 넣지 않으면 에러가 뿜뿜. --> 마찬가지...
            rr = client.read_holding_registers(1, 8, unit=UNIT)
            assert(not rq.isError())     # test that we are not an error
            # assert(rr.registers == [10]*8)      # test the expected value

            # arguments = {
            #     'read_address':    1,
            #     'read_count':      8,
            #     'write_address':   1,
            #     'write_registers': [20]*8,
            # }
            # log.debug("Read write registeres simulataneously")
            # rq = client.readwrite_registers(unit=UNIT, **arguments)
            # rr = client.read_holding_registers(1, 8, unit=UNIT)
            # assert(not rq.isError())     # test that we are not an error
            # assert(rq.registers == [20]*8)      # test the expected value
            # assert(rr.registers == [20]*8)      # test the expected value
        except AssertionError:
            print('ASSERT ERROR')
            fail_counter+=1
        except pymodbus.exceptions.ModbusIOException:
            print('REGISTER ERROR')
            fail_counter+=1
        else:
            success_counter+=1

        iteration_counter+=1
        print('iteration # : ', iteration_counter, 
                ' success : ', success_counter, 
                ' fail : ', fail_counter,
                ' rate : ', float(success_counter/iteration_counter)*100 , '%')

        
    # ----------------------------------------------------------------------- #
    # close the client
    # ----------------------------------------------------------------------- #
    client.close()


if __name__ == "__main__":
    run_sync_client()