import cv2
import json
import numpy as np
from utility import integer_to_binary

class LoG(object):

    def __init__(self):    # x and y necessary as same parameters for all detectors

        self.name = "Laplacian of Gaussian Edge Detector"

        with open('data/detectors.json') as f:
            data = json.load(f)

        self.k_size = 0

        for index in range(0, len(data['detectors'])):
            if data['detectors'][index]['name'] == 'LoG':

                self.k_size = int(data['detectors'][index]['parameters']['kernel_size'])


    def detect(self, image):

        height, width = image.shape[0], image.shape[1]
        MSB_image = image.copy()

        # loop through image
        for y in range(0, height):
            for x in range(0, width):

                # get pixel and convert to binary
                pixel = image[y][x]
                binary_pixel = integer_to_binary(pixel)

                # set 7 LSBs to 0 and preserve MSB in image
                LSBs = '0000000'
                new_binary_pixel = binary_pixel[0] + LSBs
                MSB_image[y][x] = int(new_binary_pixel, 2)

        # blur the image with Gaussian Blur before detecting edges
        blurred_image = cv2.GaussianBlur(MSB_image, (self.k_size, self.k_size), 0)
        edges_unscaled = cv2.Laplacian(blurred_image, ksize=self.k_size, ddepth=cv2.CV_16S)

        edges = cv2.convertScaleAbs(edges_unscaled)

        # reset all non-white points to 0 for most confident edges
        for y in range(0, height):
            for x in range(0, width):

                pixel = edges[y][x]
                if pixel < 255:
                    edges[y][x] = 0

        return edges
