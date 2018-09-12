# pymodbus_simulator

This project is built on the [example code](https://pymodbus.readthedocs.io/en/v1.3.2/examples/updating-server.html) from the pymodbus library. The additonal features include a config file which contains the settings of the modbus server and register details. Other important features are the addition of all types of registers present in the modbus specification(coil, discrete, holding, and input). 

The server which can be ran with the command: `python3 updating_server.py config.yaml`

## updating_server.py

This python file contains the server and all related functions to run it. 

## config.yaml

A yaml config file is used to store all of the settings related to both the modbus tcp server and the registers. An example 
`config.yaml` is included in the repo to use as a starting point. The comments in the config file explain how to properly set
it up.



