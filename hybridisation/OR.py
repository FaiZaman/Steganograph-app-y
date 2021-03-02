
class OR(object):

    def __init__(self):

        self.name = "OR"


    def merge(self, edge_area_1, edge_area_2):

        height, width = edge_area_1.shape[0], edge_area_1.shape[1]

        for y in range(0, height):
            for x in range(0, width):

                pixel_1 = edge_area_1[y][x]
                pixel_2 = edge_area_2[y][x]
