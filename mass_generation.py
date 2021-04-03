import cv2
import os
import numpy as np
from algorithms.LSB import LSB
from algorithms.LSBM import LSBM
from algorithms.LSBMR import LSBMR
from algorithms.PVD import PVD
from algorithms.Hybrid_LSBMR import Hybrid_LSBMR

from edge_detectors.Sobel import Sobel
from hybridisation.AND import AND

# initialise dataset strings
dataset_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Cover)/"
save_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Stego)/"
extension = ".pgm"

# initialise parameters
key = "hi"
embedding_rate = 0.1

# initialising secret message
message_file = "C:/Users/faizz/University Work/Year 4/Advanced Project/Messages/Embedding/10%.txt"
message_file = open(message_file, "r", encoding='utf-8')
message = message_file.read()
message_file.close()

# generates stego images for specified algorithm
def generate_basic(algorithm, algorithm_string, save_path):

    save_path = save_path + algorithm_string + '/'

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension

        # load the cover image file
        cover_path = dataset_path + filename_string
        cover_image = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
        cover_data = (filename_string, cover_image)

        # initialise algorithm and embed data
        alg = algorithm(cover_data, message, key, save_path)
        alg.embed_image()

        print(filename)


# generates stego images for edge detector + LSBMR embedding
def generate_standalone(detector, detector_string, save_path):

    save_path = save_path + detector_string + '/'

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension

        # load the cover image file
        cover_path = dataset_path + filename_string
        cover_image = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
        cover_data = (filename_string, cover_image)

        # initialise detector and detect edges
        edge_detector = detector()
        edges = edge_detector.detect(cover_image)
        cv2.imwrite(os.path.join(save_path, 'cover_edges.png'), edges)

        # initialise algorithm and embed in edges
        Hybrid_LSBMR_algorithm = Hybrid_LSBMR(cover_data, edges, message, key, save_path)
        Hybrid_LSBMR_algorithm.embed_image()

        print(filename)


# generates stego images for hyrbid edge detectors + LSBMR embedding
def generate_hybrid(detector_1, detector_2, detector_string_1, detector_string_2, hybrid_type, save_path):

    save_path = save_path + detector_string_1 + '-' + detector_string_2 + '/'

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension

        # load the cover image file
        cover_path = dataset_path + filename_string
        cover_image = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
        cover_data = (filename_string, cover_image)

        # initialise detectors
        edge_detector_1 = detector_1()
        edge_detector_2 = detector_2()

        # detect edges
        edges_1 = edge_detector_1.detect(cover_image)
        edges_2 = edge_detector_2.detect(cover_image)

        # combine the edge areas based on the hybrid type
        combinator = hybrid_type()
        hybrid_edges = combinator.merge(edges_1, edges_2)

        # initialise algorithm and embed in edges
        Hybrid_LSBMR_algorithm = Hybrid_LSBMR(cover_data, hybrid_edges, message, key, save_path)
        Hybrid_LSBMR_algorithm.embed_image()

        print(filename)


# validates the correct message was extracted
def validate_basic(algorithm, algorithm_string, save_path):

    message = ""
    save_path = save_path + algorithm_string + '/'

    for filename in range(1, 10001):

        filename_string = str(filename) + extension

        # load the cover image file
        stego_path = save_path + filename_string
        stego_image = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        stego_data = (filename_string, stego_image)

        # initialise algorithm and extract data
        alg = algorithm(stego_data, message, key, save_path)
        message = alg.extract()

        print(message)


# validates the correct message was extracted
def validate_standalone(detector, detector_string, save_path):

    message = ""
    save_path = save_path + detector_string + '/'

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension

        # load the cover image file
        stego_path = save_path + filename_string
        stego_image = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        stego_data = (filename_string, stego_image)

        # initialise detector and detect edges
        edge_detector = detector()
        edges = edge_detector.detect(stego_image)
        cv2.imwrite(os.path.join(save_path, 'stego_edges.png'), edges)


        # initialise algorithm and extract from edges
        Hybrid_LSBMR_algorithm = Hybrid_LSBMR(stego_data, edges, message, key, save_path)
        message = Hybrid_LSBMR_algorithm.extract()

        print(message)


# validates the correct message was extracted
def validate_hybrid(detector_1, detector_2, detector_string_1, detector_string_2, hybrid_type, save_path):

    message = ""
    save_path = save_path + detector_string_1 + '-' + detector_string_2 + '/'

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension

        # load the cover image file
        stego_path = save_path + filename_string
        stego_image = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        stego_data = (filename_string, stego_image)

        # initialise detectors
        edge_detector_1 = detector_1()
        edge_detector_2 = detector_2()

        # detect edges
        edges_1 = edge_detector_1.detect(stego_image)
        edges_2 = edge_detector_2.detect(stego_image)

        # combine the edge areas based on the hybrid type
        combinator = hybrid_type()
        hybrid_edges = combinator.merge(edges_1, edges_2)

        # initialise algorithm and embed in edges
        Hybrid_LSBMR_algorithm = Hybrid_LSBMR(stego_data, hybrid_edges, message, key, save_path)
        message = Hybrid_LSBMR_algorithm.extract()

        print(message)


generate_standalone(Sobel, 'Sobel', save_path)
#validate_standalone(Sobel, 'Sobel', save_path)
#generate_hybrid(Sobel, Sobel, 'Sobel', 'Sobel', AND, save_path)
#validate_hybrid(Sobel, Sobel, 'Sobel', 'Sobel', AND, save_path)
