from PIL import Image, ImageEnhance
import numpy as np
import os

max_size = 500

binToBraille = { # Dictionary for converting binary to braille.
    "000000":"⠠",

    "100000":"⠁",
    "010000":"⠂",
    "001000":"⠄",
    "000100":"⠈",
    "000010":"⠐",
    "000001":"⠠",

    "110000":"⠃",
    "101000":"⠅",
    "100100":"⠉",
    "100010":"⠑",
    "100001":"⠡",
    "011000":"⠆",
    "010100":"⠊",
    "010010":"⠒",
    "010001":"⠢",
    "001100":"⠌",
    "001010":"⠔",
    "001001":"⠤",
    "000110":"⠘",
    "000101":"⠨",
    "000011":"⠰",

    "111000":"⠇",
    "110100":"⠋",
    "110010":"⠓",
    "110001":"⠣",
    "101100":"⠍",
    "101010":"⠕",
    "101001":"⠥",
    "100110":"⠙",
    "100101":"⠩",
    "100011":"⠱",
    "011100":"⠎",
    "011010":"⠖",
    "011001":"⠦",
    "010110":"⠚",
    "010101":"⠪",
    "010011":"⠲",
    "001110":"⠜",
    "001101":"⠬",
    "001011":"⠴",
    "000111":"⠸",

    "111100":"⠏",
    "111010":"⠗",
    "111001":"⠧",
    "110110":"⠛",
    "110101":"⠫",
    "110011":"⠳",
    "101110":"⠝",
    "101101":"⠭",
    "101011":"⠵",
    "100111":"⠹",
    "011110":"⠞",
    "011101":"⠮",
    "011011":"⠶",
    "010111":"⠺",
    "001111":"⠼",

    "111110":"⠟",
    "111101":"⠻",
    "111011":"⠷",
    "110111":"⠾",
    "101111":"⠯",
    "011111":"⠽",

    "111111":"⠿",

    #   Bits are ordered like so:
    #   "123456"
    #   1 4
    #   2 5
    #   3 6
}


def toBW(arr):
    '''
    Converts an array with three values to black or white

        Parameters:
            arr (array): An array with 3 values
        
        Returns: 
            1 or 0 (int): Integer representing white or black, depending on if the average is closer to 0 or 255.
    '''
    return 0 if ( int(arr[0]) + int(arr[1]) + int(arr[2]))/3 >= 255/2 else 1 # 0 and 1 may be interchanged here to produce the inverse (negative) effect.
    # Returns 1 or 0 depending on if it's closer to white or black

for f in os.listdir("test_images"):
    if f.endswith(".jpg"): # Loops through all test images for testing
        i = Image.open(f'test_images\{f}')
        i = ImageEnhance.Contrast(i).enhance(10)
        i = ImageEnhance.Sharpness(i).enhance(0.1)
        # Numbers above found by trial and error. Contrast is the most significant factor for the final output.

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

        bwArr = bwArr.tolist()

         # Fixes how every value was in an array and as a float for some reason
        newArr = [[] for _ in range(int(len(bwArr)))]
        for row in range(len(bwArr)):
            for arr in bwArr[row]:
                newArr[row].append(int(arr[0]))
       
        bwArr = newArr

        # Converts the array so that the number of rows and columns can be converted into the 3x2 braille equivalent
        if len(bwArr[0]) % 2 != 0:
            for line in range(len(bwArr)):
                bwArr[line] += [0]
        if len(bwArr) % 3 != 0:
            for line in range(3 - len(bwArr) % 3):
                bwArr.append([0] * int(len(bwArr[0])))
        


        # Very resource expensive iteration to go through each group of 3x2 pixels and convert into a string of binary.
        binOutput = [[] for _ in range(int(len(bwArr)/3))]
        for rowTriplet in range(int(len(bwArr)/3)):
            for colDuplet in range(int(len(bwArr[0])/2)):
                stringPush = ""
                for col in range(2):
                    for row in range(3):
                        stringPush += str(bwArr[3*rowTriplet + row][2*colDuplet + col])       
                binOutput[rowTriplet].append(stringPush)

        # Braille conversion from the binary string.
        output = [[] for _ in range(int(len(binOutput)))]
        for row in range(len(binOutput)):
            for num in binOutput[row]:
                output[row].append(binToBraille[str(num)])

        
        # Prints final output    
        for i in output:
            temp = ""
            for j in i:
                temp += str(j)
            print(temp) 
        

        print(f"{fn}{fext} printed successfully.")
        

