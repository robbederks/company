#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Optional

from llm import run_llm
from helpers import colored, DEBUG

@dataclass
class _Action:
  binary_prompt: str

  @classmethod
  def _ask(cls, agent, meeting, question, answers=None) -> str:
    if DEBUG == 1: print(colored(f"Question for {agent.name}: ", "yellow") + colored(question, "black"), end=" ")
    ret = run_llm(f"{agent.pre_prompt}{meeting.story()}\n{question}", answers=answers)
    if DEBUG == 1: print(colored(ret, "cyan"))
    return ret

  @classmethod
  def follow_up(cls, agent, meeting) -> None: pass

  @classmethod
  def run(cls, agent, meeting) -> None:
    output = cls._ask(agent, meeting, f"{cls.binary_prompt} Answer with one word: YES or NO", answers=['YES', 'NO'])
    if output.lower() == "yes":
      cls.follow_up(agent, meeting)

class Speak(_Action):
  binary_prompt="Based on this conversation, do you want to say something constructive?"

  @classmethod
  def follow_up(cls, agent, meeting):
    output = cls._ask(agent, meeting, "What do you want to say? Be concise.")
    print(colored(f"{agent.name} ({agent.role}) SPEAKS: ", "green") + colored(output, "red"))
    meeting.conversation.append(f"{agent.name}: {output}")

class EndMeeting(_Action):
  binary_prompt="Have all goals for the meeting been resolved, meaning that the meeting can be ended?"

  @classmethod
  def follow_up(cls, agent, meeting):
    meeting.summary = cls._ask(agent, meeting, "Summarize the most important facts from this meeting. Be as concise as possible.")
    meeting.finished = True

@dataclass
class Agent:
  name: str
  role: str
  company_name: str
  public_backstory: str
  private_backstory: str
  actions: List[_Action]

  def __post_init__(self) -> None:
    assert '\n' not in self.public_backstory, "The public backstory needs to be concise, and a single line"

    self.pre_prompt = f"You are {self.name}, an employee at {self.company_name} with the role of {self.role}. Your backstory is:\n  {self.public_backstory}\n"
    self.pre_prompt += f"Other facts about you are:{self.private_backstory}"

  def run(self, meeting):
    for action in self.actions:
      action.run(self, meeting)
    if DEBUG == 1: print()
