import cv2
import math
from MSE import MSE

class PSNR(MSE):

    def __init__(self):

        super().__init__()
        self.name = "Peak Signal to Noise Ratio"


    def get_error(self, cover_image, stego_image, mean_squared_error):

        if mean_squared_error == 0:
            mean_squared_error = self.calculate_image_error(cover_image, stego_image)

        fractal = (255 * 255) / mean_squared_error
        peak_signal_to_noise_ratio = 10 * math.log10(fractal)

        return peak_signal_to_noise_ratio
