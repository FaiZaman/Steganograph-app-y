import cv2
import json

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

        blurred_image = cv2.GaussianBlur(image, (self.ksize, self.ksize), 0)
        edges_unscaled = cv2.Laplacian(blurred_image, ksize=self.ksize, ddepth=cv2.CV_16S)

        edges = cv2.convertScaleAbs(edges_unscaled)
        return edges
