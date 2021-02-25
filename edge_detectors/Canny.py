import cv2

class Canny(object):

    def __init__(self, lower_threshold, upper_threshold, ksize):

        self.lower_threshold = 100
        self.upper_threshold = 200


    def detect(self, image):

        edges = cv2.Canny(image, self.lower_threshold, self.upper_threshold)
        return edges
