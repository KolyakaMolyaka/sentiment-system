import nltk

nltk.download('punkt')
nltk.download('stopwords')

from navec import Navec
import wget

url = 'https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar'
filename = wget.download(url)
navec = Navec.load(filename)
