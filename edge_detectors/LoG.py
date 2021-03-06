import cv2
import json
import numpy as np
from utility import integer_to_binary, mask_LSB

class LoG(object):

    def __init__(self):    # x and y necessary as same parameters for all detectors

        self.name = "Laplacian of Gaussian Edge Detector"

        with open('data/detectors.json') as f:
            data = json.load(f)

        self.k_size = 0

        for index in range(0, len(data['detectors'])):
            if data['detectors'][index]['name'] == 'LoG':

                self.k_size = int(data['detectors'][index]['parameters']['kernel_size'])


    # detects edges in the input image
    def detect(self, image):

        # mask the LSBs
        masked_image = mask_LSB(image)

        height, width = image.shape[0], image.shape[1]
        MSB_image = masked_image.copy()

        # blur the image with Gaussian Blur before detecting edges
        blurred_image = cv2.GaussianBlur(MSB_image, (self.k_size, self.k_size), 0)
        edges_unscaled = cv2.Laplacian(blurred_image, ksize=self.k_size, ddepth=cv2.CV_16S)
        edges = cv2.convertScaleAbs(edges_unscaled)

        # reset all non-white points to 0 for most confident edges
        for y in range(0, height):
            for x in range(0, width):

                pixel = edges[y][x]
                if pixel < 128:
                    edges[y][x] = 0
                else:
                    edges[y][x] = 255

        return edges
