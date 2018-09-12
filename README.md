# pymodbus_simulator

This project is built on the [example code](https://pymodbus.readthedocs.io/en/v1.3.2/examples/updating-server.html) from the pymodbus library. The additonal features include a config file which contains the settings of the modbus server and register details. Other important features are the addition of all types of registers present in the modbus specification(coil, discrete, holding, and input). 

The server which can be ran with the command: `python3 updating_server.py config.yaml`

## updating_server.py

This python file contains the server and all related functions to run it. The functions are described below.

### write_float()
``` write_float(context_in,register,address,value,slave_id=0x0) ```

### write_32int(context_in,register,address,value,slave_id=0x0)

### initialize_registers(a,slave_id,holding_float_dict,holding_int32_dict,
    holding_int16_dict,input_float_dict,input_int32_dict,input_int16_dict,
    coil_dict, discrete_dict)
    
### update_float_registers(a,register,slave_id,register_dict_float,
    random_range, ramp_slope):
    
### update_int32_registers(a,register,slave_id,register_dict_int32,
    random_range, ramp_slope)
    
### update_int16_registers(a,register,slave_id,register_dict_int16,
    random_range, ramp_slope)
    
### update_coil_registers(a,slave_id,coil_dict)

### update_discrete_register(a,slave_id,discrete_dict)

### run_updating_server(config_in, config_section=None)

### updating_writer(a,holding_float_dict,holding_int32_dict,holding_int16_dict,
    input_float_dict,input_int32_dict,input_int16_dict,
    coil_dict,discrete_dict,random_range,ramp_slope)
  

## config.yaml

A yaml config file is used to store all of the settings related to both the modbus tcp server and the registers. An example 
`config.yaml` is included in the repo to use as a starting point. The comments in the config file explain how to properly set
it up.



