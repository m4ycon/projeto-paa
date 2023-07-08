print('Initializing...')

import random
import json
import pickle
import numpy as np
import os

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

from timeit import default_timer as timer
t_start = timer()


filedir = os.path.dirname(os.path.realpath(__file__))

try:
  nltk.word_tokenize('test')
  stopwords.words('english')
except LookupError:
  print('Downloading NLTK packages...')
  nltk.download('punkt')
  nltk.download('stopwords')

print('NLTK packages loaded.')

print('Expects intents.json to be in the following format:')
print('''
[
  {
    "tag": "type",
    "patterns": [
      "what type is pokemon_name?",
      "what type of pokemon is pokemon_name?",
    ],
    "responses": [
      "pokemon_name is type."
    ]
  }
]
''')
      

intents_filename = input('Intents path (eg. ./data/intents.json): ')
output_foldername = input('Output folder name (eg. mymodel): ')
epochs = input('Epochs (default 30): ')
learning_rate = input('Learning rate (default 0.01): ')
batch_size = input('Batch size (default 16): ')

epochs = 30 if epochs == '' else int(epochs)
learning_rate = 0.01 if learning_rate == '' else float(learning_rate)
batch_size = 16 if batch_size == '' else int(batch_size)

print('=' * 50)
print('Loading data...')

model_folder = f'{filedir}/models/{output_foldername}'

lemmatizer = WordNetLemmatizer()

intents_file = open(f'{filedir}/{intents_filename}', mode="r", encoding="utf-8").read()
intents = json.loads(intents_file)

words, classes, documents = [], [], []
ignore_letters = ['?', '!', '.', ',']
stop_words = stopwords.words('english')

for intent in intents:
  for pattern in intent['patterns']:
    word_list = nltk.word_tokenize(pattern)
    word_list = [word for word in word_list if word.lower() not in stop_words]
    words.extend(word_list)
    documents.append((word_list, intent['tag']))

    if intent['tag'] not in classes:
      classes.append(intent['tag'])

print('Data loaded.')
print('=' * 50)
print('Creating training data...')

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

if not os.path.exists(f'{model_folder}'):
  os.makedirs(f'{model_folder}')

pickle.dump(words, open(f'{model_folder}/words.pkl', mode="wb"))
pickle.dump(classes, open(f'{model_folder}/classes.pkl', mode="wb"))

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

print('Training data created.')
print('=' * 50)
print('Creating model...')

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=learning_rate, weight_decay=1e-6, momentum=.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=2)
model_path = f'{model_folder}/model.keras'
model.save(model_path, hist)

execution_time = int(timer() - t_start)
minutes = execution_time // 60
seconds = execution_time % 60
exec_time_str = f'{minutes}m {seconds}s'

print(f'Training completed in {exec_time_str} seconds with {len(train_x)} training samples.')
print(f'Model saved to {model_path}')
