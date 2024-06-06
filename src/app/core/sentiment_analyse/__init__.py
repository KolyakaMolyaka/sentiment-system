import nltk

RUSSIAN_DEFAULT_STOP_WORDS = nltk.corpus.stopwords.words('russian')

import pickle
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
# load models
modelsdir_path = '/models'
with open(dir_path + rf'{modelsdir_path}/SIMPLE_VECTORIZATION_PRETRAINED_MODEL.pkl', 'rb') as f:
	simple_vpm = pickle.load(f)
with open(dir_path + rf'{modelsdir_path}/EMBEDDINGS_PRETRAINED_MODEL.pkl', 'rb') as f:
	embedding_vpm = pickle.load(f)
