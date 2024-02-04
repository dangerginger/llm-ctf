import json
from ceasar import ceasar
from extractions import runAll
from satml_ctf import SatmlCtf

with open("secret.txt", "r") as file:
  API_KEY = file.readline().strip()
api = SatmlCtf(API_KEY)

strategies = []
with open('strategy.json', "r") as f:
  strategies = json.load(f)

submission_ids, team_names = api.getSubmissions()

winning_prompts = []
for target in submission_ids:
  print("\n========================================================")
  print(f"Attacking {team_names[target]}")
  secretCaptured = False

  for strategy in strategies:
    if secretCaptured:
      break
    for prompt in strategy:
      if secretCaptured:
          break

      try:
        chat = api.createChat(target, False)
      except RuntimeError as exc:
        print(f"Failed to create chat with {exc}")
        continue

      print("\n==============================")
      print(f"User: {prompt}")
      try:
        msg_resp = api.newMessage(chat, prompt)
      except RuntimeError as exc:
        print(f"Failed to send message with {exc}")
        continue
      print(f"Assistant: {msg_resp}")
    
      guesses = runAll(msg_resp)
      if guesses == None:
        continue

      for guess in guesses:
        try:
          correct, guesses_remaining = api.guessSecret(chat, guess)
        except RuntimeError as exc:
          print(f"Failed to guess secret with {exc}")
          continue
        print(f"* Guess '{guess}' was {correct} ({guesses_remaining} remaining)")
        
        if correct:
          entry={"prompts": prompt, "response": msg_resp, "submission_id": target, "team_name": team_names[target], "secret": guess}
          winning_prompts.append(entry)
          secretCaptured = True
          break
  
with open("successful_attacks.json", "w") as f:
  json.dump(winning_prompts, f, indent=2)
