#!/usr/bin/env python
"""
Pymodbus Server With Updating Thread
--------------------------------------------------------------------------

This is an example of having a background thread updating the
context while the server is operating. This can also be done with
a python thread::

    from threading import Thread

    thread = Thread(target=updating_writer, args=(context,))
    thread.start()
"""
# --------------------------------------------------------------------------- #
# import the modbus libraries we need
# --------------------------------------------------------------------------- #
from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer

# --------------------------------------------------------------------------- #
# import the twisted libraries we need
# --------------------------------------------------------------------------- #
from twisted.internet.task import LoopingCall

# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
import yaml
import random
import argparse
from struct import *

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# --------------------------------------------------------------------------- #
# define your callback process
# --------------------------------------------------------------------------- #


def updating_writer(a,registers_float_dict,registers_int_dict):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    log.debug("updating the context")
    context = a[0]
    register = 3
    slave_id = 0x00
    address = 0x0
    # Two integers to a floating point
    i1 = 0xC3F5
    i2 = 0x4840
    f = unpack('f',pack('>HH',i1,i2))[0]

    # Floating point to two integers
    i1, i2 = unpack('>HH',pack('f',3.14))
    #values = context[slave_id].getValues(register, address, count=5)
    #values = [v + 1 for v in values]
    values = [i1,i2]
    log.debug("new values: " + str(values))
    context[slave_id].setValues(register, address, values)


    for key, reg_list in registers_float_dict.items():
        # Go through each float register and apply the function specified by the
        # config file.
        if(reg_list[1] != -1):
            write_float(a,reg_list[0],reg_list[1])
            reg_list[1] = -1
        elif(reg_list[2] == 'random'):
            new_val = random.uniform(1.0,1000.0)
            write_float(a,reg_list[0],new_val)
        elif (reg_list[2] == 'ramp'):
            slope = 1.0
            print("float")
            print("RAMP!!!!")
            #write_float(a,reg_list[0],5.0)
            values   = context[slave_id].getValues(register, (reg_list[0]), count=2)
            f = unpack('f',pack('>HH',values[0],values[1]))[0]
            print("here")
            print(f)
            newval = f + 1*slope
            write_float(a,reg_list[0],newval)
            print(newval)

        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])

    for key, reg_list in registers_int_dict.items():
        # Go through each float register and apply the function specified by the
        # config file.
        if(reg_list[1] != -1):
            write_32int(a,reg_list[0],reg_list[1])
            reg_list[1] = -1
        elif(reg_list[2] == 'random'):
            new_val = random.randint(1,1000)
            print(new_val)
            write_32int(a,reg_list[0],new_val)
        elif (reg_list[2] == 'ramp'):
            slope = 1
            print("32int")
            #write_float(a,reg_list[0],5.0)
            values   = context[slave_id].getValues(register, (reg_list[0]), count=2)
            f = unpack('i',pack('>HH',values[0],values[1]))[0]
            print("here")
            print(f)
            new_val = f + 1*slope
            #write_float(a,reg_list[0],newval)
            print(new_val)
            write_32int(a,reg_list[0],new_val)

        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])





def write_float(context_in,address,value,slave_id=0x0):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    log.debug("updating the context")

    context = context_in[0]
    register = 3
    slave_id = 0x00
    #address = 0x0
    # Two integers to a floating point
    #i1 = 0xC3F5
    #i2 = 0x4840
    #f = unpack('f',pack('>HH',i1,i2))[0]

    # Floating point to two integers
    i1, i2 = unpack('>HH',pack('f',value))
    #i3, i4 = unpack('>HH',pack('f',value))
    #values = context[slave_id].getValues(register, address, count=5)
    #values = [v + 1 for v in values]
    values = [i1,i2]
    log.debug("new values: " + str(values))
    context[slave_id].setValues(register, address, values)

def write_32int(context_in,address,value,slave_id=0x0):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    log.debug("updating the context")

    context = context_in[0]
    register = 3
    slave_id = 0x00
    #address = 0x0
    # Two integers to a floating point
    #i1 = 0xC3F5
    #i2 = 0x4840
    #f = unpack('f',pack('>HH',i1,i2))[0]

    # Floating point to two integers
    i1, i2 = unpack('>HH',pack('i',value))
    values = [i1,i2]
    log.debug("new values: " + str(values))
    context[slave_id].setValues(register, address, values)

#def interper



def run_updating_server(config_in, config_section=None):
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #
    if (config_section==None):
        modbus_section = 'server'


    with open(config_in) as f:
        # use safe_load instead load
        modbusConfig = yaml.safe_load(f)

    '''
    self.PORT = modbusConfig[modbus_section]['port']
    self.registers_float_dict = modbusConfig[modbus_section]['float_registers']
    print(self.PORT)
    print(self.registers_float_dict)
    '''
    PORT = modbusConfig[modbus_section]['port']
    registers_float_dict = modbusConfig[modbus_section]['float_registers']
    registers_int_dict = modbusConfig[modbus_section]['int32_registers']
    print(PORT)
    print(registers_float_dict)
    print(len(registers_float_dict))
    register_size = len(registers_float_dict)*2 + len(registers_int_dict)*2
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [0]*register_size),
        ir=ModbusSequentialDataBlock(0, [17]*100))
    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'pymodbus Server'
    identity.ModelName = 'pymodbus Server'
    identity.MajorMinorRevision = '1.0'

    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #
    #initialize_registers(context,registers_float_dict,registers_int_dict)
    time = 5
    loop = LoopingCall(f=updating_writer, a=(context,),registers_float_dict=(registers_float_dict),registers_int_dict=(registers_int_dict))
    loop.start(time, now=False) # initially delay by time
    StartTcpServer(context, identity=identity, address=("0.0.0.0", 5020))
    write_float(context,0,23.73)

if __name__ == "__main__":
    # read arguments passed at .py file call
    # only argument is the yaml config file which specifies all the details
    # for connecting to the modbus device as well the local and remote
    # influx databases
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file")

    args = parser.parse_args()
    config_file = args.config
    #print(config_file)

    run_updating_server(config_in=config_file)
