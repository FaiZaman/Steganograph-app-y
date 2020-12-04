import random
from algorithms.LSBM import LSBM
from algorithms.PVD import PVD
from utility import message_to_binary, integer_to_binary, binary_to_string, save_image, save_message

class LSBMR(LSBM, PVD):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)
        self.pixels = [i for i in range(0, self.num_bytes - 1)]     # [0, 1, 2, ..., num_pixels]


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
            next_x = next_coordinates[0]
            next_y = next_coordinates[1]
