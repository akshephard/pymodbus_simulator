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

import logging
import yaml
import random
import argparse
from struct import *

# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# --------------------------------------------------------------------------- #
# define your callback process
# --------------------------------------------------------------------------- #

def write_float(context_in,register,address,value,slave_id=0x0):
    """ This function converts the value given to two short unsigned integers
    in the correct format so that the registers written to can be read together
    as one 32 bit float

    :param context_in: context containing the datastore with all registers
    :param register: type of register, 3 for holding and 4 for input register
    :param value: 32 bit float value to be written to target register(s)
    :returns: Nothing
    """
    log.debug("updating the context")

    #context = context_in[0]
    context = context_in
    slave_id = 0x00

    # Floating point to two integers
    i1, i2 = unpack('<HH',pack('f',value))

    values = [i1,i2]
    log.debug("new values: " + str(values))
    context[slave_id].setValues(register, address, values)


def write_32int(context_in,register,address,value,slave_id=0x0):
    """ This function converts the value given to two short unsigned integers
    in the correct format so that the registers written to can be read together
    as one 32 bit integer

    :param context_in: context containing the datastore with all registers
    :param register: type of register, 3 for holding and 4 for input register
    :param value: 32 bit integer value to be written to target register(s)
    :returns: Nothing
    """
    log.debug("updating the context")

    #context = context_in[0]
    context = context_in
    #register = 3
    slave_id = 0x00
    print(value)
    # 32 bit integer to two 16 bit short integers for writing to registers
    i1, i2 = unpack('<HH',pack('i',value))
    values = [i1,i2]
    print(values)
    context[slave_id].setValues(register, address, values)

def write_16int(context,register,address,value,slave_id=0x0):
    """ This function converts the value given to two short unsigned integers
    in the correct format so that the registers written to can be read together
    as one 32 bit integer

    :param context_in: context containing the datastore with all registers
    :param register: type of register, 3 for holding and 4 for input register
    :param value: 32 bit integer value to be written to target register(s)
    :returns: Nothing
    """
    slave_id = 0x00
    log.debug("updating the context")
    # Take signed 32 bit integer and convert to two unsigned short integers
    # throw away 16 bits (i2)
    i1,i2 = unpack('<HH',pack('i',value))
    context[slave_id].setValues(register, address, [i1])


def initialize_registers(context,slave_id,holding_float_dict,holding_int32_dict,
    holding_int16_dict,input_float_dict,input_int32_dict,input_int16_dict,
    coil_dict, discrete_dict):
    #TODO update context stuff
    """ This function initializes all the registers of each type contained in
    the config file to their specified initial value.

    :param context_in: context containing the datastore with all registers
    :param slave_id: slave id for simulator will likely get rid of this...
    :param holding_float_dict: dictionary with all settings for 32 bit float registers
    :param holding_int32_dict: dictionary with all settings for 32 bit int registers
    :param holding_int16_dict: dictionary with all settings for 16 bit int registers
    :param input_float_dict: dictionary with all settings for 32 bit float registers
    :param input_int32_dict: dictionary with all settings for 32 bit int registers
    :param input_int16_dict: dictionary with all settings for 16 bit int registers
    :param coil_dict: dictionary with all settings for coil registers
    :param discrete_dict: dictionary with all settings for discrete registers
    :returns: Nothing
    """
    slave_id = 0x15
    for key, reg_list in holding_float_dict.items():
        # Go through each float register and set to initial value
        write_float(context,3,reg_list[0],reg_list[1])

    for key, reg_list in holding_int32_dict.items():
        # Go through each int32 register and set to initial value
        write_32int(context,3,reg_list[0],reg_list[1])

    for key, reg_list in holding_int16_dict.items():
        # Go through each int16 register and set to initial value
        write_16int(context,3,reg_list[0],reg_list[1])

    for key, reg_list in input_float_dict.items():
        # Go through each float register and set to initial value
        write_float(context,4,reg_list[0],reg_list[1])

    for key, reg_list in input_int32_dict.items():
        # Go through each int32 register and set to initial value
        write_32int(context,4,reg_list[0],reg_list[1])

    for key, reg_list in input_int16_dict.items():
        # Go through each int16 register and set to initial value
        write_16int(context,4,reg_list[0],reg_list[1])

    for key1, reg_list_coil in coil_dict.items():
        context[slave_id].setValues(1, reg_list_coil[0], [reg_list_coil[1]])

    for key2, reg_list_discrete in discrete_dict.items():
        context[slave_id].setValues(2, reg_list_discrete[0], [reg_list_discrete[1]])

def update_float_registers(context,register,slave_id,register_dict_float,
    random_range, ramp_slope):
    """ This function updates all the registers of type 32float contained in
    the config file with their specified update function

    :param context_in: context containing the datastore with all registers
    :param slave_id: slave id for simulator will likely get rid of this...
    :param register_dict_float: dictionary with all settings for 32 bit int registers
    :param random_range: range of random numbers to be generated as list [start,end]
    :param ramp_slope: slope for ramp function
    :returns: Nothing
    """


    for key, reg_list in register_dict_float.items():
        # Go through each float register and apply the function specified by the
        # config file.

        if(reg_list[2] == 'random'):

            new_val = random.uniform(random_range[0],random_range[1])
            write_float(context,register,reg_list[0],new_val)


        elif (reg_list[2] == 'ramp'):
            # get previous values from the two registers which combine to the
            # float value
            values = context[slave_id].getValues(register, (reg_list[0]), count=2)
            #convert two short integers from register into a float value
            previous_float_val = unpack('f',pack('<HH',values[0],values[1]))[0]
            #Add in slope to previous value
            newval = previous_float_val + 1*ramp_slope
            write_float(context,register,reg_list[0],newval)

        elif (reg_list[2] == 'none'):
            print("value unchanged")


def update_int32_registers(context,register,slave_id,register_dict_int32,
    random_range, ramp_slope):
    """ This function updates all the registers of type int32 contained in
    the config file with their specified update function

    :param context_in: context containing the datastore with all registers
    :param slave_id: slave id for simulator will likely get rid of this...
    :param register_int32_dict: dictionary with all settings for 32 bit int registers
    :param random_range: range of random numbers to be generated as list [start,end]
    :param ramp_slope: slope for ramp function
    :returns: Nothing
    """
    print("We are in the update of int32 registers")
    #slope = ramp_slope

    for key, reg_list in register_dict_int32.items():
        # Go through each float register and apply the function specified by the
        # config file.

        if(reg_list[2] == 'random'):
            new_val = random.randint(random_range[0],random_range[1])
            print(new_val)
            write_32int(context,register,reg_list[0],new_val)

        elif (reg_list[2] == 'ramp'):
            # Get previous values that represent the 32 bit integer as two
            # short integers
            values  = context[slave_id].getValues(register, reg_list[0], count=2)

            #change short integers to 32 bit integer
            previous_integer_val = unpack('i',pack('<HH',int(values[0]),int(values[1])))[0]

            # Add previous value to slope
            new_val = previous_integer_val + 1*ramp_slope

            #write value back to register
            write_32int(context,register,reg_list[0],int(new_val))

        elif (reg_list[2] == 'none'):
            print("value unchanged")

        print(key, 'corresponds to', reg_list[0])

def update_int16_registers(context,register,slave_id,register_dict_int16,
    random_range, ramp_slope):
    """ This function updates all the registers of type int16 contained in
    the config file with their specified update function

    :param context_in: context containing the datastore with all registers
    :param slave_id: slave id for simulator will likely get rid of this...
    :param register_int16_dict: dictionary with all settings for 32 bit int registers
    :param random_range: range of random numbers to be generated as list [start,end]
    :param ramp_slope: slope for ramp function
    :returns: Nothing
    """

    #slope = ramp_slope
    for key, reg_list in register_dict_int16.items():
        # Go through each float register and apply the function specified by the
        # config file.

        if(reg_list[2] == 'random'):
            new_val = random.randint(random_range[0],random_range[1])
            write_16int(context,register,reg_list[0],int(new_val))
            #context[slave_id].setValues(register, reg_list[0], [new_val])

        elif (reg_list[2] == 'ramp'):
            # Get previous values that represent the 32 bit integer as two
            # short integers
            values  = context[slave_id].getValues(register, reg_list[0], count=1)
            # Convert value from unsigned to signed and throw away 16 bits (i2)
            i1,i2 = unpack('<hh',pack('i',values[0]))

            new_val = i1 + ramp_slope*1
            write_16int(context,register,reg_list[0],int(new_val))

        elif (reg_list[2] == 'none'):
            print("value unchanged")

        print(key, 'corresponds to', reg_list[0])

def update_coil_registers(context,slave_id,coil_dict):
    """ This function updates all the coil registers depending on their settings

    :param context_in: context containing the datastore with all registers
    :param slave_id: slave id for simulator will likely get rid of this...
    :param coil_dict: dictionary with all settings for 32 bit int registers
    :returns: Nothing
    """
    #context = context_in[0]
    #context = context_in
    for key1, reg_list_coil in coil_dict.items():
        # Go through each coil register and set the value to the opposite of the
        # curent value if the third item of the list is set to true in the config
        if reg_list_coil[2] == 'True':
            value = context[slave_id].getValues(1, reg_list_coil[0], count=1)
            if (value[0] == 1):
                value[0] = 0
            else:
                value[0]  = 1
            context[slave_id].setValues(1, reg_list_coil[0], [value[0]])

def update_discrete_register(context,slave_id,discrete_dict):
    """ This function updates all the coil registers depending on their settings

    :param context_in: context containing the datastore with all registers
    :param slave_id: slave id for simulator will likely get rid of this...
    :param coil_dict: dictionary with all settings for 32 bit int registers
    :returns: Nothing
    """
    print("We are in the update of discrete registers")
    #context = context_in[0]
    #context = context_in
    for key2, reg_list_discrete in discrete_dict.items():
        # Go through each discrete register and set the value to the opposite of the
        # curent value if the third item of the list is set to true in the config
        if reg_list_discrete[2] == 'True':
            value = context[slave_id].getValues(2, reg_list_discrete[0], count=1)
            print(value[0])
            if (value[0] == 1):
                value[0] = 0
            else:
                value[0]  = 1
            print(value[0])
            context[slave_id].setValues(2, reg_list_discrete[0], [value[0]])


def updating_writer(context,slave_id,holding_float_dict,holding_int32_dict,
    holding_int16_dict,input_float_dict,input_int32_dict,
    input_int16_dict,coil_dict,discrete_dict,random_range,
    ramp_slope):

    """ This function updates all the registers of each type contained in
    the config file to their specified initial value.

    :param context_in: context containing the datastore with all registers
    :param slave_id: slave id for simulator will likely get rid of this...
    :param holding_float_dict: dictionary with all settings for 32 bit float registers
    :param holding_int32_dict: dictionary with all settings for 32 bit int registers
    :param holding_int16_dict: dictionary with all settings for 16 bit int registers
    :param input_float_dict: dictionary with all settings for 32 bit float registers
    :param input_int32_dict: dictionary with all settings for 32 bit int registers
    :param input_int16_dict: dictionary with all settings for 16 bit int registers
    :param coil_dict: dictionary with all settings for coil registers
    :param discrete_dict: dictionary with all settings for discrete registers
    :param random_range: range of random numbers to be generated as list [start,end]
    :param ramp_slope: slope for ramp function
    :returns: Nothing
    """

    #log.debug("updating the context")
    #context = a[0]
    #test_context = a[0]
    #test_context = context
    # Update the coil register according to the flip boolean in the coil_dict
    #update_coil_registers(a,slave_id,coil_dict)
    update_coil_registers(context,slave_id,coil_dict)

    # # Update the discrete register according to the flip boolean in the discrete_dict
    update_discrete_register(context,slave_id,discrete_dict)

    # Update each holding register type according to function specified in config
    update_float_registers(context,3,slave_id,holding_float_dict,
        random_range, ramp_slope)

    update_int32_registers(context,3,slave_id,holding_int32_dict,
        random_range, ramp_slope)

    update_int16_registers(context,3,slave_id,holding_int16_dict,
        random_range, ramp_slope)


    # Update each input register type according to function specified in config
    update_float_registers(context,4,slave_id,input_float_dict,
        random_range, ramp_slope)

    update_int32_registers(context,4,slave_id,input_int32_dict,
        random_range, ramp_slope)

    update_int16_registers(context,4,slave_id,input_int16_dict,
        random_range, ramp_slope)


def run_updating_server(config_in, config_section=None):
    """ This function updates all the registers of each type contained in
    the config file to their specified initial value.

    :param config_in: YAML config file containing all settings (see example)
    :param config_section: section settings are under
    :returns: Nothing
    """

    # read config file
    if (config_section==None):
        modbus_section = 'server'


    with open(config_in) as f:
        # use safe_load instead load
        modbusConfig = yaml.safe_load(f)

    PORT = modbusConfig[modbus_section]['port']
    DEFINED_BLOCK = modbusConfig[modbus_section]['use_block_size']
    slave_id = modbusConfig[modbus_section]['slave_id']
    update_time = modbusConfig[modbus_section]['update_time']

    random_range = modbusConfig[modbus_section]['random_range']
    ramp_slope = modbusConfig[modbus_section]['ramp_slope']

    holding_float_dict = modbusConfig[modbus_section]['float_holding']
    holding_int32_dict = modbusConfig[modbus_section]['int32_holding']
    holding_int16_dict = modbusConfig[modbus_section]['int16_holding']

    input_float_dict = modbusConfig[modbus_section]['float_input']
    input_int32_dict = modbusConfig[modbus_section]['int32_input']
    input_int16_dict = modbusConfig[modbus_section]['int16_input']

    coil_dict = modbusConfig[modbus_section]['coil_registers']
    discrete_dict = modbusConfig[modbus_section]['discrete_registers']

    if (DEFINED_BLOCK == True):
        # User has defined a custom block and offset, read the settings
        # from the config file.

        print("block size is user defined")
        coil_block_size = modbusConfig[modbus_section]['coil_block_size']
        coil_block_offset = modbusConfig[modbus_section]['coil_block_offset']

        discrete_block_size = modbusConfig[modbus_section]['discrete_block_size']
        discrete_block_offset = modbusConfig[modbus_section]['discrete_block_offset']

        holding_block_size = modbusConfig[modbus_section]['holding_block_size']
        holding_block_offset = modbusConfig[modbus_section]['holding_block_offset']

        input_block_size = modbusConfig[modbus_section]['holding_block_size']
        input_block_offset = modbusConfig[modbus_section]['holding_block_offset']
    else:
        print("use auto calulcator")
        # Calculate size needed for each register type
        holding_block_size = len(holding_float_dict)*2
        holding_block_size += len(holding_int32_dict)*2
        holding_block_size += len(holding_int16_dict)*1

        input_block_size = len(input_float_dict)*2
        input_block_size += len(input_int32_dict)*2
        input_block_size += len(input_int16_dict)*1

        discrete_block_size = len(discrete_dict)
        coil_block_size = len(coil_dict)

        coil_block_offset = 0
        discrete_block_offset = 0
        holding_block_offset = 0
        input_block_offset = 0

    # ----------------------------------------------------------------------- #
    # initialize data store according to config file
    # ----------------------------------------------------------------------- #
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(discrete_block_offset, [0]*discrete_block_size),
        co=ModbusSequentialDataBlock(coil_block_offset, [0]*coil_block_size),
        hr=ModbusSequentialDataBlock(holding_block_offset, [0]*holding_block_size),
        ir=ModbusSequentialDataBlock(input_block_offset, [0]*input_block_size))
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

    #slave_id = 0x00
    # Set all registers to their initial value as specified in config file
    initialize_registers(context,slave_id,holding_float_dict,holding_int32_dict,
        holding_int16_dict,input_float_dict,input_int32_dict,input_int16_dict,
        coil_dict, discrete_dict)
    # Set updating time and call updating writer inside a loop accorind to interval
    # time
    time = update_time
    loop = LoopingCall(f=updating_writer, context=(context),slave_id=(slave_id),
        holding_float_dict=(holding_float_dict),
        holding_int32_dict=(holding_int32_dict),
        holding_int16_dict=(holding_int16_dict),
        input_float_dict=(input_float_dict),
        input_int32_dict=(input_int32_dict),
        input_int16_dict=(input_int16_dict),
        coil_dict=(coil_dict),
        discrete_dict=(discrete_dict),
        random_range=(random_range),
        ramp_slope=(ramp_slope))
    loop.start(time, now=False) # initially delay by time


    # Setting address to 127.0.0.1 allows only the local machine to access the
    # Server. Changing to 0.0.0.0 allows for other hosts to connect.
    StartTcpServer(context, identity=identity, address=("0.0.0.0", 5020))

if __name__ == "__main__":
    # read arguments passed at .py file call
    # only argument is the yaml config file which specifies all the details
    # for connecting to the modbus device as well the local and remote
    # influx databases
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file")

    args = parser.parse_args()
    config_file = args.config

    run_updating_server(config_in=config_file)
