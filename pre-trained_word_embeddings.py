# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 16:46:17 2018

@author: Jack
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import gensim
from gensim.models import FastText as fText
from gensim.models.keyedvectors import KeyedVectors

torch.manual_seed(1)

# Source for .vec file: https://fasttext.cc/docs/en/english-vectors.html
model = KeyedVectors.load_word2vec_format("C:\\Users\\ARL\\Documents\\CS5984\\wiki-news-300d-1M.vec")
v = model.most_similar("queen")
weights = torch.FloatTensor(model.vectors)

# Source for creating embedded layer: https://bit.ly/2uOfqgZ
def create_embedded_layer(weights, non_trainable=False):
    num_embeddings, embedding_dim = weights.size()
    emb_layer = nn.Embedding(num_embeddings, embedding_dim)
    emb_layer.load_state_dict({'weight' : weights})
    if non_trainable:
        emb_layer.weight.requires_grad= False
        
    return emb_layer, num_embeddings, embedding_dim

emb_layer, num_embeddings, embedding_dim = create_embedded_layer(weights)


    

