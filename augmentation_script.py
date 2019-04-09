from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import skimage
from scipy.ndimage import rotate
from scipy.ndimage import zoom
import scipy.misc
import tensorflow as tf
import os
f = []
from os import walk
for (dirpath, dirnames, filenames) in walk('./augmented/'):
	f.extend(filenames)
	break
for file in f:
	only_filename=os.path.splitext(file)[0]
	img = Image.open('./augmented/'+file)
	img = np.array(img)
	flipped_img = np.fliplr(img)
	scipy.misc.imsave('./augmented/'+only_filename+'_flipped.tif',flipped_img) 
	scale_out = skimage.transform.rescale(img, scale=4, mode='constant')
	scipy.misc.imsave('./augmented/'+only_filename+'_scaled.tif',scale_out)
	rot90 = rotate(img, 90, reshape=True)
	scipy.misc.imsave('./augmented/'+only_filename+'_rotated_90.tif',rot90)
	rot180 = rotate(img, 180, reshape=True)
	scipy.misc.imsave('./augmented/'+only_filename+'_rotated_180.tif',rot180)