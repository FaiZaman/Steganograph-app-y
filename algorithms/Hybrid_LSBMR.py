import random
from algorithms.LSBMR import LSBMR
from utility import message_to_binary, save_image

class Hybrid_LSBMR(LSBMR):

    def __init__(self, image, hybrid_edges, message, key, save_path):

        self.hybrid_edges = hybrid_edges
        super().__init__(image, message, key, save_path)


    # retrieves coordinates in image of locations where edges present based on hybrid edges map
    def get_edge_coordinates(self):

        edge_coordinates = []   # initialise edge coordinates list

        # loop through the image
        for y in range(0, self.height):
            for x in range(0, self.width):

                # add coordinate to list if there is edge present
                if self.hybrid_edges[y][x] == 255:
                    edge_coordinates.append((y, x))

        return edge_coordinates


    # generates pixel path through edge coordinates
    def embed_image(self):

        self.message = message_to_binary(self.message)
        message_index = 0
        message_length = len(self.message)

        edge_coordinates = self.get_edge_coordinates()
        num_edge_coordinates = len(edge_coordinates)

        if message_length > num_edge_coordinates:
            raise ValueError("The message is too large for the image.")

        # get a random path based on seed through the edge pixels
        path = random.sample(edge_coordinates, num_edge_coordinates)
        cover_image = self.image  # so image is not modified

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

                message_index += 2

                if message_index == message_length:
                    break

        # reassign, save, and return stego image
        stego_image = cover_image
        save_image(self.save_path, self.image_name, self.time_string, stego_image)

        return stego_image
