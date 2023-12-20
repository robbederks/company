#!/usr/bin/env python3

from dataclasses import dataclass

from llm import run_llm
from helpers import colored
from company import Company

@dataclass
class Action:
  name: str
  binary_prompt: str

  def prompt(self):
    output = run_llm(f"{self.binary_prompt} Answer with one word: YES or NO")

  def follow_up(self):
    pass

class Speak(Action):
  name = "SPEAK"
  binary_prompt = "Based on this conversation, do you want to say something constructive?"

  def follow_up(self):
    pass


class Agent:
  def __init__(self, name, public_backstory, private_backstory, role, actions=None):
    self.name = name
    assert '\n' not in public_backstory, "The public backstory needs to be concise, and a single line"
    self.public_backstory = public_backstory
    self.private_backstory = private_backstory
    self.actions = actions
    self.role = role

    self.pre_prompt = f"You are {self.name}, an employee at {Company.name} with the role of {self.role}. Your backstory is:\n  {self.public_backstory}\n"
    self.pre_prompt += f"Other facts about you are:{self.private_backstory}"

    if self.actions is not None:
      self.pre_prompt += f"\nYou have the following special actions available:\n - " + '\n - '.join(self.actions) + "\n"

  def run(self, meeting_description, conversation):
    output = run_llm(self.pre_prompt + '\n' + meeting_description + '\n' + '\n'.join(conversation) + f"\n{self.name}: ")
    print(colored(f"{self.name}: ", "green") + colored(output, "red"))
    conversation.append(f"{self.name}: {output}")
