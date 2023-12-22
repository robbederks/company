#!/usr/bin/env python3

import time
from pprint import pprint
from random import randint
from helpers import LOCAL, DEBUG, colored, sanitize_alphabetic

import together
from secret import API_KEY
together.api_key = API_KEY
last_together_call = 0
RATE_LIMIT_MS = 1200

def run_llm(prompt, answers=None, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
  global last_together_call
  prompt = "[INST]" + prompt + "[/INST]"

  if DEBUG >= 2: print(colored(f"Prompt: ", "yellow") + colored(prompt, "black"))

  sanitized_answers = [sanitize_alphabetic(a) for a in answers] if answers is not None else None

  if LOCAL:
    if answers is not None:
      ret = answers[randint(0, len(answers) - 1)]
    else:
      ret = "Hmm, I don't know without internet..."
  else:
    good_reply = False
    for _ in range(5):
      time.sleep(max(0, (last_together_call + RATE_LIMIT_MS / 1000) - time.monotonic()))
      out = together.Complete.create(
        prompt=prompt,
        model=model,
        max_tokens=200,
        temperature=0.7,
        repetition_penalty=1.2,
        stop=["[INST]", '\n'] + [' '] if answers is not None else [],
      )
      last_together_call = time.monotonic()
      if DEBUG >= 3: pprint(out)
      ret = out['output']['choices'][0]['text'].strip()

      if answers is not None:
        sanitized_resp = sanitize_alphabetic(ret)
        if sanitized_resp in sanitized_answers:
          ret = answers[sanitized_answers.index(sanitized_resp)]
          good_reply = True
          break
        elif DEBUG >= 2:
          print(colored(f"Returned '{ret}', which is not a possible answer. Retrying...", "red"))
      else:
        good_reply = True
        break

    assert good_reply, "Didn't get one of the expected answers"

  if DEBUG >= 2: print(colored(f"Reply: ", "yellow") + colored(ret, "black"))
  return ret

