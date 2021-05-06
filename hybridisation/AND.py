"""
Logical AND
Merges two edge areas together based on an intersection of their edge pixels
"""

import numpy as np

class AND():

    def __init__(self):

        self.name = "AND"


    # merges the two input edge areas into a single edge area with logical AND
    def merge(self, edge_area_1, edge_area_2):

        # get edge area dimensions and initialise output image
        height, width = edge_area_1.shape[0], edge_area_1.shape[1]
        merged_edges = np.ones((height, width, 1), np.uint8) * 255

        # loop through both edge areas
        for y in range(0, height):
            for x in range(0, width):

                 # get pixels from each area and combine with logical AND
                pixel_1 = edge_area_1[y][x]
                pixel_2 = edge_area_2[y][x]
                AND_pixel = pixel_1 and pixel_2
            
                # set merged edge area pixel value based on the AND pixel
                if AND_pixel == 0:
                    merged_edges[y][x] = 0
                else:
                    merged_edges[y][x] = 255
                
        return merged_edges
