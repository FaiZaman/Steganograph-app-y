import cv2
from GUI import GraphicalUserInterface


def string_to_binary(string):

    return ' '.join(format(ord(char), 'b') for char in string)


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

    GUI = GraphicalUserInterface()
    algorithm_name, cover_file, message_file, key = GUI.display()

    cover, message = read_files(cover_file, message_file)
    algorithm = algorithm_name(cover, message, key)
