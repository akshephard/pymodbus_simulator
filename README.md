# pymodbus_simulator

This project is built on the [example code](https://pymodbus.readthedocs.io/en/v1.3.2/examples/updating-server.html) from the pymodbus library. The additonal features include a config file which contains the settings of the modbus server and register details. Other important features are the addition of all types of registers present in the modbus specification(coil, discrete, holding, and input). 

The server which can be ran with the command: ```python3 updating_server.py config.yaml```
Edit the config.yaml as desired to simulate a target device.

## config.yaml

A yaml config file is used to store all of the settings related to both the modbus tcp server and the registers. An example 
`config.yaml` is included in the repo to use as a starting point. The comments in the config file explain how to properly set
it up. 

## updating_server.py

This python file contains the server and all related functions to run it. The functions are described below.

### write_float()
``` write_float(context_in,register,address,value,slave_id=0x0) ```

This function works for both holding registers (function code 3) or input registers (function code 4). The float 
value that is passed in is converted to equivalent 16 bit integers. This is necessary because the ```setValues()``` 
function in the pymodbus library only takes an array of short integers as input.

### write_32int()
```
write_32int(context_in,register,address,value,slave_id=0x0) 
```

This function works for both holding registers (function code 3) or input registers (function code 4). The int32 
value that is passed in is converted to equivalent 16 bit integers. This is necessary because the ```setValues()```
function in the pymodbus library only takes an array of short integers as input.

### initialize_registers()
```
initialize_registers(a,slave_id,holding_float_dict,holding_int32_dict,
    holding_int16_dict,input_float_dict,input_int32_dict,input_int16_dict,
    coil_dict, discrete_dict)
```

This function uses the dictionaries created from the config file to initalize the values of the registers before 
the server is started.
    
### update_float_registers()
```
update_float_registers(a,register,slave_id,register_dict_float,
    random_range, ramp_slope)
```
This function updates the float registers for both holding registers (function code 3) or input registers 
(function code 4) using the function specified in the config file (random, ramp, or none).
    
### update_int32_registers()
```
update_int32_registers(a,register,slave_id,register_dict_int32,
    random_range, ramp_slope)
```
This function updates the int32 registers for both holding registers (function code 3) or input registers 
(function code 4) using the function specified in the config file (random, ramp, or none).
    
### update_int16_registers()
```
update_int16_registers(a,register,slave_id,register_dict_int16,
    random_range, ramp_slope)
```
This function updates the int16 registers for both holding registers (function code 3) or input registers 
(function code 4) using the function specified in the config file (random, ramp, or none).
    
### update_coil_registers()
```
update_coil_registers(a,slave_id,coil_dict)
```
This function updates the coil registers (function code 1). The previous value can be flipped each time 
the server is updated if specified in the coil dictionary which is generated from the config file.

### update_discrete_register()
```
update_discrete_register(a,slave_id,discrete_dict)
```
This function updates the discrete registers (function code 2). The previous value can be flipped each time 
the server is updated if specified in the coil dictionary which is generated from the config file.


### updating_writer()
```
updating_writer(a,holding_float_dict,holding_int32_dict,holding_int16_dict,
    input_float_dict,input_int32_dict,input_int16_dict,
    coil_dict,discrete_dict,random_range,ramp_slope)
```
This function runs via the twisted library every 5 seconds to update the values of the registers according
to the register dictionaries created from the config file. 

### run_updating_server()
```
run_updating_server(config_in, config_section=None)
```
This function: parses the config file and sets the register dictionaries, initializes the registers, launches the ```updating_writer()``` function with twisted, and launches the tcp server.





