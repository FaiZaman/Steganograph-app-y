"""
Least Significant Bit Matching (LSBM) embedding & extraction algorithm
The same as LSB algorithm, but if the pixel value does not match the message bit
its entire value is incremented or decremented
"""

from algorithms.LSB import LSB
import random
import numpy as np

class LSBM(LSB):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)
        self.name = 'LSBM'


    # randomly add or subtract 1 from pixel value as not equal
    def random_increment_or_decrement(self, pixel):

        # generate random number and convert pixel value to integer for easier add/minus
        random_number = random.random()

        # edge cases
        if pixel == 255:
            return 254
        if pixel == 0:
            return 1

        if random_number < 0.5:     # subtract
            pixel += 1
        else:
            pixel -= 1      # add
        
        return pixel


    # embed a bit of the data into the Least Significant Bit of the cover image's current pixel
    def embed_pixel(self, binary_pixel, message_index):

        bit = self.message[message_index]
        pixel = int(binary_pixel, 2)

        # randomly add or subtract 1 from pixel value as not equal
        if binary_pixel[-1] != bit:

            pixel = self.random_increment_or_decrement(pixel)

        return pixel
