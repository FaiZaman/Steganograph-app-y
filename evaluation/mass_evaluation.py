import cv2
from MSE import MSE
from PSNR import PSNR

# initialise paths
cover_dataset_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Cover)/"
stego_dataset_path = "C:/Users/faizz/University Work/Year 4/Advanced Project/Dataset/BOSSbase (Stego)/"
extension = ".pgm"

# command to run ensemble classifier:
# python aletheia.py e4s-predict models/e4s_srm_bossbase_lsbm0.10_gs.model srm sample_images/1_lsb.pgm


def evaluate(folder):

    # initalise error metrics and parameters
    MSE = MSE()
    PSNR = PSNR()
    total_mse = 0
    total_psnr = 0
    num_images = 10000

    stego_dataset_path = stego_dataset_path + folder

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

        print(filename, mean_squared_error, psnr)

    average_mse = total_mse / num_images
    average_psnr = total_psnr / num_images

    print(average_mse)
    print(average_psnr)


evaluate('LSB')
