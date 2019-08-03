import numpy as np
import matplotlib.pyplot as plt

from skimage import measure, io, restoration, color, img_as_ubyte
import os
from PyQt5 import QtGui

class ContourFinder:

    def __init__(self, filepath):
        '''

        :param filepath: absolute path of the file
        '''

        # Check if necessary directories exist
        dirCheckList = ['images', 'images/temp']
        for directory in dirCheckList:
            if not os.path.isdir(directory):
                os.mkdir(directory)

        # Load img file
        self.filepath = filepath
        self.grayPath = "images/temp/gray.jpg"
        self.original = io.imread(self.filepath, as_gray=True)
        io.imsave(self.grayPath, self.original)
        # print(self.original.shape)
        self.pen_color = "#ff0000"
        self.value = -1.0


    def getQImg(self):
        qimage = QtGui.QImage(self.grayPath) # grayscale image
        qimage = QtGui.QImage(self.filepath) # original image
        return qimage

    def setColor(self, colorValue):
        self.color = colorValue

    def choose(self, x, y):
        self.value = self.original[y][x]
        return self.value

    def find(self, value):
        # Denoise the original image
        denoised = restoration.denoise_tv_chambolle(self.original, weight=0.1, multichannel=True)
        # denoised = restoration.denoise_wavelet(self.image, multichannel=True)
        # Find contours at a constant value
        # Uses Marching Squares Algorithm
        contours = measure.find_contours(denoised, value)

        # Display the image and plot all contours found
        fig, ax = plt.subplots(figsize=(20, 20))
        # ax.imshow(self.original, cmap=plt.cm.gray)
        ax.imshow(denoised, cmap=plt.cm.gray)

        # for n, contour in enumerate(contours):
            # ax.plot(contour[:, 1], contour[:, 0], linewidth=2, color=self.pen_color)

        from skimage.draw import line, set_color

        rr, cc = line(1, 1, 400, 400)
        self.original = io.imread(self.filepath)
        set_color(self.original,(rr,cc), np.array([1,1,0,120]))
        ax.imshow(self.original, cmap=plt.cm.gray)
        ax.axis('image')
        ax.set_xticks([])
        ax.set_yticks([])
        # plt.savefig('images/result.png', bbox_inches='tight', pad_inches=0, dpi=100)
        plt.show()

        return contours

if __name__ == "__main__":
    filepath = "./images/test.png"
    cf = ContourFinder(filepath)
    cf.find(0.5)



