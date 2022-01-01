""""
Neuronal Systems Lab, Centre for Neural and Cognitive Science, University of Hyderabad, India
Principal Investigator: Dr Joby Joseph
Work by: B S Ullas Kannnatha, Summer Research Fellow, 2021
********************** Code for close loop Experiment *****************************
"""

# luma.led_matrix source code: https://github.com/rm-hull/luma.led_matrix
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas       # To control individual LEDs in the matrix

# Uncomment below code if you want the time in "HH:MM:SS.ffffff"
# from datetime import datetime

# This library gives us the time in seconds since epoch (January 1, 1970, 00:00:00 (UTC))
import time

# Select is used to check whether there is value at the input port
import select

# Used to to habndle binary data stored in files
import struct
import math         # For using "floor" and "abs"
import random

# Setting up the device
serial = spi(port=0, device=0, gpio=noop())
# Change the number of "cascaded" more than one LED matrix daisy chained
device = max7219(serial, cascaded=1, block_orientation=0, rotate= 0, blocks_arranged_in_reverse_order=False)
# Set the contrast for the device. Here it is set very low
device.contrast(8)

# Open the file in which the mouse senor and time needs to be written
Closed_Loop = open("Closed_Loop.txt", "w")

# Variable declaration
j = 0
experiment_duration = 60
rand_perturbation = 5
num = 0

# Set the starting time of the experiment
Start_time = time.time()

while (time.time()-Start_time) < experiment_duration:

    # Mouse is connected to Raspberry pi Model 3B+ USB port
    # "/dev/input" hold input device files
    # Reading the mouse values as binary
    Input_f = open("/dev/input/mice", "rb")

    # If there is no value at the input we cannot use f.read()
    # If f.read() is used, it waits till some values is read
    # Checking if there is any value at USB input
    poll_object = select.poll()
    poll_object.register(Input_f, select.POLLIN) # "POLLIN" checks data availability for read
    poll_event = poll_object.poll(10)            # 10 is time
    # https://pythontic.com/modules/select/poll

    if poll_event == []:                         # [] -> No value at the USB input port
        Closed_Loop.write(str(0))
        Closed_Loop.write("\n")
        Closed_Loop.write(str(time.time()))
        Closed_Loop.write("\n")
    else:
        data = Input_f.read(3)
        val = struct.unpack('3b', data)  # Unpacking bytes to integers
        # val is in the form: (Mouse button value, x coordinate, y coordinate)
        # https://thehackerdiary.wordpress.com/2017/04/21/exploring-devinput-1/

        # Sensor movement direction and LED movement direction are opposite
        if(val[1]>0):                            # Considering only x coordinate
            j = j-1
        else:
            j = j+1
            
        # Generating random perturbatiion
        # Choose the value of (%)random number range after trying some tries
        while (math.floor(abs((time.time() - Start_time))) % random.randint(10, 60) == 0) and num < rand_perturbation:
            j = random.randint(0, 8)            # Change this range if more matrix are daisy chained
            num += 1
            

        # Uncomment others if you need 2 or 3 vertical bar of LED
        with canvas(device) as draw:
            draw.point((0+j, 0), fill="red")   # (0+j, 0 ) is the address of a LED
                #draw.point((1+j,0), fill="red")
                #draw.point((2+j,0), fill="red")
                
            draw.point((0+j, 1), fill="red")
                #draw.point((1+j,1), fill="red")
                #draw.point((2+j,1), fill="red")
                
            draw.point((0+j, 2), fill="red")
                # draw.point((1+j,2), fill="red")
                # draw.point((2+j,2), fill="red")
           
            draw.point((0+j, 3), fill="red")
                # draw.point((1+j,3), fill="red")
                # draw.point((2+j,3), fill="red")
               
            draw.point((0+j, 4), fill="red")
                #draw.point((1+j,4), fill="red")
                #draw.point((2+j,4), fill="red")
                    
            draw.point((0+j, 5), fill="red")
                #draw.point((1+j,5), fill="red")
                #draw.point((2+j,5), fill="red")
                
            draw.point((0+j, 6), fill="red")
                #draw.point((1+j,6), fill="red")
                #draw.point((2+j,6), fill="red")
                  
            draw.point((0+j, 7), fill="red")
                #draw.point((1+j,7), fill="red")
                #draw.point((2+j,7), fill="red")

            Closed_Loop.write(str(val[1]))
            Closed_Loop.write("\n")
            Closed_Loop.write(str(time.time()))
            Closed_Loop.write("\n")

Input_f.close()
Closed_Loop.close()
print("Experiment Ended")
# ************************************** End **************************************



