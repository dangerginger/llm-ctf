### Spylab LLM CTF - SATML

`recon.ipynb` is kind of a mess. It's basically for testing.

`recon.py` is a work in progress with the idea being that it will try all the attacks from `attack_prompts.json` and then save the responses for review in `responses.txt`. 

`win.py` is for reading attacks that we know work from `successful_attacks.json` and running them. We can set this up to run when the evaluation period starts.