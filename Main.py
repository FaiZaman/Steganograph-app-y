import cv2
import ntpath
from GUI import GraphicalUserInterface

def read_image(image_file):

    image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    image_name = ntpath.basename(image_file)
    image_data = (image_name, image)

    return image_data


def read_files(image_file, message_file):

    image_data = read_image(image_file)

    message_file = open(message_file, "r")
    message = message_file.read()
    message_file.close()

    return image_data, message


if __name__ == '__main__':

    # run GUI and retrieve img and txt files
    GUI = GraphicalUserInterface()

    while True:

        data = GUI.display()
        operation = data[-1]

        if operation == "embedding":

            # retrieve embedding data from GUI embedding screen
            algorithm_name, cover_file, message_file, key, save_path =\
                data[0], data[1], data[2], data[3], data[4]

            # convert into proper formats and initialise algorithm to encode message
            cover_data, message = read_files(cover_file, message_file)
            algorithm = algorithm_name(cover_data, message, key, save_path)
            algorithm.embed_image()

        elif operation == "hybrid_embedding":

            # retrieve hybrid_embedding data from GUI
            detector_1_name, detector_2_name, hybrid_type, cover_file, message_file, key, \
                save_path = data[0], data[1], data[2], data[3], data[4], data[5], data[6]

            # convert into proper formats and initalise detectors to detect edges
            cover_data, message = read_files(cover_file, message_file)
            detector_1 = detector_1_name()
            detector_2 = detector_2_name()

            # get the edge areas from each detector
            edges_1 = detector_1.detect(cover_data[1])
            edges_2 = detector_2.detect(cover_data[1])

            cv2.imshow(detector_1.name, edges_1)
            cv2.imshow(detector_2.name, edges_2)

            #for y in range(0, edges_2.shape[0]):
            #    for x in range(0, edges_2.shape[1]):
            #        
            #        if edges_2[y][x] > 128:
            #            print(edges_2[y][x])

        else:

            # retrieve extracting data from GUI embedding screen and convert into proper formats
            algorithm_name, stego_file, key, save_path = data[0], data[1], data[2], data[3]
            stego_data = read_image(stego_file)
            message = ""

            # initalise algorithm and decode message
            algorithm = algorithm_name(stego_data, message, key, save_path)
            extracted_message = algorithm.extract()
