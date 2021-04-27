import os
import cv2
import string
import random
import numpy as np

from algorithms.LSB import LSB
from algorithms.LSBM import LSBM
from algorithms.LSBMR import LSBMR
from algorithms.PVD import PVD
from algorithms.Hybrid_LSBMR import Hybrid_LSBMR

from edge_detectors.Canny import Canny
from edge_detectors.Sobel import Sobel
from edge_detectors.LoG import LoG

from hybridisation.OR import OR
from hybridisation.AND import AND

embedding_rate = 5

# initialise dataset strings
dataset_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Cover)/"
save_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Stego)/"\
            + str(embedding_rate) + "%/"
extension = ".pgm"

# initialise parameters
global_key = "hi"
random.seed(global_key)
letters = string.ascii_lowercase

# initialising secret message
message_file = "C:/Users/faizz/University Work/Year 4/Advanced Project/Messages/Embedding/"\
                + str(embedding_rate) + "%.txt"
message_file = open(message_file, "r", encoding='utf-8')
message = message_file.read()
message_file.close()

# generates stego images for specified algorithm
def generate_basic(algorithm, algorithm_string, save_path):

    save_path = save_path + algorithm_string + '/'

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension
        key = ''.join(random.choice(letters) for i in range(10))

        # load the cover image file
        cover_path = dataset_path + filename_string
        cover_image = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
        cover_data = (filename_string, cover_image)

        # initialise algorithm and embed data
        alg = algorithm(cover_data, message, key, save_path)
        alg.embed_image()

        print(filename, key)


# generates stego images for edge detector + LSBMR embedding
def generate_standalone(detector, save_path):

    # initialise detector and save path
    edge_detector = detector()
    save_path = save_path + edge_detector.name + '/'

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension
        key = ''.join(random.choice(letters) for i in range(10))

        # load the cover image file
        cover_path = dataset_path + filename_string
        cover_image = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
        cover_data = (filename_string, cover_image)

        # detect edges
        edges = edge_detector.detect(cover_image)

        # initialise algorithm and embed in edges
        Hybrid_LSBMR_algorithm = Hybrid_LSBMR(cover_data, edges, message, key, save_path)
        Hybrid_LSBMR_algorithm.embed_image()

        print(filename)


# generates stego images for hyrbid edge detectors + LSBMR embedding
def generate_hybrid(detector_1, detector_2, hybrid_type, save_path):

    # initialise detectors and combinator
    edge_detector_1 = detector_1()
    edge_detector_2 = detector_2()
    combinator = hybrid_type()

    # initialise save path
    save_path = save_path + edge_detector_1.name + '-' + combinator.name + '-' + edge_detector_2.name + '/'

    # loop through image files
    for filename in range(1, 2756):

        filename_string = str(filename) + extension
        key = ''.join(random.choice(letters) for i in range(10))

        # load the cover image file
        cover_path = dataset_path + filename_string
        cover_image = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
        cover_data = (filename_string, cover_image)

        # detect edges
        edges_1 = edge_detector_1.detect(cover_image)
        edges_2 = edge_detector_2.detect(cover_image)

        # combine the edge areas based on the hybrid type
        hybrid_edges = combinator.merge(edges_1, edges_2)

        # initialise algorithm and embed in edges
        Hybrid_LSBMR_algorithm = Hybrid_LSBMR(cover_data, hybrid_edges, message, key, save_path)
        Hybrid_LSBMR_algorithm.embed_image()

        print(filename, key)


# validates the correct message was extracted
def validate_basic(algorithm, algorithm_string, save_path):

    message = ""
    save_path = save_path + algorithm_string + '/'

    for filename in range(1, 10001):  # 7736

        filename_string = str(filename) + extension
        key = ''.join(random.choice(letters) for i in range(10))

        # load the cover image file
        stego_path = save_path + filename_string
        stego_image = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        stego_data = (filename_string, stego_image)

        # initialise algorithm and extract data
        alg = algorithm(stego_data, message, key, save_path)
        message, saved = alg.extract()

        if not saved:
            os.remove(stego_path)
        else:
            print(filename)


# validates the correct message was extracted
def validate_standalone(detector, save_path):

    # initialise message, detector, and save path
    message = ""
    edge_detector = detector()
    save_path = save_path + edge_detector.name + '/'

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension
        key = ''.join(random.choice(letters) for i in range(10))

        # load the cover image file
        stego_path = save_path + filename_string
        stego_image = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        stego_data = (filename_string, stego_image)

        # detect edges
        edges = edge_detector.detect(stego_image)

        # initialise algorithm and extract from edges
        Hybrid_LSBMR_algorithm = Hybrid_LSBMR(stego_data, edges, message, key, save_path)
        message = Hybrid_LSBMR_algorithm.extract()

        print(message)


# validates the correct message was extracted
def validate_hybrid(detector_1, detector_2, hybrid_type, save_path):

    # initialise detectors and combinator
    edge_detector_1 = detector_1()
    edge_detector_2 = detector_2()
    combinator = hybrid_type()

    # initialise save path and message
    save_path = save_path + edge_detector_1.name + '-' + combinator.name + '-' + edge_detector_2.name + '/'
    message = ""

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension
        key = ''.join(random.choice(letters) for i in range(10))

        # load the cover image file
        stego_path = save_path + filename_string
        stego_image = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        stego_data = (filename_string, stego_image)

        # detect edges and combine the edge areas based on the hybrid type
        edges_1 = edge_detector_1.detect(stego_image)
        edges_2 = edge_detector_2.detect(stego_image)
        hybrid_edges = combinator.merge(edges_1, edges_2)

        # initialise algorithm and embed in edges
        Hybrid_LSBMR_algorithm = Hybrid_LSBMR(stego_data, hybrid_edges, message, key, save_path)
        message = Hybrid_LSBMR_algorithm.extract()

        print(message)


#generate_basic(PVD, 'PVD', save_path)
#validate_basic(LSB, 'LSB', save_path)
#generate_standalone(LoG, save_path)
#validate_standalone(Sobel, save_path)
generate_hybrid(Sobel, LoG, OR, save_path)
#validate_hybrid(Canny, Sobel, AND, save_path)
