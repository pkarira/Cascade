import os
import h5py
import json
import click
import numpy as np
from functools import partial
from sklearn.externals import joblib
from sklearn.cluster import MiniBatchKMeans

# needed with slurm to see local python library under working dir
import sys
sys.path.append(os.getcwd())

from mfeat import io
from mfeat import encode

import numpy as np
from scipy.misc import imresize
from skimage.color import gray2rgb

from keras.models import Model
from keras import backend as K
from keras.applications.vgg16 import VGG16, preprocess_input

cnn = VGG16(include_top=False, weights='imagenet')
layer_id = {layer.name: idx for idx, layer in enumerate(cnn.layers)}

def image_tensor(image):
    """ replicate a grayscale image onto the three channels of an RGB image
        and reshape into a tensor appropriate for keras
    """
    image3d = gray2rgb(image).astype(np.float32)
    x = 255*image3d
    x = np.expand_dims(x, axis=0)
    y = preprocess_input(x)
    return y

def tensor_to_features(X, subsample=None):
    
    """ convert feature map tensor to numpy data matrix {nsamples, nchannels} """
    
    # transpose array so that map dimensions are on the last axis
    features = X.transpose(0,2,3,1) # to [batch, height, width, channels]
    features = features.reshape((-1, features.shape[-1])) # to [feature, channels]

    if subsample >= 1.0 or subsample <= 0:
        subsample = None

    if subsample is not None:
        choice = np.sort(
            np.random.choice(range(features.shape[0]), size=int(subsample*features.shape[0]), replace=False)
        )
        features = features[choice]
        
    return features

def cnn_features(image, layername, fraction=None):
    """ use keras to obtain cnn feature map """
    
    model = Model(input=cnn.input, output=cnn.get_layer(layername).output)
    out = model.predict(image_tensor(image))
    return tensor_to_features(out, subsample=fraction)

def ensure_dir(path):
    """ mkdir -p """
    try: os.makedirs(path)
    except: pass

def featuremap(micrographs_json, n_clusters, style, encoding, layername, multiscale):
    """ compute image representations for each image enumerated in micrographs_json 
        results are stored in HDF5 keyed by the image ids in micrographs_json
    """
    dataset_dir, __ = os.path.split(micrographs_json)

    barheight = 0
    if 'full' in dataset_dir:
        barheight = 38
        
    ensure_dir(os.path.join(dataset_dir, 'dictionary_new'))
    ensure_dir(os.path.join(dataset_dir, 'features_new'))
                
    if style in ['vgg16']:
        if multiscale:
            method = '{}_multiscale_{}'.format(style, layername)
        else:
            method = '{}_{}'.format(style, layername)
    else:
        method = style
        
    metadata = {
        'dir': dataset_dir,
        'n_clusters': n_clusters,
        'method': method,
        'encoding': encoding
    }
    
    # obtain a dataset
    with open(micrographs_json, 'r') as f:
        micrograph_dataset = json.load(f)

    # work with sorted micrograph keys...
    keys = sorted(micrograph_dataset.keys())
    micrographs = [micrograph_dataset[key] for key in keys]
    micrographs = [io.load_image(m, barheight=barheight) for m in micrographs]
    # set up paths
    dictionary_file = '{dir}/dictionary_new/{method}-kmeans-{n_clusters}.pkl'.format(**metadata)
    featurefile = '{dir}/features_new/{method}-{encoding}-{n_clusters}.h5'.format(**metadata)

    if style == 'vgg16':
        if multiscale:
            extract_func = lambda mic, fraction=1.0: cnn.multiscale_cnn_features(mic, layername, fraction=fraction)
        else:
            extract_func = lambda mic, fraction=1.0: cnn_features(mic, layername, fraction=fraction)
    training_fraction = 0.1
    results = map(partial(extract_func, fraction=training_fraction), micrographs)
    results =  list(results)
    results = tuple(results)
    features = np.vstack(results)
    filename = 'data/cropped/dictionary/vgg16_block4_conv3-kmeans-32_2.pkl'
    dictionary = joblib.load(filename, mmap_mode=None)

    if encoding == 'bow':
        encode_func = lambda mic: encode.bag_of_words(extract_func(mic), dictionary)
    elif encoding == 'vlad':
        encode_func = lambda mic: encode.vlad(extract_func(mic), dictionary)
        
    features = map(encode_func, micrographs)
    with h5py.File(featurefile, 'w') as f:
        for key, feature in zip(keys, features):
            f[key] = feature
    return

def feature_generater():
    layer_choices = layer_id.keys()
    for conv in [4]:
        featuremap('data/cropped_new/micrographs.json', 32, 'vgg16', 'vlad', 'block{}_conv3'.format(conv), False)