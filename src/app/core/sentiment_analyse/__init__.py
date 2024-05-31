import nltk

nltk.download('punkt')
nltk.download('stopwords')

from navec import Navec
import wget

url = 'https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar'
filename = wget.download(url)
navec = Navec.load(filename)

import pickle
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
# load models
modelsdir_path = '/models'
with open(dir_path + rf'{modelsdir_path}/SIMPLE_VECTORIZATION_PRETRAINED_MODEL.pkl', 'rb') as f:
	simple_vpm = pickle.load(f)
with open(dir_path + rf'{modelsdir_path}/EMBEDDINGS_PRETRAINED_MODEL.pkl', 'rb') as f:
	embedding_vpm = pickle.load(f)
