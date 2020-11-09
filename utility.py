import numpy as np

# convert any message to a binary string
def message_to_binary(message):

    if type(message) == str:
        return ''.join(format(ord(char), '08b') for char in message)
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(char, "08b") for char in message]
    elif type(message) == int:
        return format(message, "08b")
    else:
        raise TypeError("Unrecognised input.")


# convert a binary string into a UTF-8 string message
def binary_to_string(binary_message, delimiter):

    delimiter_length = len(delimiter) * -1

    # split into bytes
    message_bytes = [binary_message[i : i + 8] for i in range(0, len(binary_message), 8)]
    message = ""

    # convert each byte and append to message
    for byte in message_bytes:

        char = chr(int(byte, 2))
        message += char

        if message[delimiter_length:] == delimiter:   # reached the delimiter
            message = message[:delimiter_length]
            break

    return message
