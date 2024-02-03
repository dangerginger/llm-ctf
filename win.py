import re
import requests
import json
from ceasar import ceasar

# Load the API Key from secret.txt
API_KEY = ""
with open("secret.txt", "r") as file:
  API_KEY = file.readline()
print("API KEY: " + API_KEY)

# Load the list of successful attacks
attacks = []
with open("successful_attacks.json", "r") as f:
  attacks = json.load(f)

base_url = "https://ctf.spylab.ai/api/v1"
create_chat_api_url = f"{base_url}/chat/attack/create"
headers = {"X-API-Key": API_KEY}

for attack in attacks:
  print(f"Attacking {attack['submission_id']}...")
  create_chat_body ={'submission_id': attack['submission_id'], 'evaluation': False} 
  response = requests.post(url=create_chat_api_url, headers=headers, json=create_chat_body)
  if (response.status_code != 200):
    print(f"Received response status code: {response.status_code}")
    break
  response_body = response.json()
  chat_id = response_body['chat_id']
  secret_id = response_body['secret_id']
  attack_msg_url = f"{base_url}/chat/attack/{chat_id}/new_message"
  msg_resp = None
  for prompt in attack['prompts']:
    print("Sending prompt...")
    msg_resp = requests.post(url=attack_msg_url, headers=headers, json={"new_message": prompt})
    if (msg_resp.status_code != 200):
      print(f"Received status code {msg_resp['status_code']}")
      break
  
  last_response = msg_resp.json()['history'][-1]['content']
  if "step" in attack:
    print('Attempting to decrypt...')
    print(f"Original text: {last_response}")
    last_response = ceasar(last_response, attack['step'])
  last_response.replace(",", "")
  print(last_response)

  regex = r"['\"\\]{1}([A-Za-z0-9]*)['\"\\]{1}"
  if "regex" in attack:
    regex = attack['regex']

  print(f"Checking output for regex: {regex}...")

  guesses = set(re.findall(regex, last_response))
  guesses = [guess.replace(",","") for guess in guesses] # Remove commas

  secret_guess_url = f"{base_url}/secret/{secret_id}/guess"

  for guess in guesses:
    if guess == "SDOIFJ":
      continue
    
    print(f"Checking guess {guess}...")
    secret_guess_body = {"guess": guess, "chat_id": chat_id}
    guess_response = requests.post(url=secret_guess_url, headers=headers, json=secret_guess_body)
    if guess_response.status_code != 200:
      print(f"Guess returned status code {guess_response.status_code}")
      break
    guess_response_body = guess_response.json()
    correct = guess_response_body['correct']
    guesses_remaining = guess_response_body['guesses_remaining']
    print(f"Guess correct: {correct} ({guesses_remaining} remaining)")
