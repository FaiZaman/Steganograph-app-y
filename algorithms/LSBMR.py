import random
from algorithms.LSBM import LSBM
from algorithms.PVD import PVD
from utility import message_to_binary, integer_to_binary, binary_to_string, save_image, save_message

class LSBMR(LSBM, PVD):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)
        self.pixels = [i for i in range(0, self.num_bytes - 1)]     # [0, 1, 2, ..., num_pixels]


    def binary_function(self, a, b):

        pass


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

        all_data_embedded = False
        for index in path:

            # get pixel coordinates based on index
            x = index % self.width
            y = index // self.width

            # compute the two-pixel block and the coordinates of the next pixel
            next_coordinates, block = self.get_pixel_block(x, y)

            # assigning
            first_pixel = block[0]
            second_pixel = block[1]
            next_x = next_coordinates[0]
            next_y = next_coordinates[1]

            # check if not 0 or 255 as embedding cannot be performed otherwise
            if 0 < block[0] < 255 and 0 < block[1] < 255:
                
                first_msg_bit = self.message[message_index]
                second_msg_bit = self.message[message_index + 1]

                first_pixel_binary = integer_to_binary(first_pixel)
                second_pixel_binary = integer_to_binary(second_pixel)

                if first_msg_bit == first_pixel_binary[-1]:
                    pass

