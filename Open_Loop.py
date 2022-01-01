""""
Neuronal Systems Lab, Centre for Neural and Cognitive Science, University of Hyderabad, India
Principal Investigator: Dr Joby Joseph
Work by: B S Ullas Kannnatha, Summer Research Fellow, 2021
********************** Code for open loop Experiment *****************************
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

import random

# Setting up the device
serial = spi(port=0, device=0, gpio=noop())
# Change the number of "cascaded" more than one LED matrix daisy chained
device = max7219(serial, cascaded=1, block_orientation=0, rotate=0, blocks_arranged_in_reverse_order=False)
# Set the contrast for the device. Here it is set very low
device.contrast(8)

# Open the file in which the mouse senor and time needs to be written
Open_Loop = open("Open_loop.txt", "w")

# Variable declaration
j = 0
experiment_duration = 30
delay_iteration = 25             # Not in seconds. Find right value by trial and error
iteration_passed = 0

# Set the starting time of the experiment
Start_time = time.time()

while time.time()-Start_time < experiment_duration:
    j = random.randint(0, 7)                   # LED is moved randomly

    # Setting delay for random movement of LED using if statement
    # Not using time.sleep() bcz it delays mouse value writing
    if (iteration_passed % delay_iteration) == 0:

        # Uncomment others if you need 2 or 3 vertical bar of LED
        with canvas(device) as draw:
            draw.point((0 + j, 0), fill="red")  # (0+j, 0 ) is the address of a LED
            # draw.point((1+j,0), fill="red")
            # draw.point((2+j,0), fill="red")

            draw.point((0 + j, 1), fill="red")
            # draw.point((1+j,1), fill="red")
            # draw.point((2+j,1), fill="red")

            draw.point((0 + j, 2), fill="red")
            # draw.point((1+j,2), fill="red")
            # draw.point((2+j,2), fill="red")

            draw.point((0 + j, 3), fill="red")
            # draw.point((1+j,3), fill="red")
            # draw.point((2+j,3), fill="red")

            draw.point((0 + j, 4), fill="red")
            # draw.point((1+j,4), fill="red")
            # draw.point((2+j,4), fill="red")

            draw.point((0 + j, 5), fill="red")
            # draw.point((1+j,5), fill="red")
            # draw.point((2+j,5), fill="red")

            draw.point((0 + j, 6), fill="red")
            # draw.point((1+j,6), fill="red")
            # draw.point((2+j,6), fill="red")

            draw.point((0 + j, 7), fill="red")
            # draw.point((1+j,7), fill="red")
            # draw.point((2+j,7), fill="red")

    iteration_passed += 1
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
        Open_Loop.write(str(0))
        Open_Loop.write("\n")
        Open_Loop.write(str(time.time()))
        Open_Loop.write("\n")
    else:
        data = Input_f.read(3)
        val = struct.unpack('3b', data)  # Unpacking bytes to integers
        # val is in the form: (Mouse button value, x coordinate, y coordinate)
        # https://thehackerdiary.wordpress.com/2017/04/21/exploring-devinput-1/
        Open_Loop.write(str(val[1]))
        Open_Loop.write("\n")
        Open_Loop.write(str(time.time()))
        Open_Loop.write("\n")
    
        
Input_f.close()
Open_Loop.close()
print("Experiment Ended")
# ************************************** End **************************************