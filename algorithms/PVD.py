import cv2

class PVD():

    def __init__(self, image, message, key, save_path):

        self.image = image
        self.message = message
        self.key = key
        self.save_path = save_path

        # get dimensions of image
        self.width = np.size(self.image, 1)
        self.height = np.size(self.image, 0)
        self.num_bytes = self.width * self.height * 3   # 3 colour channels


    def split_image(self):

        stego = self.image

        for y in range(0, self.height):
            for x in range(0, self.width):

                current_pixel = self.image[y][x]
                prev_pixel = self.image[y][x - 1]
                