/*
 * This is a simple example of how to open and read from an
 * accelerometer using the libmma8451 library.
 * 
 * If new changes are made to this file, this is how you recompile it
 * gcc -shared -o accelerometer.so -fPIC accelerometer.c -lrt -lmma8451
 * 
 */
#include <time.h>
#include "libmma8451/mma8451.h"
#include <stdio.h>  
#include <unistd.h>
#include <stdlib.h>


/**
 * Prints the usage statement for this application.
 */
void printUsage() {
    printf("Usage: mma8451-test [device path] [i2c address]\n");
    printf("  e.g. mma8451 /dev/i2c-1 0x1c\n\n");
}

/**
 * Main function, starts the program and attempts to open the accelerometer
 * and read from it.
 * 
 * Use this function if testing the accelerometer independently
 */
int main(int argc, char** argv) {
    struct timespec start;
    struct timespec sample;
    unsigned int samples = 0;
    char* path;
    unsigned char address;

    //Give the path to where we are pulling the i2c data from
    path = "/dev/i2c-3"; //In this case we are pulling from the third bus
    address = (unsigned char)strtol("0x1d", NULL, 0); //and from the 0x1d spot

    printf("Attempting to open %s and talk to I2C device at 0x%02x\n", path, address);

    //Sending an open code, so we can start the communication for the accelerometer
    mma8451* dev = mma8451_open(path, address);
    if(dev == NULL) {
        perror("Unable to open device.");
        return -1;
    }

    printf("Successfully opened device, initializing...\n");
    // Getting the device to an usable status
    if(!initializeDevice(dev)) {
        perror("Unable to initialize device.");
        return -2;
    }

    printf("Successfully initialized, starting capture. (Press Ctrl-C to stop)\n");
    clock_gettime(0, &start);

    printf("\n");
    for(int i = 0; i < 20; i++) {
        mma8451_acceleration data;
        long long duration;
        double samplesPerSecond;

        usleep(500000);

        //Actually read the acceleration data from the accelerometer.
        if(!mma8451_get_acceleration(dev, &data)) {
            return 0;
        }

        clock_gettime(0, &sample);
        samples++;

        //Calculate the samples per second.
        duration = ((sample.tv_sec - start.tv_sec) * 1000);
        duration += (sample.tv_nsec - start.tv_nsec) / 1.0e6;
        samplesPerSecond = (duration > 0) ? samples / ((double)duration / 1000) : 0;

        //Print the sample.
        printf("x=%f, y=%f, z=%f, samplesPerSecond=%f\n", data.x, data.y, data.z, samplesPerSecond);
    }

    mma8451_close(dev);
    return 0;
}

//FOR PYTHON
//This function will turn on the accelerometer and get it ready to send data
mma8451* accel_on(int* status) {
    char* path;
    unsigned char address;

    //Give the path to where we are pulling the i2c data from
    path = "/dev/i2c-3"; //In this case we are pulling from the first bus
    address = (unsigned char)strtol("0x1d", NULL, 0); //and from the 0x1d spot

    printf("Attempting to open %s and talk to I2C device at 0x%02x\n", path, address);

    //Sending an open code, so we can start the communication for the accelerometer
    mma8451* dev = mma8451_open(path, address);
    if(dev == NULL) {
        perror("Unable to open device.");
        *status = -1;
        return NULL;
    }

    printf("Successfully opened device, initializing...\n");
    // Getting the device to an usable status
    if(!initializeDevice(dev)) {
        perror("Unable to initialize device.");
        *status = -2;
        return NULL;
    }
    *status = 0;
    return dev;
}

//FOR PYTHON
//This function reads data from the accelerometer
mma8451_acceleration read_accel(mma8451* accel) {
    mma8451_acceleration data;
    long long duration;
    double samplesPerSecond;

    //usleep(500000);

    //Actually read the acceleration data from the accelerometer.
    if(!mma8451_get_acceleration(accel, &data)) {
        mma8451_acceleration error;
        error.x = 5;
        error.y = 5;
        error.z = 5;
        return error;
    }
    
    return data;
}

//FOR PYTHON
//Turns of the accelerometer.
void accel_off(mma8451* accel) {
    mma8451_close(accel);
}

