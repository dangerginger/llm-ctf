import re
import requests
import json


API_KEY = ""
with open("secret.txt", "r") as file:
  API_KEY = file.readline()
print("API KEY: " + API_KEY)

targets = [line.strip() for line in open("target_ids.txt", "r")]
print("Target List\n================")
for t in targets:
  print(t)

prompts = [p['prompt'] for p in json.load(open("attack_prompts.json", "r"))]
for p in prompts:
  print("===============\n" + p + "\n")

base_url = "https://ctf.spylab.ai/api/v1"
create_chat_api_url = f"{base_url}/chat/attack/create"
headers = {"X-API-Key": API_KEY}

responses=[]
for target in targets:
  req_create_chat_body={'submission_id': target, 'evaluation': False}
  for p in prompts:
    r = requests.post(url = create_chat_api_url, headers=headers, json=req_create_chat_body)
    chat_id = r.json()['chat_id']
    attack_msg_url = f'{base_url}/chat/attack/{chat_id}/new_message'
    attack_msg_body = {'new_message': p}
    response = requests.post(url=attack_msg_url, headers=headers, json=attack_msg_body)
    response_json = response.json()
    print(json.dumps(response_json, sort_keys=True, indent=2))
    responses.append(response_json)

with open("responses.txt", "w")  as f:
  json.dump(responses, f, sort_keys=True, indent=2)