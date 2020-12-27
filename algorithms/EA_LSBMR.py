import cv2
import random
import numpy as np
from algorithms.LSBMR import LSBMR

class EA_LSBMR(LSBMR):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)
        self.Bz = 4
        self.degrees = [0, 90, 180, 270]


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
    def raster_scan(self, image):

        pass


    def embed_image(self):

        rotated_image = self.image

        # loop through image and split into non-overlapping blocks of size Bz x Bz
        for x in range(0, self.width, self.Bz):
            for y in range(0, self.height, self.Bz):

                block = self.image[y : y + self.Bz, x : x + self.Bz]

                # only look at blocks that do not go over the boundary
                if block.shape[0] == block.shape[1]:

                    rotated_block = self.rotate_block(block)
                    rotated_image[y : y + self.Bz, x : x + self.Bz] = rotated_block
        
        self.raster_scan(rotated_image)
        

