import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class GptScrapper:
  def __init__(self, model_name = "gpt-3.5-turbo"):
    system_def = open('./chatgpt-scrapper/data/system.txt', mode="r", encoding="utf-8").read()
    self.model_name = model_name
    self.messages = []
    self.messages.append({ "role": "system", "content": system_def })
    self.total_tokens = 0

  def chat(self, message):
    self.messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(model=self.model_name, messages=self.messages)
    reply = response["choices"][0]["message"]["content"]
    self.total_tokens += response["usage"]["total_tokens"]
    
    self.messages.append({"role": "assistant", "content": reply})

    return reply


gptScrapper = GptScrapper()

while True:
  message = input('\nuser > ')
  reply = gptScrapper.chat(message)
  print(f'\n{gptScrapper.model_name} ({gptScrapper.total_tokens}) > {reply}')
