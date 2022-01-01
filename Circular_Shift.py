from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas  
from collections import deque
import collections

# Setting up the device
serial = spi(port=0, device=0, gpio=noop())
# Change the number of "cascaded" more than one LED matrix daisy chained
device = max7219(serial, cascaded=1, block_orientation=180, rotate= 0, blocks_arranged_in_reverse_order=True)
# Set the contrast for the device. Here it is set very low
device.contrast(8)


k=-1
A = [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1]
a = deque(A)
a.rotate(4)
A = list(collections.deque(a))
with canvas(device) as draw:
    for i in range(8):
        for j in range(8):
            k=k+1
            if A[k]==1:
                draw.point((i,j),fill="red")
                
                
            
    
    
#     for j in range(0,8):
#         for k in range(0,8):
#             draw.point((j, 0), fill="red")   # (0+j, 0 ) is the address of a LED
