import csv
import os
import json

filedir = os.path.dirname(os.path.realpath(__file__))

intents = {
  # tag_name: ["What is the type of pokemon_name?"] <- patterns
  "type": [],
  "abilities": [],
  "is_legendary": [],
  "classification": [],
}

with open(f'{filedir}/data/1st_gen.csv', mode="r", encoding="utf-8") as csv_file:
  csv_reader = csv.DictReader(csv_file)

  for i, row in enumerate(csv_reader):
    pokemon_name = row["name"]
    
    types = row["type1"] + ("" if row["type2"] == "" else " and " + row["type2"])
    intents["type"].extend([
      f"what type is {pokemon_name}?",
      f"what type of pokemon is {pokemon_name}?",
      f"what is {pokemon_name}'s type?",
      f"{pokemon_name}'s type?",
      f"type of {pokemon_name}?",
      f"what elemental type is {pokemon_name}?",
      f"what is the elemental type of {pokemon_name}?",
      f"{pokemon_name} elemental type?",
      f"elemental type of {pokemon_name}?",
      f"what category does {pokemon_name} belong to?",
      f"{pokemon_name} belongs to what category?",
      f"what is the category of {pokemon_name}?",
      f"category of {pokemon_name}?",
      f"{pokemon_name} category?",
      f"{pokemon_name}'s category?",
      f"{pokemon_name}'s elemental type?",
      f"what is the element of {pokemon_name}?",
    ])

    abilities = row["abilities"].replace("[", "").replace("]", "").replace("'", "").split(r",\s?")
    abilities = ', '.join(abilities)
    intents["abilities"].extend([
      f"What are the abilities of {pokemon_name}?",
      f"what are {pokemon_name}'s abilities?",
      f"what abilities does {pokemon_name} have?",
      f"what abilities does {pokemon_name} possess?",
      f"what abilities does {pokemon_name} know?",
      f"abilities of {pokemon_name}?",
      f"What are the abilities of {pokemon_name}?",
      f"What abilities does {pokemon_name} have?",
      f"What are {pokemon_name}'s abilities?",
      f"What are the special abilities of {pokemon_name}?",
      f"List the abilities of {pokemon_name}."
      f"What does {pokemon_name} do?",
      f"What does {pokemon_name} have?",
    ])

    legendary = "yes" if row["is_legendary"] == "1" else "no"
    legendary_comp = "" if row["is_legendary"] == "1" else "not"
    intents["is_legendary"].extend([
      f"Is {pokemon_name} legendary?",
      f"is {pokemon_name} a legendary pokemon?",
      f"is {pokemon_name} considered a legendary?",
      f"is {pokemon_name} a legendary?",
      f"is {pokemon_name} a legendary pokemon?",
      f"is {pokemon_name} considered as a legendary pokemon?",
      f"is {pokemon_name} one of the legendary pokemon?",
      f"does {pokemon_name} belong to the legendary pokemon?",
      f"is {pokemon_name} classified as a legendary pokemon?",
      f"is {pokemon_name} part of the legendary pokemon group?",
      f"is {pokemon_name} included in the legendary pokemon category?",
      f"is {pokemon_name} in the list of legendary pokemon?",
      f"is {pokemon_name} in the list of legends?",
      f"is {pokemon_name} among the legendary pokemon?",
      f"is {pokemon_name} recognized as a legendary pokemon?",
      f"is {pokemon_name} a legend?",
    ])

    classification = row["classfication"]
    intents["classification"].extend([
      f"What is the classification of {pokemon_name}?",
      f"how is {pokemon_name} classified?",
      f"what is {pokemon_name} classified as?",
      f"what is {pokemon_name}?",
      f"what {pokemon_name}?",
      f"what is the classification of {pokemon_name}?",
      f"what is the category of {pokemon_name}?",
      f"how is {pokemon_name} classified?",
      f"what group does {pokemon_name} belong to?",
      f"what is the classification of {pokemon_name} pokemon?",
      f"what is the categorization of {pokemon_name}?",
      f"what is the class of {pokemon_name}?",
      f"what is the designation of {pokemon_name}?",
      f"how is {pokemon_name} categorized?",
      f"what is the type of {pokemon_name}?"
    ])


# build questions_answers
questions_answers = []
for tag, patterns in intents.items():
  questions_answers.append({
    "tag": tag,
    "patterns": patterns,
    "responses": [tag],
  })

intents_json = {"intents": []}

if os.path.exists(f'{filedir}/data/intents.json'):
  intents_file = open(f'{filedir}/data/intents.json', mode="r", encoding="utf-8").read()
  intents_json = json.loads(intents_file)

intents_json["intents"].extend(questions_answers)

with open(f'{filedir}/data/intents.json', mode="w", encoding="utf-8") as intents_file:
  json.dump(intents_json, intents_file, indent=2)

print(f"Added {len(questions_answers)} questions to intents.json")
