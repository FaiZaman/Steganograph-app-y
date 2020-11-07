import cv2
import numpy as np

class LSB():

    def __init__(self, cover, message, key):

        self.cover = cover
        self.message = message
        self.key = key


    def encode(self):

        width = np.size(self.cover, 1)
        height = np.size(self.cover, 0)

        num_bytes = width * height * 3   # 3 colour channels
        message_length = len(self.message)

        




#if __name__ == '__main__':
#
#    algorithm = LSB(1, "Hello World!", 2)
