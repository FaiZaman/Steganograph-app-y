import cv2

class LoG(object):

    def __init__(self, x, y, ksize):    # x and y necessary as same parameters for all detectors

        self.name = "Laplacian of Gaussian Edge Detector"
        self.ksize = ksize
    

    def detect(self, image):

        blurred_image = cv2.GaussianBlur(image, (self.ksize, self.ksize), 0)
        edges_unscaled = cv2.Laplacian(blurred_image, ksize=self.ksize, ddepth=cv2.CV_16S)

        edges = cv2.convertScaleAbs(edges_unscaled)
        return edges
