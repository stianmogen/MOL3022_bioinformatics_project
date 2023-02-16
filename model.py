from keras import Input
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Bidirectional
from keras.models import Model


def create_model(max_sequence_length, num_words, num_tags):
    input_tensor = Input(shape=(max_sequence_length,))
    x = Embedding(input_dim=num_words, output_dim=128, input_length=max_sequence_length)(input_tensor)
    x = Bidirectional(LSTM(units=64, return_sequences=True, recurrent_dropout=0.1))(x)
    y = TimeDistributed(Dense(num_tags, activation="softmax"))(x)
    model = Model(input_tensor, y)
    return model

