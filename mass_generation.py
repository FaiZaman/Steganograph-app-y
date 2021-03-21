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
for filename in range(1, 10001):

    # load the cover image file
    cover_path = dataset_path + str(filename) + extension
    cover_image = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
    cover_data = (str(filename) + extension, cover_image)

    LSB_algorithm = LSB(cover_data, message, key, save_path)
    LSB_algorithm.embed_image()

"""
MSE = MSE()
cover_path = 'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Cover/Lena.png'
stego_path = 
'C:/Users/faizz/University Work/Year 4/Advanced Project/Images/Stego/2021_03_09_13;55_Lena.png'

cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

error = MSE.get_error(cover, stego)
print(error)
"""

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
