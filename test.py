from tensorflow import keras
model = keras.models.load_model('./model/')

ans = model.predict("EEDPDLKAAIQESLREAEEA")
print(ans)


