from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import os

size = (300,300)

def toBW(arr):
    '''
    Converts an array with three values to black or white

        Parameters:
            arr (array): An array with 3 values
        
        Returns: 
            [255,255,255] or [0,0,0] (np.array): Array representation of white or black, depending on if the average of the three are greater than 255/2 or not
    '''
    
    return np.array([255,255,255]) if (int(arr[0]) + int(arr[1]) + int(arr[2]))/3 >= 255/2 else np.array([0,0,0])

for f in os.listdir("test_images"):
    if f.endswith(".jpg"):
        i = Image.open(f'test_images\{f}')
        i = ImageEnhance.Contrast(i).enhance(10) 
        i = ImageEnhance.Sharpness(i).enhance(0.1)
        # i = i.filter(ImageFilter.GaussianBlur(radius = 0.5))
        # Contrast is the most important setting here.
        
        i.thumbnail(size)
        i = i.convert("L") # Finally converts to greyscale by luminosity

        fn, fext = os.path.splitext(f)

        rgbArr = np.array(i)
        bwArr = np.zeros((int(len(rgbArr)),int(len(rgbArr[0])),3))
        
        for line in range(len(rgbArr)):
            for pixel in range(len(rgbArr[line])):
                val = rgbArr[line][pixel]
                # When converted, the image loses a dimension because of how .convert("L") works, so we put it into an array first.
                bwArr[line][pixel] = toBW(np.array([val,val,val]))

        i = Image.fromarray((bwArr).astype(np.uint8))
        i.save(f'output_images\{fn}_ToBW2{fext}')


for f in os.listdir("output_images"):
    if f.endswith(".jpg"):
        i = Image.open(f'output_images\{f}')
        fn, fext = os.path.splitext(f)
        print(f"{fn}{fext} has been created successfully in output_images.")

        