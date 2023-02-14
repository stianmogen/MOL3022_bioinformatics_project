import json

import numpy as np
#from keras_preprocessing.sequence import pad_sequences
from keras.utils import pad_sequences
from keras.preprocessing.text import tokenizer_from_json
from tensorflow import keras
import tensorflow as tf



def f1(y_true, y_pred):
    return 1

def seq2ngrams(seqs, n=3):
    return np.array([list(seq[i:i + n] for i in range(len(seq))) for seq in seqs], dtype=object)


def predict(sequence):

    with open('tokenizer/tokenizer_encoder.json') as te:
        data = json.load(te)
        tokenizer_encoder = tokenizer_from_json(data)

    with open('tokenizer/tokenizer_decoder.json') as td:
        data = json.load(td)
        tokenizer_decoder = tokenizer_from_json(data)

    model = keras.models.load_model('./model/', custom_objects={'f1':f1}, compile=False)
    model.compile(metrics=["accuracy", f1])

    maxlen_seq = 128

    input_list = [sequence]
    input_grams = seq2ngrams(input_list)

    print(input_grams)
    input_data = tokenizer_encoder.texts_to_sequences(input_grams)
    input_data = pad_sequences(input_data, maxlen=maxlen_seq, padding='post')
    result = model.predict(input_data)
    pred = tf.argmax(result, axis=-1)
    print(pred)

    pred = tokenizer_decoder.sequences_to_texts(pred.numpy())

    return pred[0].replace(" ", "")



