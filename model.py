import io
import json

import numpy as np
import pandas as pd
import tensorflow as tf
from keras import Input
from keras import backend as K
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Bidirectional
from keras.models import Model
from keras.preprocessing.text import Tokenizer
from keras.utils.np_utils import to_categorical
# from keras.utils import to_categorical
from keras_preprocessing.sequence import pad_sequences
# from keras.utils import pad_sequences
from sklearn.model_selection import train_test_split

df = pd.read_csv('data/2018-06-06-ss.cleaned.csv')
df.len.hist(bins=100)
print(df.shape)


def seq2ngrams(seqs, n=3):
    return np.array([[seq[i:i + n] for i in range(len(seq))] for seq in seqs], dtype=object)


maxlen_seq = 128
input_seqs, target_seqs = df[['seq', 'sst3']][(df.len <= maxlen_seq) & (~df.has_nonstd_aa)].values.T

input_grams = seq2ngrams(input_seqs)

tokenizer_encoder = Tokenizer()
tokenizer_encoder.fit_on_texts(input_grams)
input_data = tokenizer_encoder.texts_to_sequences(input_grams)
input_data = pad_sequences(input_data, maxlen=maxlen_seq, padding='post')

tokenizer_decoder = Tokenizer(char_level=True)
tokenizer_decoder.fit_on_texts(target_seqs)
target_data = tokenizer_decoder.texts_to_sequences(target_seqs)
target_data = pad_sequences(target_data, maxlen=maxlen_seq, padding='post')
target_data = to_categorical(target_data)
print(input_data.shape, target_data.shape)

n_words = len(tokenizer_encoder.word_index) + 1
n_tags = len(tokenizer_decoder.word_index) + 1
print(n_words, n_tags)


input = Input(shape=(maxlen_seq,))
x = Embedding(input_dim=n_words, output_dim=128, input_length=maxlen_seq)(input)
x = Bidirectional(LSTM(units=64, return_sequences=True, recurrent_dropout=0.1))(x)
y = TimeDistributed(Dense(n_tags, activation="softmax"))(x)
model = Model(input, y)
model.summary()


def q3_acc(y_true, y_pred):
    y = tf.argmax(y_true, axis=-1)
    y_ = tf.argmax(y_pred, axis=-1)
    mask = tf.greater(y, 0)
    return K.cast(K.equal(tf.boolean_mask(y, mask), tf.boolean_mask(y_, mask)), K.floatx())


model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy", q3_acc])

X_train, X_test, y_train, y_test = train_test_split(input_data, target_data, test_size=.4, random_state=0)
seq_train, seq_test, target_train, target_test = train_test_split(input_seqs, target_seqs, test_size=.4, random_state=0)

model.fit(X_train, y_train, batch_size=128, epochs=5, validation_data=(X_test, y_test), verbose=1)
model.save('./model')

tokenizer_encoder_json = tokenizer_encoder.to_json()
with io.open('tokenizer/tokenizer_encoder.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer_encoder_json, ensure_ascii=False))

tokenizer_decoder_json = tokenizer_decoder.to_json()
with io.open('tokenizer/tokenizer_decoder.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer_decoder_json, ensure_ascii=False))

