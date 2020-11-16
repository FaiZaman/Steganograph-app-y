from algorithms.LSB import LSB
import random

class LSBM(LSB):

    def __init__(self, image, message, key, save_path):

        super().__init__(image, message, key, save_path)


    def embed_pixel(self, pixel, colour, colour_index, message_index, message_length):

        if message_index < message_length:
        
            binary_pixel = pixel[colour_index]
            bit = self.message[message_index]

            if binary_pixel[-1] != bit:

                random_number = random.random()
                integer_pixel = int(binary_pixel, 2)

                if random_number < 0.5:     # subtract
                    integer_pixel += 1
                else:
                    integer_pixel -= 1
                
                new_binary_pixel = bin(integer_pixel[2:])
                
