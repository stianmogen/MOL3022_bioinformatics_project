from tensorflow import keras


def f1(y_true, y_pred):
    return 1

model = keras.models.load_model('./model/', custom_objects={'f1':f1}, compile=False)
model.compile(metrics=["accuracy", f1])
ans = model.predict(["EEDPDLKAAIQESLREAEEA"])
print(ans)


