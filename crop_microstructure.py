import glob
import numpy as np
from skimage.io import imread, imsave
import os

def quad_crop(image, w=224):
    """ crop out four panels from the center of the image """
    labels = np.array([['UL', 'UR'], ['LL', 'LR']])

    center = (np.array(image.shape) / 2).astype(int)
    x, y = center

    crops = []
    for idx in (0,1):
        xmin = x - (w * ((1-idx)%2))
        xmax = x + (w * (idx%2))
        for idy in (0,1):
            ymin = y - (w * ((1-idy)%2))
            ymax = y + (w * (idy%2))
            crop = image[xmin:xmax,ymin:ymax]
            crops.append((labels[idx,idy], crop))

    return crops

def cropper():
    paths = glob.glob('data/micrographs_new/*')
        #cropping given image into 4 sub -images
    for path in paths:
    #     print('cropping {}'.format(path))
        prefix, ext = os.path.splitext(os.path.basename(path))
        crops = quad_crop(imread(path, as_grey=True))
        for label, crop in crops:
            dest = '{}-crop{}.tif'.format(prefix, label)
            dest = os.path.join('data/crops_new', dest)
            imsave(dest, crop)