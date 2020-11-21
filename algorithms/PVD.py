import cv2
import numpy as np

class PVD():

    def __init__(self, image, message, key, save_path):

        self.image_name = image[0]
        self.image = image[1]
        self.message = message
        self.key = key
        self.save_path = save_path

        # get dimensions of image
        self.width = np.size(self.image, 1)
        self.height = np.size(self.image, 0)
        self.num_bytes = self.width * self.height * 3   # 3 colour channels


    def encode(self):

        stego = self.image
        x = y = 0

        while True:

            current_pixel = self.image[y][x]

            if y % 2 == 0:  # going right

                if x < self.width - 1:
                    x += 1
                    next_pixel = self.image[y][x]

                else:

                    if y == self.height - 1:
                        break

                    y += 1
                    next_pixel = self.image[y][x]


            else:   # going left

                if x > 0:
                    x -= 1
                    next_pixel = self.image[y][x]

                else:
                    y += 1
                    next_pixel = self.image[y][x]
