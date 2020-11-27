import os
import random
import numpy as np
from datetime import datetime
from utility import message_to_binary, integer_to_binary, binary_to_string, save_image, save_message

class LSB():

    def __init__(self, image, message, key, save_path):

        self.image_name = image[0]
        self.image = image[1]
        self.delimiter = "-----"
        self.message = message + self.delimiter
        self.save_path = save_path

        # get dimensions of image
        self.width = np.size(self.image, 1)
        self.height = np.size(self.image, 0)
        self.num_bytes = self.width * self.height   # total number of pixels in image

        # set PseudoRandom Number Generator seed as the secret key and generate list of pixel indices
        random.seed(key)
        self.pixels = [i for i in range(0, self.num_bytes)]     # [0, 1, 2, ..., num_pixels]

        self.time_string = "{:%Y_%m_%d_%H;%M}".format(datetime.now())


    # embed a bit of the data into the Least Significant Bit of the cover image's current pixel
    def embed_pixel(self, binary_pixel, message_index):

        # adding 0 or 1 (message bit) to LSB of pixel and reassigning
        bit = self.message[message_index]
        binary_pixel_msb = binary_pixel[:-1]
        embedded_pixel = binary_pixel_msb + bit
        embedded_pixel = int(embedded_pixel, 2)

        return embedded_pixel


    def encode(self):

        # convert message to binary
        self.message = message_to_binary(self.message)
        message_index = 0
        message_length = len(self.message)

        if message_length > self.num_bytes:
            raise ValueError("The message is too large for the image.")

        # get a random path based on seed through the pixels
        path = random.sample(self.pixels, message_length)
        cover_image = self.image    # so image is not modified

        # loop through image pixels in pseudorandom order based on secret key
        for index in path:

            # get pixel coordinates based on index
            x = index % self.width
            y = index // self.width

            # assign, retrieve, and convert RGB values
            pixel = cover_image[y][x]
            embedded_pixel = pixel
            binary_pixel = integer_to_binary(pixel)

            # embed data within current pixel
            embedded_pixel = self.embed_pixel(binary_pixel, message_index)

            # reassign embedded pixel to cover image
            cover_image[y][x] = embedded_pixel
            message_index += 1

        # reassign and save image
        stego_image = cover_image
        save_image(self.save_path, self.image_name, self.time_string, stego_image)


    def decode(self):

        # initialise binary message and get a random path based on seed through the pixels
        binary_message = ""
        path = random.sample(self.pixels, self.num_bytes)

        # loop through image pixels
        for index in path:

            # get pixel coordinates based on index
            x = index % self.width
            y = index // self.width

            # assign, retrieve, convert, and append LSBs to binary message
            stego_pixel = self.image[y][x]
            binary_pixel = integer_to_binary(stego_pixel)
            binary_message += binary_pixel[-1]

        # extract the original message, save to file, and return
        extracted_message = binary_to_string(binary_message, self.delimiter)
        save_message(self.save_path, self.time_string, extracted_message)

        return extracted_message
