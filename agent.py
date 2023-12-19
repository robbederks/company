#!/usr/bin/env python3

import together
from secret import API_KEY
together.api_key = API_KEY

from company import Company
from helpers import colored, DEBUG

class Agent:
  def __init__(self, name, backstory, role, actions=None, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    self.name = name
    self.backstory = backstory
    # TODO: make better
    self.short_backstory = backstory.replace('\n', ' ')
    self.actions = actions
    self.role = role
    self.model = model

    self.pre_prompt = f"[INST] You are {self.name}, an employee at {Company.name} with the role of {self.role}. Your backstory is:\n  {self.backstory}"

    if self.actions is not None:
      self.pre_prompt += f"\nYou have the following special actions available:\n - " + '\n - '.join(self.actions) + "\n"

  def run(self, conversation):
    conversation += f"\n{self.name}: [/INST]"

    prompt = self.pre_prompt + conversation
    if DEBUG:
      print(colored(f"\n\nDEBUG: {self.name} Prompt:", "yellow"))
      print(colored(prompt, "yellow"))

    print(colored(f"\n{self.name}: ", "green"), end="")
    ret = together.Complete.create(
      prompt=prompt,
      model=self.model,
      max_tokens=200,
      temperature=0.7,
      repetition_penalty=1.2,
      stop=["\n", "[INST]"],
    )
    output = ret['output']['choices'][0]['text'].strip()
    print(colored(output, "red"), end="")
    conversation += output
    return conversation.replace("[/INST]", "")
