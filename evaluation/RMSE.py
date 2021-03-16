import cv2
import math
from MSE import MSE

class RMSE(MSE):

    def __init__(self):

        super().__init__()
        self.name = "Root Mean Squared Error"


    # calculates MSE and takes square root
    def get_error(self, cover_image, stego_image):

        mean_squared_error = self.calculate_image_error(cover_image, stego_image)
        root_mean_squared_error = math.sqrt(mean_squared_error)
        return root_mean_squared_error
