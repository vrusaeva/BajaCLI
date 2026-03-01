import os
import glob
import time

# These tow lines mount the device and make it connect easier:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
#This is where the temp sensor is sending data too
temp_file = "/sys/bus/w1/devices/28-000000379b4d/w1_slave"

#This reads the raw output from the temperature sensor
def read_temp_raw():
    f = open(temp_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#Takes the raw output and turns it into a readable design
def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.02)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f
 
# while True:
#     print(' C=%3.3f  F=%3.3f'% read_temp())
# time.sleep(1)