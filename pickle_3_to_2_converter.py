from sklearn.externals import joblib
import pickle
dictionary = joblib.load("xgboost_model_3.sav", mmap_mode=None)
print (dictionary)
outfile="xgboost_model_4.sav"
with open(outfile, 'wb') as pickle_file:
	pickle.dump(dictionary, pickle_file, protocol=2)

