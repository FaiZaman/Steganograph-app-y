import cv2
import numpy as np
from utility import message_to_binary, binary_to_string

class LSB():

    def __init__(self, cover, message, key):

        self.cover = cover
        self.delimiter = "-----"
        self.message = message + self.delimiter
        self.key = key


    def embed_pixel(self, pixel, colour, message_index, message_length, bit):

        if message_index < message_length:
            pixel[0] = int(colour[:-1] + message_bit, 2)    # make agnostic
        else:
            return None

        return pixel


    def encode(self):

        width = np.size(self.cover, 1)
        height = np.size(self.cover, 0)
        num_bytes = width * height * 3   # 3 colour channels

        self.message = message_to_binary(self.message)
        message_index = 0
        message_length = len(self.message)

        if message_length > num_bytes:
            raise ValueError("The message is too large for the image.")

        # loop through image pixels
        for x in range(0, width):
            for y in range(0, height):

                pixel = self.cover[y][x]
                embedded_pixel = pixel

                r, g, b = message_to_binary(pixel)
                message_bit = self.message[message_index]

                for colour in [r, g, b]:
                    embedded_pixel = self.embed_pixel\
                        (embedded_pixel, colour, message_index, message_length, message_bit)
                    #if embedded_pixel:
                     #   self.cover[y][x] = 
                    message_index += 1

                break
            break
