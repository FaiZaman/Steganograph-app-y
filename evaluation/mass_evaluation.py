import cv2
from MSE import MSE

# initialise paths and error metrics
cover_dataset_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Cover)/"
stego_dataset_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Stego)/"
extension = ".pgm"

MSE = MSE()


# loop through image files
for filename in range(1, 10001):

    filename_string = str(filename) + extension

    # load the cover image file
    cover_path = cover_dataset_path + filename_string
    cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)

    stego_path = stego_dataset_path + filename_string
    stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

    error = MSE.get_error(cover, stego)
    print(error)
