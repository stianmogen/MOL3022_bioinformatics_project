from typing import Union
import numpy as np

from fastapi import FastAPI
from pydantic import BaseModel
#import keras


app = FastAPI()


aa_to_index = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10, 'N': 11, 'P': 12, 'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19}
def create_data(seq):
    data = np.array(20)
    data.fill(0)
    for letter in seq:
        if letter in aa_to_index:
            data[aa_to_index[letter]] = 1
    return data



class Sequence(BaseModel):
    string: str

@app.post("/predict")
def update_item(sequence: Sequence):
    #model = keras.models.load_model('path/to/location')
    #data = create_data(sequence.string)
    return { "ans": "it worked" }

