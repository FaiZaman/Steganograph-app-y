import numpy as np

# convert any message to a binary string
def message_to_binary(message):

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message


# convert any integer into 8-bit binary value
def integer_to_binary(integer):

    binary_value = format(integer, "08b")
    return binary_value


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
