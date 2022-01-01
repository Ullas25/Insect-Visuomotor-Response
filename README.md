# Virtual Arena to Investigate Bee Visuomotor Response

**This work is carried out under the guidance of Dr. Joby Joseph in the [Neuronal Systems Lab](https://sites.google.com/site/nsyslabcncs/research), Center for Neural and Cognitive Sciences, University of Hyderabad, India.**

Virtual Arenas used to understand the insect visuomotor response are generally complex and expensive. Insect Neurophysiology has been studied using LED virtual arena. The existing system uses multiple hardware boards to control the feedback and therefore increasing the complexity of the system. One approach is to use a hardware board to receive the incoming signal, use another hardware board to do the necessary computation and finally a hardware to send the feedback signal to the LED driver. This usage of multiple hardware might increase the time of feedback communication. The speed of the system comes down to the efficient hardware system. Here we have worked on a low price, fast closed-loop LED virtual arena. This system is not only inexpensive but also simple. The proposed system can be used to understand the neural underpinnings of bee visuomotor response. Our system uses only a microcomputer (Raspberry pi) to receive the incoming signal, perform necessary computation and send the feedback signal to the LED driver to control the arena, saving the time of communication.

## Hardware setup
![image](https://user-images.githubusercontent.com/46472021/147846047-5f83831c-0eea-4fca-ad59-5f7916396f8c.png)


The experiment setup is as follows: Logitech wired mouse is used as an optical sensor. This mouse is connected to the USB port of the Raspberry pi model B+. Raspberry pi is a small-sized, high-performance computer developed by the Raspberry Pi Foundation. All the necessary computation is done in the pi alone. Raspberry Pi OS (also known as Raspbian) is the operating system used. The pi sends the data to the MAX7219 driver, which will drive the LEDs by sending the appropriate signal. The program to control the system is written in python using Thonny IDE. Pi can be directly connected to a monitor using the right HDMI cable. We also can connect the keyboard and mouse to pi. In this project, I used a windows laptop as a monitor, keyboard and touchpad using VNC Viewer. Ethernet cable is used to connect the laptop to pi. We can connect a number of 8 * 8 LED matrxi together to form a circular LED arena.

## Algorithm

### Closed-loop system

***Closed_Loop.py: The code for closed loop system***

In a closed-loop system, the LED bar is moved in relation to mouse sensor movement. The mouse sensor value should be collected and timestamped for analysis in a file. The program should randomly move the LED bar for a given number of times after a certain time interval.
1. Firstly, we need to import all the libraries that are needed for the closed-loop experiment. Installation of the libraries is discussed in Appendix B. We import luma.led_matrix library which allows us to interface MAX7219 driver with Raspberry pi. It provides the ability to draw patterns on a LED matrix.
    
    We also import libraries for time stamping, to generate random numbers, to use math operations and to monitor the I/O function.

2. We then set up Serial Peripheral Interface (SPI) using luma.led_matrix library. Before doing this, we need to make sure that we have enabled SPI in raspberry pi. The procedure for enabling SPI Appendix C. We then set up the device by choosing the required parameters. 
def __init__(self, serial_interface=None, width=8, height=8, cascaded=None, rotate=0, block_orientation=0, blocks_arranged_in_reverse_order=False, contrast=0x70, ** kwargs)
    
    These are the parameters that can be initialized in MAX7219. We can set the device height and width or we can leave it to default. If multiple devices are cascaded together, we can specify the number and then all the matrix is considered as one matrix. We can specify the orientation of the matrix. The values it can take is 0, 90, 180 and -90 degrees. We can set the LED intensity from 0-255.

3.	As we need to write the mouse values into a file, we open the file in the beginning in write mode. This file will be created in the root directory.

4.	We then initialize all the variables. We should specify the experiment duration and number of random perturbations.

5.	To get the time and keep track of the time we are using time.time() from the time library. This function returns the time in milliseconds since the epoch (January 1, 1970, 00:00:00 (UTC)). In the beginning, we take the time and initialize it to Start_time variable to keep track of the time.

6.	While loop keeps track of time by constantly subtracting the current time with start and then checking whether this is less than the experiment time initialized earlier.

7.	We can easily read the mouse value that is connected to the USB port of pi using this command “/dev/input/mice”. We read the mouse value as a binary file.

    When there are no values at the input, we want to store zero (“0”) in the file. If we try to read the values at the input using the file.read(), it waits till some value is read, halting the program execution. Before proceeding further, we check whether there are any values at the pi USB input port using the poll method. Using a poll, the I/O event can be registered for a descriptor. Using select (), numbers of descriptors can be monitored. 

    Firstly we choose the polling object using select.poll(). Then we set the rate at which it has to be polled. If there are no values at the poll the returned value will be empty ([]). On the other hand, if there are some values at the input port and some value is returned. We use the if statement to check whether polling has returned some value or not. If there is no value then, the value “0” is stored in the file with the current time. If there is some value, the value is read (file.read(3)). As this data is in byte format, we unpack it into integers. The returned value is in the form of, (Mouse button value, x coordinate, y coordinate). 

8.	We are only concerned with x coordinate. So, we move ahead with the first returned coordinate. The “x” coordinate is positive in one direction and negative in the other.
As the LEDs in the matrix are in the form of coordinates. We can control the LED movement by incrementing or decrementing the coordinates. We change the j value, which is the column number with respect to the mouse movement direction. If the mouse moves in one direction we increment and we decrement the column value if it moves in the other direction.

9.	It is known that when the experiment is conducted there is a chance that the insect might fixate on the bar and not change its fixation. Through observation, we might have a rough idea of fixation time. To move ahead with the experiment, we disturb the LED matrix after a certain interval by moving the LED bar in a random direction. 

    A random value is generated by keeping track of the time elapsed and then take modulus (%) of it with a random value and comparing it with 0. The time interval of this random value can be controlled by setting the appropriate random value range. For example, if the random value range is (10, 20), the random value is generated only after 10s. This is because the math.floor(abs((time.time() - Start_time))) % random.randint(10, 60) == 0 might become zero only after 10 seconds.

10.	Then we control the LED lighting by considering each LED as a point. There are two values to this point, one is the row value while the other is the column value. In this project we want the bar of LED to move as a bar of LED so we keep the row value constant but we vary column value.

11.	We store the x coordinate value and time in a file.

12.	Finally, we close all the open files.

### Open Loop

***Open_Loop.py: Code for open loop system***

In the open-loop system, the LED movement is independent of mouse sensor value. LED is moved randomly and the mouse sensor response is stored with its timestamp. The code for open-loop is similar to Closed Loop. The only difference is mouse sensor reading code and LED movement code is independent.

We need to randomly choose which columns of the LED matrix has to be lighted randomly. This is achieved by j = random.randint(0, 7). We also need to choose the time at which the bar of light has to be lighted. This is achieved by if (iteration_passed % delay_iteration) == 0. iteration_passed is incremented with each iteration and delay_iteration is initialized in the beginning. Whenever the iteration_time is a multiple of delay_iteration, the loop is executed, lighting the LED.

### Any pattern movement

***Circular_Shift.py: Code for any pattern movement***

When the experiment contains 7 other LED matrices, we need to have the ability to control each one of them. If we can control a given pattern in one matrix, we would have the ability to control all 8 LED matrices. 
This control is achieved by circular shifting the pattern of a matrix in a clockwise or anticlockwise direction. The libraries imported are similar to that of the open-loop or closed-loop experiment. The required pattern is in the form of an array (64 length). This 64 is the number of LEDs in a given matrix.
The value of the mouse value read is used to set the direction circular shift of the LED. If the mouse sensor value is less than 0 the LED the circular shift direction is set to the left by setting dir to -1. On the other hand, if the sensor value is greater than 0 the circular shift direction is set to the right by setting dir to +1.

1. We want the LED pattern to move in a snake-like pattern. So, we have to change the row value at the values are circular shifting. This is done when the shift has completed one row. For example, when the circular shift has reached the last row of the first column, then the next position of the circular shift has to last row second column next last but one-row second column.

2.	We then compare each element of a given pattern in the form of an array. If it's “1” the LED that particular LED is lighted. On the other hand, if it's “0” the LED is not switched on.

3.	The next position of the last LED of the last column is the first LED of the first column

## Results

When the mouse moves the LED bar should also move in the direction of sensor movement. By calculating the delay in LED movement with respect to mouse movement we get the response time of the system. The dealy is found by calculating the cross-correlation between the two sets of pixels of interest (Pixels of LED lighting and pixels of the mouse). The result of the cross-correlation is given below. 

![image](https://user-images.githubusercontent.com/46472021/147846373-2cbd3046-fcbe-440b-9eae-eb3c87a4a0f0.png)

In the above figure, the first plot is of LED bar pixels over different frames, the second plot is of mouse wire pixels over frames and the final plot is of the velocity of the LED bar and mouse wire. Here we can see the difference in the velocity. Cross-correlation between filtered LED pixels and mouse wire pixels is found. ***The delay was 1 frame and the video FPS was 20. So the response time of the system is 50ms.***


To check how the system might perform when used for the actual Bee Visuomotor experiment we collected fast mouse senor movement data for about 3 minutes. The time it took to light up the LED bar from one mouse sensor value to the other is calculated and stored along with the sensor value. Our goal here is to find the response time of the system. We find the response time by analysing the data that we stored in the file. The response time is also calculated by video analysis. This validates the response time value.
We performed fast mouse sensor movement for various time duration and calculated the mean response time. Initially, the mouse sensor value and timestamp were stored in a .txt file. Later the values were copied into an excel workbook (.xlsx) and used for data analysis. The values were sored with a column named “Values”. The mouse sensor value is stored first and in the next row, its timestamp is stored.

![image](https://user-images.githubusercontent.com/46472021/147846405-ed7c4369-b6f7-4649-aa28-c06ee840abb0.png)

Above is the code of Data Analysis

![image](https://user-images.githubusercontent.com/46472021/147846443-2b505456-f1ac-4c83-bda0-9ee52b77fce8.png)

The result of the analysis of four trials is given below. The minimum response time of the four trials is 33.2508, 37.9924, 31.5463 and 33.9717 milliseconds respectively. No. of values read is the number of mouse sensor values read.
