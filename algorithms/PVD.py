import cv2
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

        # set PseudoRandom Number Generator seed as the secret key
        random.seed(key)


    def encode(self):

        self.message = message_to_binary(self.message)
        message_index = 0
        message_length = len(self.message)

        if message_length > self.num_bytes:
            raise ValueError("The message is too large for the image.")

        cover_image = self.image  # so image is not modified
        x = y = 0

        while True:

            current_pixel = cover_image[y][x]

            if y % 2 == 0:  # going right

                if x < self.width - 1:
                    x += 1
                    next_pixel = cover_image[y][x]

                else:

                    if y == self.height - 1:
                        break

                    y += 1
                    next_pixel = cover_image[y][x]


            else:   # going left

                if x > 0:
                    x -= 1
                    next_pixel = cover_image[y][x]

                else:
                    y += 1
                    next_pixel = cover_image[y][x]
