import cv2

class Sobel(object):

    def __init__(self, x_order, y_order, ksize):

        self.name = "Sobel Edge Detector"
        self.x_order = x_order
        self.y_order = y_order
        self.ksize = ksize


    def detect(self, image):

        edges_unscaled = cv2.Sobel(image, cv2.CV_64F, self.x_order, self.y_order, self.ksize)
        edges = cv2.convertScaleAbs(edges_unscaled)

        return edges
