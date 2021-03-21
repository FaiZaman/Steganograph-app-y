import cv2
from algorithms.LSB import LSB

# initialise dataset strings
dataset_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Cover)/"
save_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Stego)/"
extension = ".pgm"

# initialise parameters
key = "hi"
embedding_rate = 0.1

# initialising secret message
message_file = "C:/Users/faizz/University Work/Year 4/Advanced Project/Messages/Embedding/10%.txt"
message_file = open(message_file, "r", encoding='utf-8')
message = message_file.read()
message_file.close()

# loop through image files

def generate():

    for filename in range(1, 10001):

        filename_string = str(filename) + extension

        # load the cover image file
        cover_path = dataset_path + filename_string
        cover_image = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
        cover_data = (filename_string, cover_image)

        LSB_algorithm = LSB(cover_data, message, key, save_path)
        LSB_algorithm.embed_image()

message = ""

def validate():

    for filename in range(1, 10001):

        filename_string = str(filename) + extension

        # load the cover image file
        stego_path = save_path + filename_string
        stego_image = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        stego_data = (filename_string, stego_image)

        LSB_algorithm = LSB(stego_data, message, key, save_path)
        message = LSB_algorithm.extract()

        print(message)

generate()

"""
RMSE = RMSE()
cover_path = 'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Cover/Lena.png'
stego_path = 
'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Stego/2021_03_09_13;55_Lena.png'

cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

error = RMSE.get_error(cover, stego)
print(error)
"""

"""
PSNR = PSNR()
cover_path = 'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Cover/Lena.png'
stego_path = 
'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Stego/2021_03_09_13;55_Lena.png'

cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

error = PSNR.get_error(cover, stego)
print(error)
"""
