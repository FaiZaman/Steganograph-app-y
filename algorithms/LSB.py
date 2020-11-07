import cv2
import numpy as np
from utility import message_to_binary, binary_to_string

class LSB():

    def __init__(self, cover, message, key):

        self.cover = cover
        self.delimiter = "-----"
        self.message = message + self.delimiter
        self.key = key



    def encode(self):

        width = np.size(self.cover, 1)
        height = np.size(self.cover, 0)
        num_bytes = width * height * 3   # 3 colour channels

        message_length = len(self.message)

        # loop through image pixels
        for x in range(0, width):
            for y in range(0, height):

                pixel = self.cover[y][x]
                print(pixel)
                r, g, b = message_to_binary(pixel)
                print(r, g, b)
                break