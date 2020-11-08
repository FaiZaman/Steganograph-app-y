import cv2
from GUI import GraphicalUserInterface

def read_files(cover_file, message_file):

    cover = cv2.imread(cover_file)

    message_file = open(message_file, "r")
    message = message_file.read()
    message_file.close()

    return cover, message


if __name__ == '__main__':

    # run GUI and retrieve img and txt files
    GUI = GraphicalUserInterface()
    algorithm_name, cover_file, message_file, key = GUI.display()

    # convert into proper formats and initialise algorithm
    cover, message = read_files(cover_file, message_file)
    algorithm = algorithm_name(cover, message, key)

    stego = algorithm.encode()
    extract = algorithm.decode()

    print(extract)