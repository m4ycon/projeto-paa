import random
import json
import pickle
import numpy as np
import os

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from tensorflow.keras.models import load_model

filedir = os.path.dirname(os.path.realpath(__file__))

try:
  nltk.word_tokenize('test')
  stopwords.words('english')
except LookupError:
  print('Downloading NLTK packages...')
  nltk.download('punkt')
  nltk.download('stopwords')


class ModelLoader:
  def __init__(self, model_name='pguess', intents_file='pguess_intents_backup.json', min_confidence=0.70):
    self.lemmatizer = WordNetLemmatizer()
    self.stop_words = stopwords.words('english')
    self.min_confidence = min_confidence

    intents_file = open(f'{filedir}/data/pguess_intents_backup.json', mode="r", encoding="utf-8").read()
    self.list_of_intents = json.loads(intents_file)

    self.words = pickle.load(open(f'{filedir}/models/{model_name}/words.pkl', mode="rb"))
    self.classes = pickle.load(open(f'{filedir}/models/{model_name}/classes.pkl', mode="rb"))
    self.model = load_model(f'{filedir}/models/{model_name}/model.keras')

  def clean_up_sentence(self, sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [word for word in sentence_words if word.lower() not in self.stop_words]
    sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


  def bag_of_words(self, sentence):
    sentence_words = self.clean_up_sentence(sentence)
    bag = [0] * len(self.words)
    for w in sentence_words:
      for i, word in enumerate(self.words):
        if word == w:
          bag[i] = 1
    return np.array(bag)


  def predict_class(self, sentence):
    bow = self.bag_of_words(sentence)
    res = self.model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 1 - self.min_confidence
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": self.classes[r[0]], "probability": str(r[1])} for r in results]


  def get_response(self, message):
    intents_list = self.predict_class(message)
    tag = intents_list[0]['intent']
    for i in self.list_of_intents:
      if i['tag'] == tag:
        return random.choice(i['responses'])


model = ModelLoader('pguess', 'pguess_intents_backup.json')

print("Welcome to the Pokemon Chatbot!")
while True:
  message = input("You > ")
  res = model.get_response(message)
  print(f"Bot > {res}")

