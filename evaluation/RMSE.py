import cv2
import math
from MSE import MSE

class RMSE(MSE):

    def __init__(self):

        super().__init__()
        self.name = "Root Mean Squared Error"


    def get_error(self, cover_image, stego_image):

        mean_squared_error = self.calculate_image_error(cover_image, stego_image)
        root_mean_squared_error = math.sqrt(mean_squared_error)
        return root_mean_squared_error


RMSE = RMSE()
cover_path = 'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Cover/Lena.png'
stego_path = 'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Stego/2021_03_09_13;55_Lena.png'

cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

error = RMSE.get_error(cover, stego)
print(error)
