from algorithms.LSB import LSB
import numpy as np
import random

class LSBM(LSB):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)


    # embed a bit of the data into the Least Significant Bit of the cover image's current pixel
    def embed_pixel(self, binary_pixel, message_index):

        bit = self.message[message_index]
        integer_pixel = int(binary_pixel, 2)

        # randomly add or subtract 1 from pixel value as not equal
        if binary_pixel[-1] != bit:

            # generate random number and convert pixel value to integer for easier add/minus
            random_number = random.random()

            if random_number < 0.5:     # subtract
                integer_pixel += 1
            else:
                integer_pixel -= 1      # add

        return integer_pixel
