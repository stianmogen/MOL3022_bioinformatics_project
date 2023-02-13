import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/2018-06-06-ss.cleaned.csv')
df.len.hist(bins=100)
print(df.shape)

def seq2ngrams(seqs, n=3):
    # seq.ljust(128)[:128] pads each seq to 128 characters with blank lines at end, to avoid inhomogeneous shape error
    return np.array([[seq[i:i+n] for i in range(len(seq.ljust(128)[:128]))] for seq in seqs])

maxlen_seq = 128
#input_seqs, target_seqs = df[['seq', 'sst3']][(df.len <= maxlen_seq) & (~df.has_nonstd_aa)]

selected_rows = df[(df['len'] <= maxlen_seq) & (~df['has_nonstd_aa'])]
input_seqs = selected_rows['seq'].values
target_seqs = selected_rows['sst3'].values
input_grams = seq2ngrams(input_seqs)
print(len(input_seqs))
print(input_grams)


### preprocess

from keras.preprocessing import text, sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical


tokenizer_encoder = Tokenizer()
tokenizer_encoder.fit_on_texts(input_grams)
input_data = tokenizer_encoder.texts_to_sequences(input_grams)
input_data = [tokenizer_decoder.texts_to_sequences(input_gram) for input_gram in input_grams]
input_data = sequence.pad_sequences(input_data, maxlen=maxlen_seq, padding='post')

tokenizer_decoder = Tokenizer(char_level=True)
tokenizer_decoder.fit_on_texts(target_seqs)
target_data = [tokenizer_decoder.texts_to_sequences(target_seq) for target_seq in target_seqs]
target_data = sequence.pad_sequences(target_data, maxlen=maxlen_seq, padding='post')
target_data = to_categorical(target_data)
input_data.shape, target_data.shape







