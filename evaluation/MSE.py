import cv2

class MSE():

    def __init__(self):

        self.name = 'Mean Squared Error'
        self.error = 0


    # calculates the mean squared error between cover and stego pixel
    def calculate_pixel_error(self, cover_pixel, stego_pixel):

        pixel_error = (abs(stego_pixel - cover_pixel)) ** 2
        return pixel_error


    # calculates the mean squared error between cover and stego images
    def calculate_image_error(self, cover_image, stego_image):

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
                pixel_error = self.calculate_pixel_error(int(cover_pixel), int(stego_pixel))
                self.error += pixel_error

        # normalise the error and return
        normalised_error = self.error / normalisation_factor
        return normalised_error
    

    # gets the MSE
    def get_error(self, cover_image, stego_image):

        self.error = 0
        mean_squared_error = self.calculate_image_error(cover_image, stego_image)
        return mean_squared_error
