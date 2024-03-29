"""
Main file for Steganograph-app-y
Run to display the GUI and embed and extract
"""

import cv2
import ntpath

from algorithms.LSBMR import LSBMR
from algorithms.Hybrid_LSBMR import Hybrid_LSBMR

from GUI import GraphicalUserInterface


def read_image(image_file):

    image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    image_name = ntpath.basename(image_file)
    image_data = (image_name, image)

    return image_data


def read_files(image_file, message_file):

    image_data = read_image(image_file)

    message_file = open(message_file, "r", encoding='utf-8')
    message = message_file.read()
    message_file.close()

    return image_data, message


if __name__ == '__main__':

    # run GUI and retrieve img and txt files
    GUI = GraphicalUserInterface()
    running = True

    while running:

        data = GUI.display()
        operation = data[-1]

        if operation == "embedding":

            # retrieve embedding data from GUI embedding screen
            algorithm_name, cover_file, message_file, key, save_path =\
                data[0], data[1], data[2], data[3], data[4]

            # convert into proper formats and initialise algorithm to encode message
            cover_data, message = read_files(cover_file, message_file)
            algorithm = algorithm_name(cover_data, message, key, save_path)

            # embed the message and display result of embedding
            saved = algorithm.embed_image()
            running = GUI.status(saved, operation, save_path)

        elif operation == "hybrid_embedding":

            # retrieve hybrid embedding data from GUI
            detector_1_name, detector_2_name, hybrid_type, cover_file, message_file, key, save_path =\
                data[0], data[1], data[2], data[3], data[4], data[5], data[6]

            # convert into proper formats and initalise detectors to detect edges
            cover_data, message = read_files(cover_file, message_file)
            detector_1 = detector_1_name()
            detector_2 = detector_2_name()

            # get the edge areas from each detector
            edges_1 = detector_1.detect(cover_data[1])
            edges_2 = detector_2.detect(cover_data[1])

            # combine the edge areas based on the hybrid type
            combinator = hybrid_type()
            hybrid_edges = combinator.merge(edges_1, edges_2)

            # initialise LSBMR algorithm, embed within hybrid edge areas, and display status
            Hybrid_LSBMR_algorithm = Hybrid_LSBMR(cover_data, hybrid_edges, message, key, save_path)
            saved = Hybrid_LSBMR_algorithm.embed_image()
            running = GUI.status(saved, operation, save_path)

        elif operation == "extracting":

            # retrieve extracting data from GUI extracting screen and convert into proper formats
            algorithm_name, stego_file, key, save_path = data[0], data[1], data[2], data[3]
            stego_data = read_image(stego_file)
            message = ""

            # initalise algorithm, decode message, and display status
            algorithm = algorithm_name(stego_data, message, key, save_path)
            saved = algorithm.extract()
            running = GUI.status(saved, operation, save_path)

        else:

            # retrieve hybrid embedding data from GUI
            detector_1_name, detector_2_name, hybrid_type, stego_file, key, save_path =\
                data[0], data[1], data[2], data[3], data[4], data[5]

            # convert into proper formats and initalise message
            stego_data = read_image(stego_file)
            message = ""

            # initialise detectors to detect edges
            detector_1 = detector_1_name()
            detector_2 = detector_2_name()

            # get the edge areas from each detector
            edges_1 = detector_1.detect(stego_data[1])
            edges_2 = detector_2.detect(stego_data[1])

            # combine the edge areas based on the hybrid type
            combinator = hybrid_type()
            hybrid_edges = combinator.merge(edges_1, edges_2)

            # initialise hybrid LSBMR algorithm, decode message, and display status
            Hybrid_LSBMR_algorithm = Hybrid_LSBMR(stego_data, hybrid_edges, message, key, save_path)
            saved = Hybrid_LSBMR_algorithm.extract()
            running = GUI.status(saved, operation, save_path)
