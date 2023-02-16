import io
import json

import keras.callbacks
import numpy as np
import pandas as pd
import tensorflow as tf
from keras import backend as K
from keras.preprocessing.text import Tokenizer
from keras.utils.np_utils import to_categorical
# from keras.utils import to_categorical
# from keras_preprocessing.sequence import pad_sequences
from keras.utils import pad_sequences
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

from model import create_model


def sequence_to_ngrams(seqs, n=3):
    """This function take a list of string as input and return a list of ngrams for each string"""
    return np.array([[seq[i:i + n] for i in range(len(seq))] for seq in seqs], dtype=object)


# This method saves a tokenizer for later use
def save_tokenizer(file_path, tokenizer, encoding='utf-8'):
    """This function saves a tokenizer for later use"""
    tokenizer_json = tokenizer.to_json()
    with io.open(file_path, 'w', encoding=encoding) as f:
        f.write(json.dumps(tokenizer_json, ensure_ascii=False))


# This m
def get_data(file_path, max_sequence_length, input_column, target_column):
    """This method reads a csv file and return inputs and targets based on desired columns"""
    df = pd.read_csv(file_path)
    df.len.hist(bins=100)

    inputs, targets = df[[input_column, target_column]][
        (df.len <= max_sequence_length) & (~df.has_nonstd_aa)].values.T

    return inputs, targets


def preprocess(data, max_sequence_length, char_level=False, is_target=False):
    """
    This method tokenizes the data and pads the data if it is shorter than maximum sequence length.
    If the data is target data it also transforms it into a one-hot vector using to_categorical
    """
    tokenizer = Tokenizer(char_level=char_level)
    tokenizer.fit_on_texts(data)
    data = tokenizer.texts_to_sequences(data)
    data = pad_sequences(data, maxlen=max_sequence_length, padding='post')
    if is_target:
        data = to_categorical(data)

    return data, tokenizer


def q3_acc(y_true, y_pred):
    """This method measures the accuracy of the m"""
    y = tf.argmax(y_true, axis=-1)
    y_ = tf.argmax(y_pred, axis=-1)
    mask = tf.greater(y, 0)
    return K.cast(K.equal(tf.boolean_mask(y, mask), tf.boolean_mask(y_, mask)), K.floatx())


input_csv_file = 'data/2018-06-06-ss.cleaned.csv'
MAX_SEQUENCE_LENGTH = 128
BATCH_SIZE = 128
EPOCHS = 25
VAL_SIZE = 0.4
RANDOM_STATE = 0

input_sequences, target_sequences = get_data(file_path=input_csv_file,
                                             max_sequence_length=MAX_SEQUENCE_LENGTH,
                                             input_column='seq',
                                             target_column='sst3')

input_ngrams = sequence_to_ngrams(input_sequences)

input_data, input_tokenizer = preprocess(data=input_ngrams,
                                         max_sequence_length=MAX_SEQUENCE_LENGTH)

target_data, target_tokenizer = preprocess(data=target_sequences,
                                           max_sequence_length=MAX_SEQUENCE_LENGTH,
                                           char_level=True,
                                           is_target=True)


num_words = len(input_tokenizer.word_index) + 1
num_tags = len(target_tokenizer.word_index) + 1

model = create_model(max_sequence_length=MAX_SEQUENCE_LENGTH,
                     num_words=num_words,
                     num_tags=num_tags)

model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy", q3_acc])

x_train, x_val, y_train, y_val = train_test_split(input_data, target_data, test_size=VAL_SIZE,
                                                  random_state=RANDOM_STATE)

checkpoints = keras.callbacks.ModelCheckpoint("protein.h5", save_best_only=True)
history = model.fit(x_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data=(x_val, y_val), verbose=1, callbacks=[checkpoints])
model.save('./model')

save_tokenizer(file_path="tokenizer/input_tokenizer.json", tokenizer=input_tokenizer)
save_tokenizer(file_path="tokenizer/target_tokenizer.json", tokenizer=target_tokenizer)

model_history = pd.DataFrame(history.history)
model_history['epoch'] = history.epoch

fig, ax = plt.subplots(1, figsize=(8,6))
num_epochs = model_history.shape[0]

print(model_history)

ax.plot(np.arange(0, num_epochs), model_history["accuracy"],
        label="Training accuracy"),
ax.plot(np.arange(0, num_epochs), model_history["q3_acc"],
        label="Training q3 accuracy")
ax.plot(np.arange(0, num_epochs), model_history["val_accuracy"],
        label="Validation accuracy")
ax.plot(np.arange(0, num_epochs), model_history["val_q3_acc"],
        label="Validation q3 accuracy")
ax.legend()

plt.tight_layout()
plt.show()

ax.plot(np.arange(0, num_epochs), model_history["loss"],
        label="Training loss"),
ax.plot(np.arange(0, num_epochs), model_history["val_loss"],
        label="Validation loss")
ax.legend()

plt.tight_layout()
plt.show()
