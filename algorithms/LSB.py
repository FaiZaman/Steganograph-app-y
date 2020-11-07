import cv2
import numpy as np
from utility import message_to_binary, binary_to_string

class LSB():

    def __init__(self, cover, message, key):

        self.cover = cover
        self.delimiter = "-----"
        self.message = message + self.delimiter
        self.key = key


    def embed_pixel(self, pixel, colour, colour_index, message_index, message_length):

        # embed a bit of the data into the Least Significant Bit of the cover image's current pixel
        if message_index < message_length:
            bit = self.message[message_index]
            pixel[colour_index] = int(colour[:-1] + bit, 2)
        else:
            return np.array([])     # no more data to embed

        return pixel


    def encode(self):

        # get dimensions of cover image
        width = np.size(self.cover, 1)
        height = np.size(self.cover, 0)
        num_bytes = width * height * 3   # 3 colour channels

        self.message = message_to_binary(self.message)
        message_index = 0
        message_length = len(self.message)

        if message_length > num_bytes:
            raise ValueError("The message is too large for the image.")

        cover_image = self.cover    # so cover is not modified

        # loop through image pixels
        for x in range(0, width):
            for y in range(0, height):

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

        # reassign and return stego image
        self.stego = cover_image
        return self.stego
