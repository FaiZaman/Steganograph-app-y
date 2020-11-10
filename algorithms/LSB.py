import cv2
import os
import numpy as np
from datetime import datetime
from utility import message_to_binary, binary_to_string

class LSB():

    def __init__(self, image, message, key, save_path):

        self.image_name = image[0]
        self.image = image[1]
        self.delimiter = "-----"
        self.message = message + self.delimiter
        self.key = key
        self.save_path = save_path

        # get dimensions of image
        self.width = np.size(self.image, 1)
        self.height = np.size(self.image, 0)
        self.num_bytes = self.width * self.height * 3   # 3 colour channels

        self.time_string = "{:%Y_%m_%d_%H;%M}".format(datetime.now())


    def embed_pixel(self, pixel, colour, colour_index, message_index, message_length):

        # embed a bit of the data into the Least Significant Bit of the cover image's current pixel
        if message_index < message_length:
            bit = self.message[message_index]
            pixel[colour_index] = int(colour[:-1] + bit, 2)
        else:
            return np.array([])     # no more data to embed

        return pixel


    def encode(self):

        # convert message to binary
        self.message = message_to_binary(self.message)
        message_index = 0
        message_length = len(self.message)

        if message_length > self.num_bytes:
            raise ValueError("The message is too large for the image.")

        cover_image = self.image    # so image is not modified

        # loop through image pixels
        for x in range(0, self.width):
            for y in range(0, self.height):

                # assign, retrieve, and convert RGB values
                pixel = cover_image[y][x]
                embedded_pixel = pixel
                r, g, b = message_to_binary(pixel)

                # embed message data in each colour channel
                for colour_index, colour in enumerate([r, g, b]):

                    # embed data within current pixel
                    embedded_pixel = self.embed_pixel(embedded_pixel, colour,\
                        colour_index, message_index, message_length)

                    # reassign embedded pixel to cover image
                    if embedded_pixel.any():
                        cover_image[y][x] = embedded_pixel
                        message_index += 1
                    else:
                        break   # no more data so break

        # reassign and save image
        stego_image = cover_image
        self.save_image(stego_image)


    def decode(self):

        binary_message = ""

        # loop through image pixels
        for x in range(0, self.width):
            for y in range(0, self.height):

                # assign, retrieve, convert, and append LSBs to binary message
                stego_pixel = self.image[y][x]
                r, g, b = message_to_binary(stego_pixel)
                binary_message += r[-1] + g[-1] + b[-1]

        # extract the original message, save to file, and return
        extracted_message = binary_to_string(binary_message, self.delimiter)
        self.save_message(extracted_message)
        return extracted_message


    def save_image(self, stego):

        cv2.imwrite(os.path.join(self.save_path, '{0}_{1}'.\
            format(self.time_string, self.image_name)), stego)


    def save_message(self, message):

        message_file = open(os.path.join(self.save_path, "{0}.txt".format(self.time_string)), "w")
        message_file.write(message)
        message_file.close()
