import random
import json
import pickle
import numpy as np
import os

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


filedir = os.path.dirname(os.path.realpath(__file__))

try:
  nltk.word_tokenize('test')
except LookupError:
  print('Downloading NLTK packages...')
  nltk.download('punkt')


lemmatizer = WordNetLemmatizer()

intents_file = open(f'{filedir}/data/intents.json', mode="r", encoding="utf-8").read()
intents = json.loads(intents_file)

words, classes, documents = [], [], []
ignore_letters = ['?', '!', '.', ',']

for intent in intents['intents']:
  for pattern in intent['patterns']:
    word_list = nltk.word_tokenize(pattern)
    words.extend(word_list)
    documents.append((word_list, intent['tag']))

    if intent['tag'] not in classes:
      classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open(f'{filedir}/data/words.pkl', mode="wb"))
pickle.dump(classes, open(f'{filedir}/data/classes.pkl', mode="wb"))

training = []
output_empty = [0] * len(classes)

for document in documents:
  bag = []
  word_patterns = document[0]
  word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
  for word in words:
    bag.append(1 if word in word_patterns else 0)

  output_row = list(output_empty)
  output_row[classes.index(document[1])] = 1
  training.append(bag + output_row)

random.shuffle(training)

training = np.array(training)

train_x = training[:, :len(words)]
train_y = training[:, len(words):]

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=.01, weight_decay=1e-6, momentum=.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
model.save(f'{filedir}/data/pokemon_gpt.h5', hist)
print('Done')


