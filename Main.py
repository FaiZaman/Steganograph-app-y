import cv2
from GUI import GraphicalUserInterface

delimiter = "-----"

def message_to_binary(message):

    message += delimiter

    if type(message) == str:
        return ' '.join(format(ord(char), 'b') for char in message)
    elif type(message) == bytes:
        return [format(char, "08b") for i in message]
    elif type(message) == int:
        return format(message, "08b")
    else:
        raise TypeError("Unrecognised input.")


def binary_to_string(binary_string):

    binary_values = binary_string.split()
    string = ""

    for value in binary_values:

        an_integer = int(value, 2)
        char = chr(an_integer)
        string += char

    return string


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
    binary_message = message_to_binary(message)
    algorithm = algorithm_name(cover, binary_message, key)

    algorithm.encode()
