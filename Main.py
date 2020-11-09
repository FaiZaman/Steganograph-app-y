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

    while True:

        data = GUI.display()
        embedding = data[-1]

        if embedding:

            algorithm_name, cover_file, message_file, key, save_path =\ 
                data[0], data[1], data[2], data[3], data[4]
            cover, message = read_files(cover_file, message_file)
            print(message)

            # convert into proper formats and initialise algorithm
            algorithm = algorithm_name(cover, message, key, save_path)
            algorithm.encode()

        else:

            algorithm_name, stego_file, key, save_path = data[0], data[1], data[2], data[3]
            stego = cv2.imread(stego_file)

            algorithm = algorithm_name(stego, message, key, save_path)
            extract = algorithm.decode()
            print(extract)
