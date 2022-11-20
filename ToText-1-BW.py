from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import os

max_size = 300

def toBW(arr):
    '''
    Converts an array with three values to black or white

        Parameters:
            arr (array): An array with 3 values
        
        Returns: 
            [1] or [0]: Array representation of white or black
    '''
    return np.array([1]) if ( int(arr[0]) + int(arr[1]) + int(arr[2]))/3 >= 255/2 else np.array([0]) 
    # Returns 1 or 0 depending on if it's closer to white or black

for f in os.listdir("test_images"):
    if f.endswith(".jpg"):
        i = Image.open(f'test_images\{f}')
        i = ImageEnhance.Contrast(i).enhance(5)
        i = ImageEnhance.Sharpness(i).enhance(0.1)
        #i = i.filter(ImageFilter.GaussianBlur(radius = 0.5)) # doesnt work too well
        i.thumbnail((max_size,max_size))
        i = i.convert("L") # Converts to greyscale by luminosity

        fn, fext = os.path.splitext(f)

        rgbArr = np.array(i)
        bwArr = np.zeros((int(len(rgbArr)),int(len(rgbArr[0])),1))
        
        for line in range(len(rgbArr)):
            for pixel in range(len(rgbArr[line])):
                val = rgbArr[line][pixel]
                # When converted, the image loses a dimension because of how .convert("L") works, so we put it into an array first.
                bwArr[line][pixel] = toBW(np.array([val,val,val]))
        
        
        output = [[] for _ in range(len(bwArr))] # The final string to be printed

        for line in range(len(bwArr)): 
            # Line here a two dimensional array, with each array as a row and each value in the array as a pixel value
            for pixel in range(len(bwArr[line])):
                # Adds . or # to the output depending on if closer to black or white
                if bwArr[line][pixel] == 1: output[line] += "." 
                else: output[line] += "#"


        # Prints final output
        for i in output:
            temp = ""
            for j in i:
                temp += str(j)
            print(temp) 


