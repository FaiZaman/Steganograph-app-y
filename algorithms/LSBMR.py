import math
import random
from algorithms.LSBM import LSBM
from algorithms.PVD import PVD
from utility import message_to_binary, integer_to_binary, binary_to_string,\
                    save_image, save_message

class LSBMR(LSBM, PVD):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)

        # initialise pixels = [0, 1, 2, ..., num_pixels] and outliers for masking
        self.pixels = [i for i in range(0, self.num_bytes - 1)]
        self.outliers = {}

        # generate the cases where masking the 2 LSBs does not give the same result
        # for two adjacent values, and value is value to add to fix this
        for j in range(1, 254):

            if 252 & j != 252 & (j + 1):
                self.outliers[j] = -1

            elif 252 & j != 252 & (j - 1):
                self.outliers[j] = 1


    # satisfies condition such that the LSB of the second message bit is result of the function
    def binary_function(self, a, b):

        value = math.floor(a/2) + b
        binary_value = integer_to_binary(value)
        return binary_value[-1]


    # computes the first stego pixel from LSBMR embedding
    def first_pixel_change(self, first_pixel, first_stego_pixel, value):

        # if pixel is outlier do the operation as defined in outliers dict
        if first_pixel in self.outliers:
            first_stego_pixel += self.outliers[first_pixel]
        else:
            first_stego_pixel = first_pixel + value

        return first_stego_pixel


    # embeds message bits in pair of pixels as per LSBMR embedding
    def embed_pixels(self, first_pixel, second_pixel, message_index):

        # get inputs and convert
        first_msg_bit = self.message[message_index]
        second_msg_bit = self.message[message_index + 1]

        first_pixel_binary = integer_to_binary(first_pixel)
        first_stego_pixel, second_stego_pixel = first_pixel, second_pixel

        # LSBMR algorithm
        if first_msg_bit == first_pixel_binary[-1]:

            if second_msg_bit != self.binary_function(first_pixel, second_pixel):

                # if pixel is outlier do the operation as defined in outliers dict
                if second_pixel in self.outliers:
                    second_stego_pixel += self.outliers[second_pixel]
                else:
                    second_stego_pixel = self.random_increment_or_decrement(second_pixel)

            else:

                second_stego_pixel = second_pixel

            first_stego_pixel = first_pixel

        else:

            if second_msg_bit == self.binary_function(first_pixel - 1, second_pixel):
                first_stego_pixel = self.first_pixel_change(first_pixel, first_stego_pixel, -1)
            else:
                first_stego_pixel = self.first_pixel_change(first_pixel, first_stego_pixel, 1)

            second_stego_pixel = second_pixel

        # LSBMR adjustment for masking edges - if the adjustment offsets binary function
        # add or subtract 3 from first stego pixel to conserve this; keeping 6 MSBs same for masking
        if second_msg_bit != self.binary_function(first_stego_pixel, second_stego_pixel):
            if first_stego_pixel > first_pixel:
                first_stego_pixel = first_pixel + 3
            else:
                first_stego_pixel = first_pixel - 3

        return first_stego_pixel, second_stego_pixel


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
        embedded_coordinates = []

        for index in path:

            # get pixel coordinates based on index
            x = index % self.width
            y = index // self.width

            # compute the two-pixel block and the coordinates of the next pixel
            next_coordinates, block = self.get_pixel_block(x, y)
            first_pixel, second_pixel = block[0], block[1]
            next_x, next_y = next_coordinates[0], next_coordinates[1]

            # check if not 0 or 255 as embedding cannot be performed otherwise
            if 0 < first_pixel < 255 and 0 < second_pixel < 255:

                if (y, x) not in embedded_coordinates and (next_y, next_x) not in embedded_coordinates\
                    and not(y == self.height - 1 and x == 0)\
                    and not(y == self.height - 1 and x == self.width - 1):

                    # use LSBMR embedding and output stego pixels
                    first_stego_pixel, second_stego_pixel =\
                        self.embed_pixels(first_pixel, second_pixel, message_index)

                    if first_stego_pixel == 128 and second_stego_pixel == 144:
                        print(y, x, next_y, next_x)

                    # reassign new stego pixels and increment message index
                    cover_image[y][x] = first_stego_pixel
                    cover_image[next_y][next_x] = second_stego_pixel

                    embedded_coordinates.append((y, x))
                    embedded_coordinates.append((next_y, next_x))
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
        embedded_coordinates = []
        path = random.sample(self.pixels, self.num_bytes - 1)
        counter = 0

        # loop through image pixel blocks
        for index in path:

            # get pixel coordinates based on index
            x = index % self.width
            y = index // self.width

            counter += 1
            if counter % 1000 == 0:
                print(counter)

            # compute the two-pixel block and the coordinates of the next pixel
            next_coordinates, stego_block = self.get_pixel_block(x, y)
            first_stego_pixel, second_stego_pixel = stego_block[0], stego_block[1]
            next_x, next_y = next_coordinates[0], next_coordinates[1]

            if (y, x) not in embedded_coordinates and (next_y, next_x) not in embedded_coordinates\
                and not(y == self.height - 1 and x == 0)\
                and not(y == self.height - 1 and x == self.width - 1):

                # extract both bits from the pixel pair
                first_binary_pixel = integer_to_binary(first_stego_pixel)
                first_msg_bit = first_binary_pixel[-1]
                second_msg_bit = self.binary_function(first_stego_pixel, second_stego_pixel)

                binary_message += first_msg_bit + second_msg_bit

                embedded_coordinates.append((y, x))
                embedded_coordinates.append((next_y, next_x))

        # extract the original message, save to file, and return
        extracted_message = binary_to_string(binary_message, self.delimiter)
        save_message(self.save_path, self.time_string, extracted_message)

        return extracted_message
