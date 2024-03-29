"""
Canny Edge Detection
Implementation taken from OpenCV
Masks the input image on the two LSBs and detects edges based on the masked image
"""

import cv2
import json
from utility import mask_LSB

class Canny(object):

    def __init__(self):

        self.name = "Canny"

        with open('data/detectors.json') as f:
            data = json.load(f)

        self.lower_threshold = self.upper_threshold = 0

        for index in range(0, len(data['detectors'])):
            if data['detectors'][index]['name'] == 'Canny':

                self.lower_threshold =\
                    int(data['detectors'][index]['parameters']['lower_threshold'])
                self.upper_threshold =\
                    int(data['detectors'][index]['parameters']['upper_threshold'])


    # detects edges in the input image
    def detect(self, image):

        # mask the LSBs and run Canny edge detector on masked image
        masked_image = mask_LSB(image)
        edges = cv2.Canny(masked_image, self.lower_threshold, self.upper_threshold)

        return edges
