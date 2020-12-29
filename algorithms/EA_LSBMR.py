import cv2
import random
import numpy as np
from algorithms.LSBMR import LSBMR

class EA_LSBMR(LSBMR):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)
        self.Bz = 4
        self.degrees = [0, 90, 180, 270]


    def get_next_pixel(self, x, y):

        if x < self.width - 1:
            x += 1
        else:
            x = 0
            y += 1

        return x, y                


    # rotate by a random degree as determined by secret key
    def rotate_block(self, block):

        degree = random.choice(self.degrees)

        if degree == 90:
            rotated_block = cv2.rotate(block, cv2.cv2.ROTATE_90_CLOCKWISE)
        elif degree == 180:
            rotated_block = cv2.rotate(block, cv2.ROTATE_180)
        elif degree == 270:
            rotated_block = cv2.rotate(block, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            rotated_block = block

        return rotated_block


    # rearrange rotated image as row vector by raster scanning
    def convert_to_row_vector(self, image):

        image = image.astype(np.int16)
        V = np.arange(self.num_bytes)    # row vector
        index = 0

        for y in range(0, self.height):
            for x in range(0, self.width):

                pixel = image[y][x]
                V[index] = pixel
                index += 1

        return V


    # divides into consecutive pairs of embedding units
    def divide_into_embedding_units(self, row_vector, threshold):

        EU = set()

        for i in range(0, len(row_vector), 2):

            # get difference value
            unit = row_vector[i : i + 2]
            difference = abs(unit[1] - unit[0])

            # add index to embedding units if greater than threshold t
            if difference >= threshold:
                EU.add(i)

        return EU

    """
    def values(self):

        # get values at each index
        for index in EU_t:

            x = index % self.width
            y = index // self.width

            if self.width % 2 == 0 and y % 2 != 0:
                next_x, next_y = self.get_next_pixel(x, y)
            else:
                next_x, next_y = x + 1, y

            pixel1 = rotated_image[y][x]
            pixel2 = rotated_image[next_y][next_x]

        return pixel1, pixel2
    """

    # calculates the threshold T
    def calculate_threshold(self, row_vector, message_length, rotated_image):

        argmax = 0  # initalise T
        rotated_image = rotated_image.astype(np.int16)

        # compute EU(t) for all ts to find argmax
        for t in range(31, -1, -1):

            EU_t = self.divide_into_embedding_units(row_vector, t)
            EU_size = len(EU_t)

            print(EU_size, message_length)

            # conditional argmax and replacement
            if 2 * EU_size >= message_length:
                return t

        return 0


    def embed_image(self):

        rotated_image = self.image
        message_length = len(self.message)

        # loop through image and split into non-overlapping blocks of size Bz x Bz
        for x in range(0, self.width, self.Bz):
            for y in range(0, self.height, self.Bz):

                block = self.image[y : y + self.Bz, x : x + self.Bz]

                # only look at blocks that do not go over the boundary
                if block.shape[0] == block.shape[1]:

                    rotated_block = self.rotate_block(block)
                    rotated_image[y : y + self.Bz, x : x + self.Bz] = rotated_block

        # convert rotated image to row vector and calculate threshold based on embedding units
        row_vector = self.convert_to_row_vector(rotated_image)
        T = self.calculate_threshold(row_vector, message_length, rotated_image)
