import cv2

class MSE(object):

    def __init__(self):

        self.name = 'Mean Squared Error'
        self.mean_squared_error = 0


    def calculate_error(self, cover_image, stego_image):

        # initalise dimensions
        height, width = cover_image.shape[0], cover_image.shape[1]
        normalisation_factor = height * width

        # calculate MSE by looping over the images
        for y in range(0, height):
            for x in range(0, width):

                # retrieve pixels
                cover_pixel = cover_image[y][x]
                stego_pixel = stego_image[y][x]

                # calculate error for current pixel
                pixel_error = (abs(int(stego_pixel) - int(cover_pixel))) ** 2
                self.mean_squared_error += pixel_error

        # normalise the error and return
        normalised_error = self.mean_squared_error / normalisation_factor
        return normalised_error

"""
MSE = MSE()
cover_path = 'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Cover/Lena.png'

cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

error = MSE.calculate_error(cover, stego)
print(error)
"""
