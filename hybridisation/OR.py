"""
Logical OR
Merges two edge areas together based on a union of their edge pixels
"""

import numpy as np

class OR():

    def __init__(self):

        self.name = "OR"


    # merges the two input edge areas into a single edge area with logical OR
    def merge(self, edge_area_1, edge_area_2):

        # get edge area dimensions and initialise output image
        height, width = edge_area_1.shape[0], edge_area_1.shape[1]
        merged_edges = np.ones((height, width, 1), np.uint8) * 255

        # loop through both edge areas
        for y in range(0, height):
            for x in range(0, width):

                # get pixels from each area and combine with logical OR
                pixel_1 = edge_area_1[y][x]
                pixel_2 = edge_area_2[y][x]
                OR_pixel = pixel_1 or pixel_2

                # set merged edge area pixel value based on the OR pixel
                if OR_pixel == 0:
                    merged_edges[y][x] = 0
                else:
                    merged_edges[y][x] = 255
        
        return merged_edges
