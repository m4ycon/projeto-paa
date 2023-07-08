import csv
import os
import json

filedir = os.path.dirname(os.path.realpath(__file__))

pokemons = {
  # pokemon_name: [{ tag: "type", patterns: ["What is the type of pokemon_name?"], responses: [pokemon_type] }]
}

with open(f'{filedir}/data/1st_gen.csv', mode="r", encoding="utf-8") as csv_file:
  csv_reader = csv.DictReader(csv_file)

  for i, row in enumerate(csv_reader):
    pokemon_name = row["name"]
    pokemons[pokemon_name] = []
    
    types = row["type1"] + ("" if row["type2"] == "" else " and " + row["type2"])
    pokemons[pokemon_name].append({
      "tag": "type",
      "patterns": [f"What is the type of {pokemon_name}?"],
      "responses": [f"{pokemon_name} is a {types} type pokemon.", f"It is a {types} type pokemon."]
    })

    abilities = row["abilities"].replace("[", "").replace("]", "").replace("'", "").split(r",\s?")
    abilities = ', '.join(abilities)
    pokemons[pokemon_name].append({
      "tag": "abilities",
      "patterns": [f"What are the abilities of {pokemon_name}?"],
      "responses": [f"{pokemon_name} has {abilities} abilities.", f"It has {abilities} abilities."]
    })

    legendary = "yes" if row["is_legendary"] == "1" else "no"
    legendary_comp = "" if row["is_legendary"] == "1" else "not"
    pokemons[pokemon_name].append({
      "tag": "is legendary",
      "patterns": [f"Is {pokemon_name} legendary?"],
      "responses": [legendary, f"{pokemon_name} is {legendary_comp} legendary.", f"It is {legendary_comp} legendary."]
    })

    weight = row["weight_kg"]
    pokemons[pokemon_name].append({ 
      "tag": "weight",
      "patterns": [f"What is the weight of {pokemon_name}?"],
      "responses": [weight +" kg"]
    })
    
    pokedex_number = row["pokedex_number"]
    pokemons[pokemon_name].append({
      "tag": "pokedex number",
      "patterns": [f"What is the pokedex number of {pokemon_name}?"],
      "responses": [f"{pokemon_name} is the pokemon number {pokedex_number} in the pokedex."]
    })
    
    height = row["height_m"]
    pokemons[pokemon_name].append({
      "tag": "height",
      "patterns": [f"What is the height of {pokemon_name}?"],
      "responses": [height + " meters"]
    })

    classification = row["classfication"]
    pokemons[pokemon_name].append({
      "tag": "classification",
      "patterns": [f"What is the classification of {pokemon_name}?"],
      "responses": [f"{pokemon_name} is a {classification}.", f"It is a {classification}."]
    })

    types = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fight', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'normal', 'poison', 'psychic', 'rock', 'steel', 'water']
    for t in types:
      is_weak = "yes" if float(row[f"against_{t}"]) > 1 else "no"
      is_weak_comp = "" if float(row[f"against_{t}"]) > 1 else "not"
      pokemons[pokemon_name].append({
        "tag": "weak against",
        "patterns": [f"Is {pokemon_name} weak against {t}?"],
        "responses": [is_weak, f"{pokemon_name} is {is_weak_comp} weak against {t}.", f"It is {is_weak_comp} weak against {t}."]
      })

      is_strong = "yes" if float(row[f"against_{t}"]) < 1 else "no"
      is_strong_comp = "" if float(row[f"against_{t}"]) < 1 else "not"
      pokemons[pokemon_name].append({
        "tag": "strong against",
        "patterns": [f"Is {pokemon_name} strong against {t}?"],
        "responses": [is_strong, f"{pokemon_name} is {is_strong_comp} strong against {t}.", f"It is {is_strong_comp} strong against {t}."]
      })


# build questions_answers
questions_answers = []
for pokemon_name, questions in pokemons.items():
  for q in questions:
    questions_answers.append({
      "tag": q["tag"],
      "patterns": q["patterns"],
      "responses": q["responses"],
    })

intents_json = {"intents": []}

if os.path.exists(f'{filedir}/data/intents.json'):
  intents_file = open(f'{filedir}/data/intents.json', mode="r", encoding="utf-8").read()
  intents_json = json.loads(intents_file)

intents_json["intents"].extend(questions_answers)

with open(f'{filedir}/data/intents.json', mode="w", encoding="utf-8") as intents_file:
  json.dump(intents_json, intents_file, indent=2)

print(f"Added {len(questions_answers)} questions to intents.json")
