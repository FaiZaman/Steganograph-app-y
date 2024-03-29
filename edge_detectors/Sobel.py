"""
Sobel Edge Detection
Implementation taken from OpenCV
Masks the input image on the two LSBs and detects edges based on the masked image for both Sobel filters
The edge areas are then combined and returned
"""

import cv2
import json
from utility import mask_LSB

class Sobel(object):

    def __init__(self):

        self.name = "Sobel"

        with open('data/detectors.json') as f:
            data = json.load(f)

        self.ksize = 0

        for index in range(0, len(data['detectors'])):
            if data['detectors'][index]['name'] == 'Sobel':

                self.k_size = int(data['detectors'][index]['parameters']['kernel_size'])
                self.threshold = int(data['detectors'][index]['parameters']['gradient_threshold'])


    # detects edges in the input image
    def detect(self, image):

        # mask the LSBs
        masked_image = mask_LSB(image)

        # calculate gradients in both x and y directions and get image dimensions
        x_gradients = cv2.Sobel(masked_image, cv2.CV_64F, 0, 1, self.ksize)
        y_gradients = cv2.Sobel(masked_image, cv2.CV_64F, 1, 0, self.ksize)

        # get image dimensions and initialise new gradients image
        height, width = masked_image.shape[0], masked_image.shape[1]
        edges = x_gradients.copy()

        # loop thorough x and y gradients and combine them
        for y in range(0, height):
            for x in range(0, width):

                # take the sum
                edges[y][x] = x_gradients[y][x] + y_gradients[y][x]

                # set binary values depending on threshold = 400
                if edges[y][x] > self.threshold:
                    edges[y][x] = 255
                else:
                    edges[y][x] = 0

        return edges
