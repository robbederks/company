#!/usr/bin/env python3

from random import randint
from helpers import LOCAL, DEBUG, colored

import together
from secret import API_KEY
together.api_key = API_KEY

def run_llm(prompt, answers=None, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
  prompt = "[INST]" + prompt + "[/INST]"

  if DEBUG >= 2: print(colored(f"Prompt: ", "yellow") + colored(prompt, "black"))

  if LOCAL:
    if answers is not None:
      ret = answers[randint(0, len(answers) - 1)]
    else:
      ret = "Hmm, I don't know without internet..."
  else:
    good_reply = False
    for _ in range(5):
      out = together.Complete.create(
        prompt=prompt,
        model=model,
        max_tokens=200,
        temperature=0.7,
        repetition_penalty=1.2,
        stop=["\n", "[INST]"] + answers if answers is not None else [],
      )
      ret = out['output']['choices'][0]['text'].strip()

      if answers is None or ret.lower() in [a.lower() for a in answers]:
        good_reply = True
        break
      if DEBUG >= 2: print(colored(f"Returned '{ret}', which is not a possible answer. Retrying...", "red"))
    assert good_reply, "Didn't get one of the expected answers"

  if DEBUG >= 2: print(colored(f"Reply: ", "yellow") + colored(ret, "black"))
  return ret

