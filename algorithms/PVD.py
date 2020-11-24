import cv2
import math
import random
import numpy as np
from utility import message_to_binary, integer_to_binary, binary_to_string


class PVD():

    def __init__(self, image, message, key, save_path):

        self.image_name = image[0]
        self.image = image[1]
        self.message = message
        self.key = key
        self.save_path = save_path

        # get dimensions of image
        self.width = np.size(self.image, 1)
        self.height = np.size(self.image, 0)
        self.num_bytes = self.width * self.height   # total number of pixels in image

        self.ranges = {     # difference value ranges
            0: 7,
            8: 15,
            16: 31,
            32: 63,
            64: 127,
            128: 255
        }

        # set PseudoRandom Number Generator seed as the secret key and generate list of pixel indices
        random.seed(key)
        self.pixels = [i for i in range(0, self.num_bytes - 1)]     # [0, 1, 2, ..., num_pixels]


    # takes the coordinates of current pixel and returns a two-pixel block based on PVD img traversal
    def get_pixel_block(self, x, y):

        current_pixel = self.image[y][x]
        next_pixel = None

        if y % 2 == 0:  # going right

            if x < self.width - 1:      # keep going right if the end of image is not reached
                next_pixel = self.image[y][x + 1]

            else:      # go down a row
                next_pixel = self.image[y + 1][x]

        else:   # going left

            if x > 0:   # keep going left if the end of image is not reached
                next_pixel = self.image[y][x - 1]

            else:       # go down a row
                next_pixel = self.image[y + 1][x]

        block = (current_pixel, next_pixel)
        return block
    

    def inverse_calculation(self, block, m, difference):

        half_m = m / 2
        ceiling_m = math.ceil(half_m)
        floor_m = math.floor(half_m)

        if difference % 2 == 0:
            embedded_block = (block[0] - floor_m, block[1] + ceiling_m)
        else:
            embedded_block = (block[0] - ceiling_m, block[1] + floor_m)

        return embedded_block


    # check that the block chosen stays within the range [0, 255] after embedding
    def check_fall_off(self, block, upper, difference):

        m = upper - difference
        embedded_block = self.inverse_calculation(block, m, difference)

        if embedded_block[0] < 0 or embedded_block[0] > 255 or\
            embedded_block[1] < 0 or embedded_block[1] > 255:

            return True
        
        return False


    def encode(self):

        self.message = message_to_binary(self.message)
        message_index = 0
        message_length = len(self.message)

        if message_length > self.num_bytes:
            raise ValueError("The message is too large for the image.")

        # get a random path based on seed through the pixels
        path = random.sample(self.pixels, self.num_bytes - 1)
        cover_image = self.image  # so image is not modified
        x = y = 0

        for index in path:

            # get pixel coordiantes based on index
            x = index % self.width
            y = index // self.width

            block = self.get_pixel_block(x, y)
            difference_value = abs(block[1] - block[0])
                
            #fall_off = self.check_fall_off(block, upper, difference_value)