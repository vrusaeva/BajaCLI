import temp_sens
# import linear_potentiometer as lp
import ctypes
import datetime as date
import time, os, csv
from dotenv import load_dotenv

def main(out_file_name):
    # Load the shared library
    accel = ctypes.CDLL('./accelerometer.so')


    load_dotenv()
    filepath = os.getenv("BASE_FILEPATH_OUTPUT")


    #The data type that is returned from the read_accel function to read acceleration (This is a C Struct)
    class mma8451_acceleration(ctypes.Structure):
        _fields_ = [('x', ctypes.c_double),
                    ('y', ctypes.c_double),
                    ('z', ctypes.c_double)
                    ]

    #A data type that is used in the mma8451 class (This is a Enum)
    class mma8451_range_scale(ctypes.c_int):
        MMA8451_RANGE_2G = 0
        MMA8451_RANGE_4G = 1
        MMA8451_RANGE_8G = 2
        MMA8451_RANGE_RESERVED = 3

    #A data type that is used in the mma8451 class (This is a Enum)
    class mma8451_output_size(ctypes.c_int):
        MMA8451_8BIT_OUTPUT = 1
        MMA8451_14BIT_OUTPUT = 0

    #The class that holds the information of the accelerometer
    #so we can access the accelerometer from multiple functions in python (This is a C Struct)
    class mma8451(ctypes.Structure):
        _fields_ = [('path',ctypes.POINTER(ctypes.c_char)),
                    ('file',ctypes.c_int),
                    ('addr',ctypes.c_ubyte),
                    ('range',mma8451_range_scale),
                    ('data_size',mma8451_output_size),
                    ('last_error',ctypes.c_char * 500)
                    ]


    #This chunks of code are telling python the input parameters and
    #the return types of the C functions we are calling 
    accel.accel_on.argtypes = [ctypes.POINTER(ctypes.c_int)]
    accel.accel_on.restype = ctypes.POINTER(mma8451)

    accel.read_accel.argtypes = [ctypes.POINTER(mma8451)]
    accel.read_accel.restype = mma8451_acceleration

    accel.accel_off.argtypes = [ctypes.POINTER(mma8451)]

    #code for checking power state
    #Will be connected to a switch in the future
    def power():
        power = True

        return power

    #code for the switch to be on or off
    #Will be connected to a button in the future
    def record():
        record = True

        return record

    #Will launch a shutdown a script to put DALE to sleep
    def shutdown():
        return False
        
    auto = False

    count = 0
    #Start of the control flow where if the switch is turned on we start
    if auto:
        while (power() & (count < 20)):
            count = count + 1
            #Create the variable to hold the address of the accelerometer
            #Then we start reading the data and recording it in the dedicated caches.
            if record():
                #initialize all the sensors
                print("Initializing sensors\n")
                status = ctypes.c_int(0)

                #creates the variable to hold the actual acceleration
                acceleration = mma8451_acceleration(x=0.0, y=0.0, z=0.0)

                #Turn on the accelerometer and prepare to recieve values
                accelerometer = accel.accel_on(ctypes.byref(status))

                #Initalize the linear potentiometers
                # pot = lp.init_pot()

                with open(file = filepath + out_file_name, mode='w') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["Temperature", "x", "y", "z"])
                    #Will record as long as the button is flipped to the on state
                    while record():
                        #Start calling the recording funtions to get the data

                        #Read the acceleration
                        acceleration = accel.read_accel(accelerometer)
                        
                        #Read the temperature
                        temp = temp_sens.read_temp()

                        #Read the position data from the linear potetiometers
                        #Reads data out as a list
                        # lin_data = lp.pot_read(pot)

                        #In the future we will write these values to a file

                        # print(f"Temperature: {temp[1]}")
                        # print(f"x={acceleration.x}, y={acceleration.y}, z={acceleration.z}")
                        # print('fr:',lin_data[0].value,', fl:',lin_data[1].value) #', rr:',lin_data[2].value,', rl:',lin_data[3].value,'\n')
                        # print('\n')
                        # write to a CSV file
                        writer.writerow([temp[1], acceleration.x, acceleration.y, acceleration.z])

                        
                    #Record came back as false and now we stop recording and close out all of the sensors
                    accel.accel_off(ctypes.byref(accelerometer))
                    return filepath + out_file_name
                
            else:
                print("waiting for record function")
    else:
        with open('opened.txt', 'w+') as file:
            file.write(str(date.datetime.now()))
            # file.write(' Time:')
            # file.write(str(time.time()))

    shutdown()