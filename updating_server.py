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

def write_float(context_in,register,address,value,slave_id=0x0):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    log.debug("updating the context")

    context = context_in[0]
    #register = 3
    slave_id = 0x00

    # Floating point to two integers
    i1, i2 = unpack('<HH',pack('f',value))

    values = [i1,i2]
    log.debug("new values: " + str(values))
    context[slave_id].setValues(register, address, values)

def write_32int(context_in,register,address,value,slave_id=0x0):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    log.debug("updating the context")

    context = context_in[0]
    #register = 3
    slave_id = 0x00
    print(value)
    # 32 bit integer to two 16 bit short integers for writing to registers
    i1, i2 = unpack('<HH',pack('i',value))
    values = [i1,i2]
    print(values)
    context[slave_id].setValues(register, address, values)

def initialize_registers(context_in,slave_id,holding_float_dict,holding_int32_dict,
    holding_int16_dict,input_float_dict,input_int32_dict,input_int16_dict,
    coil_dict, discrete_dict):
    #TODO update context stuff 
    context = a[0]


    for key, reg_list in holding_float_dict.items():
        # Go through each float register and set to initial value
        write_float(a,3,reg_list[0],reg_list[1])

    for key, reg_list in holding_int32_dict.items():
        # Go through each int32 register and set to initial value
        write_32int(a,3,reg_list[0],reg_list[1])

    for key, reg_list in holding_int16_dict.items():
        # Go through each int16 register and set to initial value
        context[slave_id].setValues(3, reg_list[0], [reg_list[1]])

    for key, reg_list in input_float_dict.items():
        # Go through each float register and set to initial value
        write_float(a,4,reg_list[0],reg_list[1])

    for key, reg_list in input_int32_dict.items():
        # Go through each int32 register and set to initial value
        write_32int(a,4,reg_list[0],reg_list[1])

    for key, reg_list in input_int16_dict.items():
        # Go through each int16 register and set to initial value
        context[slave_id].setValues(4, reg_list[0], [reg_list[1]])

    for key1, reg_list_coil in coil_dict.items():
        context[slave_id].setValues(1, reg_list_coil[0], [reg_list_coil[1]])

    for key2, reg_list_discrete in discrete_dict.items():
        context[slave_id].setValues(2, reg_list_discrete[0], [reg_list_discrete[1]])







def update_float_registers(context,register,slave_id,register_dict_float
    random_range, ramp_slope):
    #TODO figure out the context situation

    for key, reg_list in register_dict_float.items():
        # Go through each float register and apply the function specified by the
        # config file.

        if(reg_list[2] == 'random'):

            new_val = random.uniform(random_range[0],random_range[1])
            write_float(a,register,reg_list[0],new_val)


        elif (reg_list[2] == 'ramp'):
            print("ramp float")
            # TODO use settings from config file to set this slope
            slope = ramp_slope
            # get previous values from the two registers which combine to the
            # float value
            values = context[slave_id].getValues(register, (reg_list[0]), count=2)
            #convert two short integers from register into a float value
            previous_float_val = unpack('f',pack('<HH',values[0],values[1]))[0]
            #Add in slope to previous value
            newval = previous_float_val + 1*slope
            write_float(a,3,reg_list[0],newval)
            print(newval)

        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])

def update_int32_registers(context,register,slave_id,register_dict_int32,
    random_range, ramp_slope):
    for key, reg_list in register_dict_int32.items():
        # Go through each float register and apply the function specified by the
        # config file.

        values  = context[slave_id].getValues(register, reg_list[0], count=2)
        print("here is the address")
        print(reg_list[1])
        print("here is the value")
        print(values)
        if(reg_list[1] != -1):
            write_32int(a,register,reg_list[0],reg_list[1])
            reg_list[1] = -1

        elif(reg_list[2] == 'random'):
            print("random 32 int")
            new_val = random.randint(0,1000)
            print(new_val)
            write_32int(a,3,reg_list[0],new_val)
        elif (reg_list[2] == 'ramp'):
            print("ramp 32 int")
            slope = 1.0
            # Get previous values that represent the 32 bit integer as two
            # short integers
            values  = context[slave_id].getValues(register, reg_list[0], count=2)
            print(values)
            #change short integers to 32 bit integer

            previous_integer_val = unpack('i',pack('<HH',int(values[0]),int(values[1])))[0]

            # Add previous value to slope
            new_val = previous_integer_val + 1*slope

            #write value back to register
            print(new_val)

            write_32int(a,register,reg_list[0],int(new_val))
        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])

def update_int16_registers(context,register,slave_id,register_dict_int32,
    random_range, ramp_slope):
    for key, reg_list in registers_int16_dict.items():
        # Go through each float register and apply the function specified by the
        # config file.
        print(reg_list[0])
        values  = context[slave_id].getValues(register, reg_list[0], count=1)
        print("here is new value")
        print(values)
        print("should be the address")
        print(reg_list[0])
        if(reg_list[1] != -1):

            #i1 = unpack('<H',pack('H',reg_list[1]))
            #unpack(reg_list[])
            #print(i1)

            context[slave_id].setValues(register, reg_list[0], [reg_list[1]])

            reg_list[1] = -1

        elif(reg_list[2] == 'random'):
            print("RANDOM!!!")
            new_val = random.randint(0,1000)
            #i1 = unpack('<H',pack('H',new_val))
            #print(new_val)
            #print(i1)
            context[slave_id].setValues(register, reg_list[0], [new_val])
            #Swrite_32int(a,reg_list[0],new_val)
        elif (reg_list[2] == 'ramp'):
            slope = 1.0
            # Get previous values that represent the 32 bit integer as two
            # short integers

            values  = context[slave_id].getValues(register, reg_list[0], count=1)
            #print(values)
            new_val = values[0] + slope*1
            context[slave_id].setValues(register, reg_list[0], [int(new_val)])
        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])

def update_coil_registers(context,slave_id,coil_dict):

    for key1, reg_list_coil in coil_dict.items():
        # Go through each coil register and set the value to the opposite of the
        # curent value if the third item of the list is set to true in the config
        if reg_list_coil[2] == 'True':
            print("FLIP COILS!!!")
            value = context[slave_id].getValues(1, reg_list_coil[0], count=1)
            print(value[0])
            if (value[0] == 1):
                value[0] = 0
            else:
                value[0]  = 1
            print(value[0])
            context[slave_id].setValues(1, reg_list_coil[0], [value[0]])

def update_discrete_register(context,slave_id,discrete_dict):
    for key2, reg_list_discrete in discrete_registers.items():
        # Go through each coil register and set the value to the opposite of the
        # curent value if the third item of the list is set to true in the config
        if reg_list_discrete[2] == 'True':
            print("FLIP DISCRETE!!!")
            value = context[slave_id].getValues(2, reg_list_discrete[0], count=1)
            print(value[0])
            if (value[0] == 1):
                value[0] = 0
            else:
                value[0]  = 1
            print(value[0])
            context[slave_id].setValues(2, reg_list_discrete[0], [value[0]])



def updating_writer(a,registers_float_dict,registers_int_dict,registers_int16_dict,
    input_float_dict,input_int_dict,input_int16_dict,
    coil_registers,discrete_registers,random_range,ramp_slope):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    #log.debug("updating the context")
    context = a[0]
    register = 3
    slave_id = 0x00
    address = 0x0

    print(discrete_registers)


    for key, reg_list in registers_float_dict.items():
        # Go through each float register and apply the function specified by the
        # config file.
        if(reg_list[1] != -1):
            write_float(a,3,reg_list[0],reg_list[1])

            context[slave_id].setValues(4, 0, [35])
            count = 0
            '''
            while (count < 10):
                context[slave_id].setValues(2, count, [True])
                count += 1
            '''
            #Initialize coils to state from config file
            for key1, reg_list_coil in coil_registers.items():
                context[slave_id].setValues(1, reg_list_coil[0], [reg_list_coil[1]])

            for key2, reg_list_discrete in discrete_registers.items():
                context[slave_id].setValues(2, reg_list_discrete[0], [reg_list_discrete[1]])
                print("Another one")

            #set initial value to -1 to signify it has already been initialized
            reg_list[1] = -1
            print("tester1")
        elif(reg_list[2] == 'random'):
            for key1, reg_list_coil in coil_registers.items():
                if reg_list_coil[2] == 'True':
                    print("FLIP COILS!!!")
                    value = context[slave_id].getValues(1, reg_list_coil[0], count=1)
                    print(value[0])
                    if (value[0] == 1):
                        value[0] = 0
                    else:
                        value[0]  = 1
                    print(value[0])
                    context[slave_id].setValues(1, reg_list_coil[0], [value[0]])

            for key2, reg_list_discrete in discrete_registers.items():
                if reg_list_discrete[2] == 'True':
                    print("FLIP DISCRETE!!!")
                    value = context[slave_id].getValues(2, reg_list_discrete[0], count=1)
                    print(value[0])
                    if (value[0] == 1):
                        value[0] = 0
                    else:
                        value[0]  = 1
                    print(value[0])
                    context[slave_id].setValues(2, reg_list_discrete[0], [value[0]])
                    #context[slave_id].setValues(1, reg_list_coil[0], [reg_list_coil[1]])
            print("random float ")
            new_val = random.uniform(random_range[0],random_range[1])
            print("issue?")
            write_float(a,3,reg_list[0],new_val)


        elif (reg_list[2] == 'ramp'):
            print("ramp float")
            # TODO use settings from config file to set this slope
            slope = ramp_slope
            # get previous values from the two registers which combine to the
            # float value
            values = context[slave_id].getValues(register, (reg_list[0]), count=2)
            #convert two short integers from register into a float value
            previous_float_val = unpack('f',pack('<HH',values[0],values[1]))[0]
            #Add in slope to previous value
            newval = previous_float_val + 1*slope
            write_float(a,3,reg_list[0],newval)
            print(newval)

        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])

    for key, reg_list in registers_int_dict.items():
        # Go through each float register and apply the function specified by the
        # config file.

        values  = context[slave_id].getValues(3, reg_list[0], count=2)
        print("here is the address")
        print(reg_list[1])
        print("here is the value")
        print(values)
        if(reg_list[1] != -1):
            write_32int(a,3,reg_list[0],reg_list[1])
            reg_list[1] = -1

        elif(reg_list[2] == 'random'):
            print("random 32 int")
            new_val = random.randint(0,1000)
            print(new_val)
            write_32int(a,3,reg_list[0],new_val)
        elif (reg_list[2] == 'ramp'):
            print("ramp 32 int")
            slope = 1.0
            # Get previous values that represent the 32 bit integer as two
            # short integers
            values  = context[slave_id].getValues(3, reg_list[0], count=2)
            print(values)
            #change short integers to 32 bit integer

            previous_integer_val = unpack('i',pack('<HH',int(values[0]),int(values[1])))[0]

            # Add previous value to slope
            new_val = previous_integer_val + 1*slope

            #write value back to register
            print(new_val)

            write_32int(a,3,reg_list[0],int(new_val))
        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])


    for key, reg_list in registers_int16_dict.items():
        # Go through each float register and apply the function specified by the
        # config file.
        print(reg_list[0])
        values  = context[slave_id].getValues(3, reg_list[0], count=1)
        print("here is new value")
        print(values)
        print("should be the address")
        print(reg_list[0])
        if(reg_list[1] != -1):

            #i1 = unpack('<H',pack('H',reg_list[1]))
            #unpack(reg_list[])
            #print(i1)

            context[slave_id].setValues(3, reg_list[0], [reg_list[1]])

            reg_list[1] = -1

        elif(reg_list[2] == 'random'):
            print("RANDOM!!!")
            new_val = random.randint(0,1000)
            #i1 = unpack('<H',pack('H',new_val))
            #print(new_val)
            #print(i1)
            context[slave_id].setValues(3, reg_list[0], [new_val])
            #Swrite_32int(a,reg_list[0],new_val)
        elif (reg_list[2] == 'ramp'):
            slope = 1.0
            # Get previous values that represent the 32 bit integer as two
            # short integers

            values  = context[slave_id].getValues(3, reg_list[0], count=1)
            #print(values)
            new_val = values[0 ]+ slope*1
            context[slave_id].setValues(3, reg_list[0], [int(new_val)])
        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])

    for key, reg_list in input_float_dict.items():
        # Go through each float register and apply the function specified by the
        # config file.

        print(reg_list[2])
        if(reg_list[1] != -1):
            print("initialization input")
            print(reg_list[2])
            print("initial value for input is:::")
            print(reg_list[1])
            write_float(a,4,reg_list[0],float(reg_list[1]))

            #context[slave_id].setValues(4, 0, [35])
            '''
            count = 0
            while (count < 10):
                context[slave_id].setValues(2, count, [True])
                count += 1
            '''
            #Initialize coils to state from config file
            for key_, reg_list_coil in coil_registers.items():
                context[slave_id].setValues(1, reg_list_coil[0], [reg_list_coil[1]])

            #set initial value to -1 to signify it has already been initialized
            reg_list[1] = -1
            print("tester1")
        elif(reg_list[2] == 'random'):
            print("random float input")
            new_val = random.uniform(random_range[0],random_range[1])
            write_float(a,4,reg_list[0],new_val)


        elif (reg_list[2] == 'ramp'):
            print("ramp float input")
            # TODO use settings from config file to set this slope
            slope = ramp_slope
            # get previous values from the two registers which combine to the
            # float value
            print(reg_list[0])
            values = context[slave_id].getValues(4, reg_list[0], count=2)
            #convert two short integers from register into a float value
            print("Issue?")
            print(values)
            previous_float_val = unpack('f',pack('<HH',values[0],values[1]))[0]
            #Add in slope to previous value
            print("Issue??")
            newval = previous_float_val + 1*slope
            write_float(a,4,reg_list[0],newval)
            print(newval)

        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])

    for key, reg_list in input_int_dict.items():
        # Go through each float register and apply the function specified by the
        # config file.

        values  = context[slave_id].getValues(3, reg_list[0], count=2)
        print("here is the address")
        print(reg_list[1])
        print("here is the value")
        print(values)
        if(reg_list[1] != -1):
            write_32int(a,4,reg_list[0],reg_list[1])
            reg_list[1] = -1

        elif(reg_list[2] == 'random'):
            print("random 32 int")
            new_val = random.randint(0,1000)
            print(new_val)
            write_32int(a,4,reg_list[0],new_val)
        elif (reg_list[2] == 'ramp'):
            print("ramp 32 int")
            slope = 1.0
            # Get previous values that represent the 32 bit integer as two
            # short integers
            values  = context[slave_id].getValues(4, reg_list[0], count=2)
            print(values)
            #change short integers to 32 bit integer

            previous_integer_val = unpack('i',pack('<HH',int(values[0]),int(values[1])))[0]

            # Add previous value to slope
            new_val = previous_integer_val + 1*slope

            #write value back to register
            print(new_val)

            write_32int(a,4,reg_list[0],int(new_val))
        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])


    for key, reg_list in input_int16_dict.items():
        # Go through each float register and apply the function specified by the
        # config file.
        print(reg_list[0])
        values  = context[slave_id].getValues(4, reg_list[0], count=1)
        print("here is new value")
        print(values)
        print("should be the address")
        print(reg_list[0])
        if(reg_list[1] != -1):

            #i1 = unpack('<H',pack('H',reg_list[1]))
            #unpack(reg_list[])
            #print(i1)

            context[slave_id].setValues(4, reg_list[0], [reg_list[1]])

            reg_list[1] = -1

        elif(reg_list[2] == 'random'):
            print("RANDOM!!!")
            new_val = random.randint(0,1000)
            #i1 = unpack('<H',pack('H',new_val))
            #print(new_val)
            #print(i1)
            context[slave_id].setValues(4, reg_list[0], [new_val])
            #Swrite_32int(a,reg_list[0],new_val)
        elif (reg_list[2] == 'ramp'):
            slope = 1.0
            # Get previous values that represent the 32 bit integer as two
            # short integers

            values  = context[slave_id].getValues(4, reg_list[0], count=1)
            #print(values)
            new_val = values[0 ]+ slope*1
            context[slave_id].setValues(4, reg_list[0], [int(new_val)])
        elif (reg_list[2] == 'none'):
            print("value unchanged")
        else:
            raise e
        print(key, 'corresponds to', reg_list[0])












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

    registers_float_dict = modbusConfig[modbus_section]['float_holding']
    registers_int_dict = modbusConfig[modbus_section]['int32_holding']
    registers_int16_dict = modbusConfig[modbus_section]['int16_holding']

    input_float_dict = modbusConfig[modbus_section]['float_input']
    input_int_dict = modbusConfig[modbus_section]['int32_input']
    input_int16_dict = modbusConfig[modbus_section]['int16_input']

    coil_registers = modbusConfig[modbus_section]['coil_registers']
    discrete_registers = modbusConfig[modbus_section]['discrete_registers']
    random_range = modbusConfig[modbus_section]['random_range']
    ramp_slope = modbusConfig[modbus_section]['ramp_slope']

    print(coil_registers)
    print(discrete_registers)
    print(PORT)
    print(registers_float_dict)
    print(registers_int16_dict)
    print(len(registers_float_dict))
    register_size = len(registers_float_dict)*2 + len(registers_int_dict)*2


    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*99),
        hr=ModbusSequentialDataBlock(0, [0]*(register_size+100)),
        ir=ModbusSequentialDataBlock(0, [0]*100))
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
    first_time = False
    loop = LoopingCall(f=updating_writer, a=(context,),
        registers_float_dict=(registers_float_dict),
        registers_int_dict=(registers_int_dict),
        registers_int16_dict=(registers_int16_dict),
        input_float_dict=(input_float_dict),
        input_int_dict=(input_int_dict),
        input_int16_dict=(input_int16_dict),
        coil_registers=(coil_registers),
        discrete_registers=(discrete_registers),
        random_range=(random_range),
        ramp_slope=(ramp_slope))
    loop.start(time, now=False) # initially delay by time
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
    #print(config_file)

    run_updating_server(config_in=config_file)
