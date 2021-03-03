from algorithms.LSBMR import LSBMR

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

        edge_coordinates = self.get_edge_coordinates()
