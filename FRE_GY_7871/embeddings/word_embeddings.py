import os

from gensim.models.keyedvectors import KeyedVectors
import gensim.downloader as api
import requests

from utils import filename, create_path

W2VDIR = "data/w2v/"
ORIGINAL_W2V = "GoogleNews-vectors-negative300.bin.gz"
W2V_SMALL = "GoogleNews-vectors-negative300_top500k.kv"


def load_word_vector_model(num_most_common_words=500000):
    """
    load google word2vec model from gensim api
    """
    orig_model = api.load('word2vec-google-news-300')
    words = orig_model.index2entity[:num_most_common_words]
    kv = KeyedVectors(vector_size=orig_model.wv.vector_size)

    vectors = []
    for word in words:
        vectors.append(orig_model.get_vector(word))

    # adds keys (words) & vectors as batch
    kv.add(words, vectors)

    return kv


def get_word_embeddings(word_emb_model):
    """
    Word2Vec embeddings
    """
    word_list = word_emb_model.index2entity
    vectors = []
    for word in word_list:
        vectors.append(word_emb_model.get_vector(word))

    return vectors, word_list

