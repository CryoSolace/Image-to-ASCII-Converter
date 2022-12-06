from PIL import Image
import numpy as np
import os

# size = (300,300)

def toBW(arr):
    '''
    Converts an array with three values to black or white

        Parameters:
            arr (array): An array with 3 values
        
        Returns: 
            [255,255,255] or [0,0,0] (np.array): Array representation of white or black, depending on if the average of the three are greater than 255/2 or not
    '''
    
    return np.array([255,255,255]) if (int(arr[0]) + int(arr[1]) + int(arr[2]))/3 >= 255/2 else np.array([0,0,0])


for f in os.listdir("test_images"): # This is the directory where the script will search in.
    if f.endswith(".jpg"): # Checks through each test image ending in jpg.

        i = Image.open(f'test_images\{f}')
        fn, fext = os.path.splitext(f) # File name, File extension

        rgbArr = np.array(i)
        bwArr = np.zeros((int(len(rgbArr)),int(len(rgbArr[0])),3)) # Initialise the bwArr array to be saved, is currently a numpy array of only zeros
        
        for line in range(len(rgbArr)):
            for pixel in range(len(rgbArr[line])):
                bwArr[line][pixel] = toBW(rgbArr[line][pixel])
        # runs the toBW function on each pixel and alters the value inside each pixel in bwArr

        i = Image.fromarray((bwArr).astype(np.uint8)) # Quick fix
        i.save(f'output_images\{fn}_toBW1{fext}') 
 

for f in os.listdir("output_images"):
    if f.endswith(".jpg"):
        i = Image.open(f'output_images\{f}')
        fn, fext = os.path.splitext(f)
        print(f"{fn}{fext} has been created successfully in output_images.")
