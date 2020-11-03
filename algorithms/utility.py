
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
