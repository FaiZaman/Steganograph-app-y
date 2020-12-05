import math
import random
from algorithms.LSBM import LSBM
from algorithms.PVD import PVD
from utility import message_to_binary, integer_to_binary, binary_to_string, save_image, save_message

class LSBMR(LSBM, PVD):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)
        self.pixels = [i for i in range(0, self.num_bytes - 1)]     # [0, 1, 2, ..., num_pixels]


    # satisfies condition such that the LSB of the second message bit is the result of the function
    def binary_function(self, a, b):

        value = math.floor(a/2) + b
        binary_value = integer_to_binary(value)
        return binary_value[-1]


    # generates pixel path through image and sends pixels to be embedded with message data
    def embed_image(self):

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

            # get pixel coordinates based on index
            x = index % self.width
            y = index // self.width

            # compute the two-pixel block and the coordinates of the next pixel
            next_coordinates, block = self.get_pixel_block(x, y)

            # assigning
            first_pixel, second_pixel = block[0], block[1]
            next_x, next_y = next_coordinates[0], next_coordinates[1]

            # check if not 0 or 255 as embedding cannot be performed otherwise
            if 0 < first_pixel < 255 and 0 < second_pixel < 255:

                # get inputs and convert
                first_msg_bit = self.message[message_index]
                second_msg_bit = self.message[message_index + 1]

                first_pixel_binary = integer_to_binary(first_pixel)
                second_pixel_binary = integer_to_binary(second_pixel)

                # LSBMR algorithm
                if first_msg_bit == first_pixel_binary[-1]:

                    if second_msg_bit != self.binary_function(first_pixel, second_pixel):
                        second_stego_pixel = self.embed_pixel(second_pixel_binary, message_index + 1)
                    else:
                        second_stego_pixel = second_pixel

                    first_stego_pixel = first_pixel

                else:

                    if second_msg_bit == self.binary_function(first_pixel - 1, second_pixel):
                        first_stego_pixel = first_pixel - 1
                    else:
                        first_stego_pixel = first_pixel + 1

                    second_stego_pixel = second_pixel

                # reassign new stego pixels and increment message index
                cover_image[y][x] = first_stego_pixel
                cover_image[next_y][next_x] = second_stego_pixel

                message_index += 2

                if message_index == message_length:
                    break

        # reassign, save, and return stego image
        stego_image = cover_image
        save_image(self.save_path, self.image_name, self.time_string, stego_image)

        return stego_image


    # loops through image in the same order as when encoding and extracts message bits
    def extract(self):

        # initialise message and same pseudorandom embedding path
        binary_message = ""
        path = random.sample(self.pixels, self.num_bytes - 1)

        # loop through image pixel blocks
        for index in path:

            # get pixel coordinates based on index
            x = index % self.width
            y = index // self.width

            # compute the two-pixel block and the coordinates of the next pixel
            next_coordinates, stego_block = self.get_pixel_block(x, y)
            first_stego_pixel, second_stego_pixel = stego_block[0], stego_block[1]

            