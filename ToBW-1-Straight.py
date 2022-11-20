from PIL import Image
import numpy as np
import os

size_300 = (300,300)

def toBW(arr):
    '''
    Converts an array with three values to black or white

        Parameters:
            arr (array): An array with 3 values
        
        Returns: 
            [255,255,255] or [0,0,0]: Array representation of white or black
    '''
    
    return np.array([255,255,255]) if (int(int(arr[0])) + int(int(arr[1])) + int(int(arr[2])))/3 >= 255/2 else np.array([0,0,0])


for f in os.listdir("test_images"):
    if f.endswith(".jpg"): # Just checks through each test image ending in jpg

        i = Image.open(f'test_images\{f}')
        print(np.array(i))
        fn, fext = os.path.splitext(f)

        rgbArr = np.array(i)
        bwArr = np.zeros((int(len(rgbArr)),int(len(rgbArr[0])),3)) # initialise the bwArr array to be saved
        
        print(type(bwArr), type(rgbArr)) 
        for line in range(len(rgbArr)):
            for pixel in range(len(rgbArr[line])):
                bwArr[line][pixel] = toBW(rgbArr[line][pixel])
        # runs the toBW function on each pixel and returns the value.

        i = Image.fromarray((bwArr).astype(np.uint8))
        i.save(f'output_images\{fn}_bw{fext}') 
 

for f in os.listdir("output_images"):
    if f.endswith(".jpg"):
        i = Image.open(f'output_images\{f}')
        print(i.height, i.width)
