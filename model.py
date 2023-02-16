import numpy as np
from keras import Input
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Bidirectional, Dropout, MultiHeadAttention, \
    LayerNormalization, Conv1D, GlobalMaxPooling1D, Conv2D, GlobalMaxPooling2D
from keras.models import Model


def create_lstm_model(max_sequence_length, num_words, num_tags):
    input_tensor = Input(shape=(max_sequence_length,))
    x = Embedding(input_dim=num_words, output_dim=128, input_length=max_sequence_length)(input_tensor)
    x = Bidirectional(LSTM(units=64, return_sequences=True, recurrent_dropout=0.1))(x)
    y = TimeDistributed(Dense(num_tags, activation="softmax"))(x)
    model = Model(input_tensor, y)
    return model


def create_transformer_model(max_sequence_length, num_words, num_tags, dropout_rate=0.1,
                             num_heads=8, d_model=128, dense_size=64):
    input_tensor = Input(shape=((max_sequence_length, )))

    # Embedding layer
    x = Embedding(input_dim=num_words, output_dim=d_model, input_length=max_sequence_length)(input_tensor)

    # Positional encoding
    pos_encoding = np.array([
        [pos / np.power(10000, 2. * i / d_model) for i in range(d_model)]
        if pos != 0 else np.zeros(d_model) for pos in range(max_sequence_length)])
    x = x + pos_encoding

    # Dropout
    x = Dropout(rate=dropout_rate)(x)

    # Multi-head attention
    x = MultiHeadAttention(num_heads=num_heads, key_dim=d_model)(x, x)
    x = LayerNormalization(epsilon=1e-6)(x)

    # Feed-forward network
    y = Dense(units=dense_size, activation='relu')(x)
    y = Dropout(rate=dropout_rate)(y)
    y = TimeDistributed(Dense(units=num_tags, activation='softmax'))(y)

    # Model
    model = Model(input_tensor, y)

    return model
