import random
from algorithms.LSBMR import LSBMR
from utility import integer_to_binary, message_to_binary, is_message_complete,\
                    binary_to_string, save_image, save_message

class Hybrid_LSBMR(LSBMR):

    def __init__(self, image, hybrid_edges, message, key, save_path):

        self.hybrid_edges = hybrid_edges
        super().__init__(image, message, key, save_path)


    # retrieves coordinates in image of locations where edges present based on hybrid edges map
    def get_coordinates(self):

        # initialise coordinate lists
        edge_coordinates = []
        non_edge_coordinates = []

        # loop through the image
        for y in range(0, self.height):
            for x in range(0, self.width):

                # either both odd or both even for first pixel in block
                if (y % 2 == 0 and x % 2 == 0) or (y % 2 != 0 and x % 2 != 0):

                    # add coordinate to list if there is edge present
                    if self.hybrid_edges[y][x] == 255:
                        edge_coordinates.append((y, x))
                    else:
                        non_edge_coordinates.append((y, x))

        return edge_coordinates, non_edge_coordinates


    # traverses edge or non-edge path and embeds data using LSBMR
    def embed_path(self, path, message_length, message_index, cover_image, embedded):

        for (y, x) in path:

            # compute the two-pixel block and the coordinates of the next pixel
            next_coordinates, block = self.get_pixel_block(x, y)

            # assigning
            first_pixel, second_pixel = block[0], block[1]
            next_x, next_y = next_coordinates[0], next_coordinates[1]

            # check if not 0 or 255 as embedding cannot be performed otherwise
            if 0 < first_pixel < 255 and 0 < second_pixel < 255:

                # use LSBMR embedding and output stego pixels
                first_stego_pixel, second_stego_pixel =\
                    self.embed_pixels(first_pixel, second_pixel, message_index)

                # reassign new stego pixels and increment message index
                cover_image[y][x] = first_stego_pixel
                cover_image[next_y][next_x] = second_stego_pixel

                # add current pair of coordinates to the embedded coordinates list and increment index
                message_index += 2

                # if the whole message was embedded we can check this later
                if message_index == message_length:
                    embedded = True
                    break

        return cover_image, message_index, embedded


    # generates pixel path through edge coordinates
    def embed_image(self):

        self.message = message_to_binary(self.message)
        message_length = len(self.message)
        message_index = 0

        # get the edge coordinates from the hybrid edge areas and initialise embedded coordinates list
        edge_coordinates, non_edge_coordinates = self.get_coordinates()
        num_edge_coordinates = len(edge_coordinates)
        num_non_edge_coordinates = len(non_edge_coordinates)

        if message_length > self.num_bytes:
            raise ValueError("The message is too large for the image.")

        # get a random path based on seed through the edge pixels
        edge_path = random.sample(edge_coordinates, num_edge_coordinates)
        cover_image = self.image  # so image is not modified

        # embeds based on the edge path
        embedded = False
        cover_image, message_index, embedded =\
            self.embed_path(edge_path, message_length, message_index, cover_image, embedded)

        # embed based on non-edge pixels if the message was too big for edge pixels alone
        if not embedded:
            random.seed(self.key)
            non_edge_path = random.sample(non_edge_coordinates, num_non_edge_coordinates)
            cover_image, message_index, embedded =\
                self.embed_path(non_edge_path, message_length, message_index, cover_image, embedded)

        # reassign, save, and return stego image
        stego_image = cover_image
        save_image(self.save_path, self.image_name, self.time_string, stego_image)

        return stego_image


    # traverses edge or non-edge path and extracts data using LSBMR
    def extract_path(self, path, binary_message):

        counter = 0

        for (y, x) in path:

            # compute the two-pixel block and the coordinates of the next pixel
            next_coordinates, stego_block = self.get_pixel_block(x, y)
            first_stego_pixel, second_stego_pixel = stego_block[0], stego_block[1]
            next_x, next_y = next_coordinates[0], next_coordinates[1]

            # extract both bits from the pixel pair
            first_binary_pixel = integer_to_binary(first_stego_pixel)
            first_msg_bit = first_binary_pixel[-1]
            second_msg_bit = self.binary_function(first_stego_pixel, second_stego_pixel)

            # append to message and add current pair of coordinates to the embedded coordinates list
            binary_message += first_msg_bit + second_msg_bit

            # check every 5000 iterations if the message is in the extracted bits so far
            # in order to speed up the algorithm
            if counter % 5000 == 0:
                if is_message_complete(binary_message, self.delimiter):
                    break
                extracted_message, _ = binary_to_string(binary_message, self.delimiter)
            counter += 1

        return binary_message


    # loops through edge pixels in same order as when encoding and extracts message bits
    def extract(self):

        # initialise message and embedded coordinates list
        binary_message = ""

        # get the coordinates from the hybrid edge areas and pseudorandom embedding path
        edge_coordinates, non_edge_coordinates = self.get_coordinates()
        num_edge_coordinates = len(edge_coordinates)
        num_non_edge_coordinates = len(non_edge_coordinates)

        # extracts based on the edge path
        edge_path = random.sample(edge_coordinates, num_edge_coordinates)
        binary_message = self.extract_path(edge_path, binary_message)

        # attempt to extract original message
        extracted_message, delimiter_present = binary_to_string(binary_message, self.delimiter)

        # extract based on non-edge pixels if the message was too big for edge pixels alone
        if not delimiter_present:

            # re-seed and sample path of non edge pixels
            random.seed(self.key)
            non_edge_path = random.sample(non_edge_coordinates, num_non_edge_coordinates)

            # extract the message and convert back from binary
            binary_message = self.extract_path(non_edge_path, binary_message)
            extracted_message, delimiter_present = binary_to_string(binary_message, self.delimiter)

        # save to file, and return
        save_message(self.save_path, self.time_string, extracted_message)
        return extracted_message
