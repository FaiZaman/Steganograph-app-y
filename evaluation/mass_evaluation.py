import cv2
from pathlib import Path
from MSE import MSE
from PSNR import PSNR

embedding_rate = 50

# initialise paths - replace with your own
cover_dataset_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Cover)/"
stego_dataset_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Stego)/"\
                        + str(embedding_rate) + "%/"
extension = ".pgm"

# command to run RS Analysis:
# for ($num = 1; $num -le 100; $num++){python aletheia.py rs C:/Users/faizz/"University Work"/
# "Year 4"/"Advanced Project"/Dataset/"BOSSbase (Stego)"/10%/LSB/"$num".pgm}

# initalise error metrics
MSE = MSE()
PSNR = PSNR()


def evaluate(folder, cover_dataset_path, stego_dataset_path):

    # initalise parameters
    total_mse = 0
    total_psnr = 0
    num_images = 10000

    stego_dataset_path = stego_dataset_path + folder + '/'

    # loop through image files
    for filename in range(1, 10001):

        filename_string = str(filename) + extension

        # load the cover image file
        cover_path = cover_dataset_path + filename_string
        cover = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)

        stego_path = stego_dataset_path + filename_string
        stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

        mean_squared_error = MSE.get_error(cover, stego)
        psnr = PSNR.get_error(cover, stego, mean_squared_error)

        total_mse += mean_squared_error
        total_psnr += psnr

        print(filename, mean_squared_error, psnr, folder)

    average_mse = total_mse / num_images
    average_psnr = total_psnr / num_images

    print(average_mse)
    print(average_psnr)


evaluate('Sobel', cover_dataset_path, stego_dataset_path)
