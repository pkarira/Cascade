from collections import defaultdict
import pickle
import os
import h5py
import numpy as np
def max_vote(results):
    ans = []
    d = defaultdict(int)
    for i in results:
        d[i] += 1
    result = max(d.items(), key=lambda x: x[1])[1]
    for i in d:
        if d[i]==result:
            ans.append(i)
    print (ans)
    return ans

def load_representations(datafile):
    # grab image representations from hdf5 file
    keys, features = [], []

    with h5py.File(datafile, 'r') as f:
        for key in f:
            keys.append(key)
            features.append(f[key][...])

    return np.array(keys),np.array(features)

def classifier():
    feature_file=  os.listdir('data/cropped_new/features_new')
    datafile = 'data/cropped_new/features_new/'+feature_file[0]
    keys, features = load_representations(datafile)
    Xtest = features
    #     Xtest = X / np.linalg.norm(X, axis=1)[:,np.newaxis]

    filename = 'xgboost_model_4.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(Xtest)
    return (max_vote(result))