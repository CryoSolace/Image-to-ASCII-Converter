from PIL import Image, ImageEnhance
import numpy as np
import os
from math import floor

max_size = 300

def toBW(arr):
    '''
    Converts an array with three values to black or white

        Parameters:
            arr (array): An array with 3 values
        
        Returns: 
            [1] or [0]: Array representation of white or black
    '''
    

    average = (int(arr[0]) + int(arr[1]) + int(arr[2]))/3
    if average >= 255: average -= 1 # Ensures never equal to 4

    return np.array(3 - floor(average/(255/4))) # Splits the values into 3, 2, 1, or 0 depending on the brightness in the resulting image

for f in os.listdir("test_images"):
    if f.endswith(".jpg"):
        i = Image.open(f'test_images\{f}')
        i = ImageEnhance.Contrast(i).enhance(5)
        i = ImageEnhance.Sharpness(i).enhance(0.1) 
        #i = i.filter(ImageFilter.GaussianBlur(radius = 0.5))
        
        i.thumbnail((max_size,max_size))
        i = i.convert("L") # First converts to greyscale by luminosity
        fn, fext = os.path.splitext(f)

        rgbArr = np.array(i)
        bwArr = np.zeros((int(len(rgbArr)),int(len(rgbArr[0])),1))
        
        for line in range(len(rgbArr)):
            for pixel in range(len(rgbArr[line])):
                val = rgbArr[line][pixel]
                # When converted, the image loses a dimension because of how .convert("L") works, so we put it into an array first.
                bwArr[line][pixel] = toBW(np.array([val,val,val]))
        
        #print(bwArr)
        output = [[] for _ in range(len(bwArr))] 
        palette = ".=;#"
        for line in range(len(bwArr)): # Line here a two dimensional array, with each array as a row and each value in the array as a pixel value
            for pixel in range(len(bwArr[line])):
                output[line] += palette[int(bwArr[line][pixel])]

                # ^ More succinct version of: 
                # if bwArr[line][pixel] == 0: output[line] += "."
                # elif bwArr[line][pixel] == 1: output[line] += "="
                # elif bwArr[line][pixel] == 2: output[line] += ";"
                # elif bwArr[line][pixel] == 3: output[line] += "#"

        for i in output:
            temp = ""
            for j in i:
                temp += str(j)
            print(temp)


