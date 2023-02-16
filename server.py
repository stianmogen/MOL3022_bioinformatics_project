from keras.preprocessing import sequence
import numpy as np
from typing import Dict, Any


from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .predict import predict

#import keras


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


aa_to_index = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10, 'N': 11, 'P': 12, 'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19}
def create_data(seq):
    data = np.array(20)
    data.fill(0)
    for letter in seq:
        if letter in aa_to_index:
            data[aa_to_index[letter]] = 1
    return data



class Sequence(BaseModel):
    sequence: str


@app.post("/predict")
async def use_predict(data: Sequence):
    ans = predict(data.sequence)
    return { "ans": ans, "sequence": data.sequence }

