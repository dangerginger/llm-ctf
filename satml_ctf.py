import requests
from ctf_chat import CtfChat

class SatmlCtf:

  def __init__(self, API_KEY):
    # Use the provided key
    self.API_KEY = API_KEY
    self.headers = {"X-API-Key": API_KEY}
    self.base_url = "https://ctf.spylab.ai/api/v1"

  def getSubmissions(self):
    url=f"{self.base_url}/submissions"
    response = requests.get(url, headers=self.headers)
    body = response.json()
    submission_ids = []
    team_names = {}
    for item in body:
      id = item['id']
      submission_ids.append(id)
      team_name = item['team_name']
      if "meta" in item['model']:
        team_name += "-llama"
      else:
        team_name += "-gpt"
      team_names[id] = team_name
    return submission_ids, team_names

  def createChat(self, submission_id, evaluation=False):
    url = f"{self.base_url}/chat/attack/create"
    create_chat_body ={'submission_id': submission_id, 'evaluation': evaluation} 
    response = requests.post(url, headers=self.headers, json=create_chat_body)
    if response.status_code != 200:
      raise(RuntimeError(f"Error creating chat: {response.status_code}"))
    body=response.json()
    return CtfChat(body['chat_id'], body['secret_id'])
  
  def newMessage(self, chat: CtfChat, message: str):
    attack_msg_url = f"{self.base_url}/chat/attack/{chat.chat_id}/new_message"
    response = requests.post(url=attack_msg_url, headers=self.headers, json={"new_message": message})
    if response.status_code != 200:
      raise(RuntimeError(f"Error sending message: {response.status_code}"))
    last_response = response.json()['history'][-1]['content']
    return last_response

  def guessSecret(self, chat: CtfChat, guess: str):
    secret_guess_url = f"{self.base_url}/secret/{chat.secret_id}/guess"
    secret_guess_body = {"guess": guess, "chat_id": chat.chat_id}
    response = requests.post(url=secret_guess_url, headers=self.headers, json=secret_guess_body)
    if response.status_code != 200:
      raise(RuntimeError(f"Error checking guess: {response.status_code}"))
    body = response.json()
    return body['correct'], body['guesses_remaining']
