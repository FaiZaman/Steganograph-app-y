import cv2
import json

class Canny(object):

    def __init__(self):

        self.name = "Canny Edge Detector"

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

        edges = cv2.Canny(image, self.lower_threshold, self.upper_threshold)
        return edges
