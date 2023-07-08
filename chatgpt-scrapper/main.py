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


lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')

intents_file = open(f'{filedir}/data/intents.json', mode="r", encoding="utf-8").read()
intents_json = json.loads(intents_file)

words = pickle.load(open(f'{filedir}/data/words.pkl', mode="rb"))
classes = pickle.load(open(f'{filedir}/data/classes.pkl', mode="rb"))
model = load_model(f'{filedir}/data/pokemon_gpt.keras')

class PokemonGpt:
  def clean_up_sentence(self, sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [word for word in sentence_words if word.lower() not in stop_words]
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


  def bag_of_words(self, sentence):
    sentence_words = self.clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
      for i, word in enumerate(words):
        if word == w:
          bag[i] = 1
    return np.array(bag)


  def predict_class(self, sentence):
    bow = self.bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]


  def get_response(self, message):
    intents_list = self.predict_class(message)
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
      if i['tag'] == tag:
        return random.choice(i['responses'])


pokemonGpt = PokemonGpt()

print("Welcome to the Pokemon Chatbot!")
while True:
  message = input("You: ")
  res = pokemonGpt.get_response(message)
  print(f"Bot: {res}")

