from algorithms.LSB import LSB

class LSBM(LSB):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)
        print(self.message)

