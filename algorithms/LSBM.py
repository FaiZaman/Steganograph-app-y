from algorithms.LSB import LSB
import numpy as np
import random

class LSBM(LSB):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)


    def embed_pixel(self, pixel, colour, colour_index, message_index, message_length):

        # embed a bit of the data into the Least Significant Bit of the cover image's current pixel
        if message_index < message_length:

            binary_pixel = pixel[colour_index]
            bit = self.message[message_index]

            # randomly add or subtract 1 from pixel value as not equal
            if colour[-1] != bit:

                # generate random number and convert pixel value to integer for easier add/minus
                random_number = random.random()
                integer_pixel = int(colour, 2)

                if random_number < 0.5:     # subtract
                    integer_pixel += 1
                else:
                    integer_pixel -= 1      # add

                # convert back to binary and reassign
                new_binary_pixel = bin(integer_pixel)[2:]
                pixel[colour_index] = new_binary_pixel

            return pixel

        else:
            return np.array([])     # no more data to embed
