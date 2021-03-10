import math
from evaluation.MSE import MSE

class RMSE(MSE):

    def __init__(self):

        super().__init__()
        self.name = "Root Mean Squared Error"


    # calculates the root mean squared error between cover and stego pixel
    def calculate_pixel_error(self, cover_pixel, stego_pixel):

        pixel_error = (abs(stego_pixel - cover_pixel)) ** 2
        root_pixel_error = math.floor(pixel_error)

        return root_pixel_error

RMSE = RMSE()
cover_path = 'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Cover/Lena.png'
stego_path = 'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Stego/2021_03_09_13;55_Lena.png'

cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

error = RMSE.calculate_image_error(cover, stego)
print(error)
