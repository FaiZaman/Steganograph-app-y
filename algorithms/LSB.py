import cv2

class LSB():

    def __init__(self, cover, message, key):

        self.cover = cover
        self.message = message
        self.key = key


    def encode(self):

        #binary = string_to_binary(self.message)
        pass


if __name__ == '__main__':

    algorithm = LSB(1, "Hello World!", 2)

    #binary_string = string_to_binary(algorithm.message)
    #string = binary_to_string(binary_string)
