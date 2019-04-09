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
def side_center_crop(image,w=224):
    labels = np.array([['UL', 'UR'], ['LL', 'LR']])
    size = np.array(image.shape).astype(int)
    x, y = size
    crops = []
    crop = image[0:w,0:w]
    crops.append(('UL', crop))
    crop = image[x-w:,0:w]
    crops.append(('UR',crop))
    crop  = image[0:w,y-w:]
    crops.append(('LL',crop))
    crop = image[x-w:,y-w:]
    crops.append(('LR',crop))
    center = (np.array(image.shape) / 2).astype(int)
    x, y = center
    crop = image[x-w/2:x+w/2,y-w/2:y+w/2]
    crops.append(('CC', crop))
    return crops

def single_crop(image, w=224):
    center = (np.array(image.shape) / 2).astype(int)
    x, y = center
    crops = []
    print x-w/2
    print x+w/2
    print y-w/2
    print y+w/2
    crop = image[x-w/2:x+w/2,y-w/2:y+w/2]
    crops.append(('CC', crop))
    return crops

def cropper():
    paths = glob.glob('data/micrographs_new/*')
        #cropping given image into 4 sub -images
    for path in paths:
    #     print('cropping {}'.format(path))
        prefix, ext = os.path.splitext(os.path.basename(path))
        image = imread(path, as_grey=True)
        if image.shape[0]<448 or image.shape[1]<448:
            crops = side_center_crop(image)
        else:
            crops = quad_crop(image)
        for label, crop in crops:
            dest = '{}-crop{}.tif'.format(prefix, label)
            dest = os.path.join('data/crops_new', dest)
            imsave(dest, crop)