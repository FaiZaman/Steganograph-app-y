import cv2
import random
import numpy as np
from algorithms.LSBMR import LSBMR

class EA_LSBMR(LSBMR):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)

        # select Bz at random
        self.Bz_list = [1, 4, 8, 12]
        self.Bz = random.choice(self.Bz_list)

        # degrees to rotate by
        self.degrees = [0, 90, 180, 270]
        self.opposite_degrees = [0, 270, 180, 90]

        # storing 7 bits of preset data
        self.preset_region = [(y, 0) for y in range(0, 7)]
        self.new_preset_region = []


    # uses coordinates to get next consecutive coordinate based on raster scanning
    def get_next_pixel(self, x, y):

        if x < self.width - 1:
            x += 1
        else:
            x = 0
            y += 1

        return x, y


    # split image into non-overlapping blocks of size Bz x Bz
    def divide_and_rotate(self, rotated_image, degrees):

        for x in range(0, self.width, self.Bz):
            for y in range(0, self.height, self.Bz):

                block = self.image[y : y + self.Bz][x : x + self.Bz]

                # only look at blocks that do not go over the boundary
                if block.shape[0] == block.shape[1]:
                    
                    rotated_block, degree = self.rotate_block(block, degrees)

                    if (y, x) in self.preset_region:

                        if y < self.Bz:
                            if degree == 90:
                                x = self.Bz - y - 1
                                y = 0
                            elif degree == 180:
                                y = self.Bz - y - 1
                                x = self.Bz - 1
                            elif degree == 270:
                                y = self.Bz - y - 1
                                x = 0   

                        else:

                            if degree == 90:
                                x = 2 * self.Bz - y - 1
                                y = self.Bz
                            elif degree == 180:
                                y = 3 * self.Bz - y - 1
                                x = self.Bz - 1
                            elif degree == 270:
                                x = y - self.Bz
                                y = 2 * self.Bz - 1

                        self.new_preset_region.append((y, x))

                    rotated_image[y : y + self.Bz][x : x + self.Bz] = rotated_block

        return rotated_image


    # rotate by a random degree as determined by secret key
    def rotate_block(self, block, degrees):

        degree = random.choice(degrees)

        if degree == 90:
            rotated_block = cv2.rotate(block, cv2.cv2.ROTATE_90_CLOCKWISE)
        elif degree == 180:
            rotated_block = cv2.rotate(block, cv2.ROTATE_180)
        elif degree == 270:
            rotated_block = cv2.rotate(block, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            rotated_block = block

        return rotated_block, degree


    # rearrange rotated image as row vector by raster scanning
    def convert_to_row_vector(self, image):

        image = image.astype(np.int16)
        V = np.arange(self.num_bytes)    # row vector
        index = 0

        for y in range(0, self.height):
            for x in range(0, self.width):

                # TODO: remove if in new preset region

                if (y, x) not in self.new_preset_region:

                    pixel = image[y][x]
                    V[index] = pixel
                    index += 1

        return V


    # divides into consecutive pairs of embedding units
    def divide_into_embedding_units(self, row_vector, threshold):

        EU = []

        for i in range(0, len(row_vector), 2):

            # get difference value
            unit = row_vector[i : i + 2]
            difference = abs(unit[1] - unit[0])

            # add index to embedding units if greater than threshold t
            if difference >= threshold:
                EU.append(i)

        return EU


    # calculates the threshold T
    def calculate_threshold(self, row_vector, message_length, rotated_image):

        argmax = 0  # initalise T
        rotated_image = rotated_image.astype(np.int16)

        # compute EU(t) for all ts to find argmax
        for t in range(31, -1, -1):

            EU_t = self.divide_into_embedding_units(row_vector, t)
            EU_size = len(EU_t)

            # conditional argmax and replacement with final threshold T
            if 2 * EU_size >= message_length:
                return t
        
        return 0


    # readjustment - TODO or simply skip over these pixels
    def adjust_values(self, first_stego_pixel, second_stego_pixel, T):

        return first_stego_pixel, second_stego_pixel


    # embeds Bz and T in a preset region where data has not been hidden
    def embed_parameters(self, T):

        # convert parameters to binary
        Bz_index = self.Bz_list.index(self.Bz)
        Bz_binary = bin(Bz_index)[2:]
        T_binary = bin(T)[2:]



    def embed_image(self):

        message_index = 0
        message_length = len(self.message)
        
        if message_length > self.num_bytes:
            raise ValueError("The message is too large for the image.")

        # get image after dividing and rotating blocks of size Bz
        cover_image = self.divide_and_rotate(self.image, self.degrees)
        print(self.Bz)
        cv2.imshow('cover', cover_image)

        # convert rotated image to row vector and calculate threshold based on embedding units
        row_vector = self.convert_to_row_vector(cover_image)
        T = self.calculate_threshold(row_vector, message_length, cover_image)

        # calculate new embedding units based on final threshold T and randomise the embedding order
        EU_T = self.divide_into_embedding_units(row_vector, T)
        random.shuffle(EU_T)

        # loop through all embedding units and embed using LSBMR
        for index in EU_T:

            x = index % self.width
            y = index // self.width

            if self.width % 2 == 0 and y % 2 != 0:
                next_x, next_y = self.get_next_pixel(x, y)
            else:
                next_x, next_y = x + 1, y

            # get cover pixels
            first_pixel = cover_image[y][x]
            second_pixel = cover_image[next_y][next_x]

            # get stego pixels using LSBMR embedding
            first_stego_pixel, second_stego_pixel =\
                self.embed_pixels(first_pixel, second_pixel, message_index)

            # check if readjustment is needed if stego pixels out of bounds or threshold    
            if not 0 < first_stego_pixel < 255 or not 0 < second_stego_pixel < 255\
                or abs(first_stego_pixel - second_stego_pixel) < T:

                first_stego_pixel, second_stego_pixel =\
                    self.adjust_values(first_stego_pixel, second_stego_pixel, T)

            # reassign new stego pixels and increment message index
            cover_image[y][x] = first_stego_pixel
            cover_image[next_y][next_x] = second_stego_pixel

            message_index += 2

            if message_index == message_length:
                break

        # reset seed for opposite degrees and redivide and rotate image
        random.seed(self.key)
        self.Bz = random.choice(self.Bz_list)
        stego_image = self.divide_and_rotate(cover_image, self.opposite_degrees)

        # embeds Bz and T
        self.embed_parameters(T)

        cv2.imshow('stego', stego_image)
