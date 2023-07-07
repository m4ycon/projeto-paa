import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

model_name = "gpt-3.5-turbo"
messages = []
messages.append({
  "role": "system", 
  "content": "You are a scrapper robot that generates formatted questions and answers from pokemon universe"
})

print("Your new assistant is ready!")
while input != "quit()":
  message = input()
  messages.append({"role": "user", "content": message})
  response = openai.ChatCompletion.create(model=model_name, messages=messages)
  reply = response["choices"][0]["message"]["content"]
  messages.append({"role": "assistant", "content": reply})
  print("\n" + reply + "\n")
