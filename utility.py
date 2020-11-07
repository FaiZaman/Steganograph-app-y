import numpy as np

def message_to_binary(message):

    if type(message) == str:
        return ' '.join(format(ord(char), 'b') for char in message)
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(char, "08b") for char in message]
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