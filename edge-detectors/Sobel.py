import cv2

class Sobel(object):

    def __init__(self, x_order, y_order, ksize):

        self.x_order = x_order
        self.y_order = y_order
        self.ksize = ksize

    
    def detect(self, image):

        edges = cv2.Sobel(image, cv2.CV64F, self.x_order, self.y_order, self.ksize)
        return edges
