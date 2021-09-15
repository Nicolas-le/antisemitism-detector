import fasttext

model = fasttext.train_supervised('data.train.txt')
print(model.predict("Hello I like to be here. It's nice"))
model.save_model("model_trained.bin")