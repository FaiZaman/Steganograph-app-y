import cv2
import math
import random
import numpy as np
from datetime import datetime
from utility import message_to_binary, integer_to_binary, binary_to_string, save_image, save_message

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

        self.time_string = "{:%Y_%m_%d_%H;%M}".format(datetime.now())


    # takes the coordinates of current pixel and returns a two-pixel block based on PVD img traversal
    def get_pixel_block(self, x, y):

        current_pixel = self.image[y][x]
        next_pixel = None

        if y % 2 == 0:  # going right

            if x < self.width - 1:      # keep going right if the end of image is not reached
                x += 1
                next_pixel = self.image[y][x]

            else:      # go down a row
                y += 1
                next_pixel = self.image[y][x]

        else:   # going left

            if x > 0:   # keep going left if the end of image is not reached
                x -= 1
                next_pixel = self.image[y][x]

            else:       # go down a row
                y += 1
                next_pixel = self.image[y][x]

        block = (x, y), (current_pixel, next_pixel)
        return block
    

    # the calculation to embed the bits into the block based on the difference values
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

        all_data_embedded = False
        for index in path:

            # get pixel coordiantes based on index
            x = index % self.width
            y = index // self.width

            # compute the two-pixel block and the coordinates of the next pixel with difference val
            next_coordinates, block = self.get_pixel_block(x, y)
            next_x = next_coordinates[0]
            next_y = next_coordinates[1]

            difference_value = abs(int(block[1]) - int(block[0]))

            # get the lower and upper bound of the range that the difference falls into
            lower_key = 0
            for lower, upper in self.ranges.items():

                if lower <= difference_value <= upper:
                    lower_key = lower
                    break
            
            # calculate range width and check if the block causes fall off
            upper = self.ranges[lower_key]
            range_width = upper - lower_key + 1
            fall_off = self.check_fall_off(block, upper - difference_value, difference_value)

            if not fall_off:

                # get the number of bits that can be embedded in this block based on range width
                num_bits = int(math.log(range_width))
                new_message_index = message_index + num_bits

                # check for the index surpassing the whole message: if so, everything embedded
                if new_message_index > message_length:
                    all_data_embedded = True
                    new_message_index = message_length

                message_bits = self.message[message_index : new_message_index]

                # compute new difference as m & get the embedded block based off inverse calculation
                new_difference = lower_key + int(message_bits, 2)
                m = abs(new_difference - difference_value)

                # calculate new embedded block values and reassign to stego image
                embedded_block = self.inverse_calculation(block, m, difference_value)
                cover_image[y][x] = embedded_block[0]
                cover_image[next_y][next_x] = embedded_block[1]

                message_index = new_message_index   # increment index by num_bits

                if all_data_embedded or message_index == message_length:
                    break

        stego_image = cover_image
        save_image(self.save_path, self.image_name, self.time_string, stego_image)

