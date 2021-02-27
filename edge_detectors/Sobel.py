import cv2
import json

class Sobel(object):

    def __init__(self, x_order, y_order, ksize):

        self.name = "Sobel Edge Detector"

        with open('data/detectors.json') as f:
            data = json.load(f)

        self.x_order = self.y_order = self.ksize = 0

        for index in range(0, len(data['detectors'])):
            if data['detectors'][index]['name'] == 'Sobel':

                self.x_order = int(data['detectors'][index]['parameters']['x'])
                self.y_order = int(data['detectors'][index]['parameters']['y'])
                self.k_size = int(data['detectors'][index]['parameters']['kernel_size'])


    def detect(self, image):

        edges_unscaled = cv2.Sobel(image, cv2.CV_64F, self.x_order, self.y_order, self.ksize)
        edges = cv2.convertScaleAbs(edges_unscaled)

        return edges
