import numpy as np

def message_to_binary(message):

    if type(message) == str:
        return ''.join(format(ord(char), '08b') for char in message)
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(char, "08b") for char in message]
    elif type(message) == int:
        return format(message, "08b")
    else:
        raise TypeError("Unrecognised input.")


def binary_to_string(binary_message):

    message_bytes = [binary_message[i : i + 8] for i in range(0, len(binary_message), 8)]
    string = ""

    for value in message_bytes:

        an_integer = int(value, 2)
        char = chr(an_integer)
        string += char

    return string
