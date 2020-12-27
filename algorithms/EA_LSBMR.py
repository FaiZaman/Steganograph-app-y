import cv2
from algorithms.LSBMR import LSBMR

class EA_LSBMR(LSBMR):

    def __init__(self, image, message, key, save_path):

        self.Bz = 4
        super().__init__(image, message, key, save_path)


    def rotate_block(self, block):

        pass


    def embed_image(self):

        # loop through image and split into non-overlapping blocks of size Bz x Bz
        for x in range(0, self.width, self.Bz):
            for y in range(0, self.height, self.Bz):

                block = self.image[y : y + self.Bz, x : x + self.Bz]

                # only look at blocks that do not go over the boundary
                if block.shape[0] == block.shape[1]:
                    self.rotate_block(block)

