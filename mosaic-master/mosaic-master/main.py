from itertools import product  # to iterate through input image
import numpy as np
import cv2  # numpy for manipulating images
import os  # to manipulate files and directories

if __name__ == '__main__':

    piece_size = 20  # size of pieces

    image_in = cv2.imread("input.jpg")  # default = IMREAD_COLOR
    h, w, _ = image_in.shape  # height, width, channels
    im = np.zeros((h, w, 3), np.uint8)  # output image, initially zeroes, 8 bit

    dataset = []
    avg_color = []

    for file in os.listdir(os.getcwd()+"/dataset"):  # 347 files
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
            path = "dataset/" + file
            image = cv2.imread(path)  # default = IMREAD_COLOR
            image = cv2.resize(image, (piece_size, piece_size))  # resize mosaic pieces
            dataset.append(image)

            # average colors of images in dataset
            avg_color_row = np.average(image, axis=0)  # take the average of all the rows.
            avg_color.append(np.average(avg_color_row, axis=0))  # take the avg from the first average(), 2D matrix

    for col, row in product(range(int(w / piece_size)), range(int(h / piece_size))):  # cart product of rows and cols
        # choose a square from input image equal to one patch size
        piece = image_in[row * piece_size: (row + 1) * piece_size, col * piece_size: (col + 1) * piece_size]

        # average color of this piece
        piece_color_row = np.average(piece, axis=0)  # take the average of all the rows.
        piece_color = np.average(piece_color_row, axis=0)  # again take the avg from the first average(), 2D matrix

        # compare average colors by euclidean distance, find the best match
        euclid_dist = np.linalg.norm(piece_color - avg_color, axis=1)
        index = np.argmin(euclid_dist)  # index of minimal euclid_dist

        # fill the square with chosen patch image
        im[row * piece_size: (row + 1) * piece_size, col * piece_size: (col + 1) * piece_size] = dataset[index]

    cv2.imwrite("output.jpg", im)  # output image
