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
  def _ask_binary(cls, agent, meeting, question) -> str:
    question += " Answer with one word, and that word only: YES or NO. If you're unsure, answer NO."
    return cls._ask(agent, meeting, question, answers=['YES', 'NO']) == "YES"

  @classmethod
  def follow_up(cls, agent, meeting) -> None: pass

  @classmethod
  def run(cls, agent, meeting) -> None:
    if cls._ask_binary(agent, meeting, cls.binary_prompt):
      cls.follow_up(agent, meeting)

class Speak(_Action):
  binary_prompt="Based on this transcript, do you want to say something constructive?"

  @classmethod
  def follow_up(cls, agent, meeting):
    output = cls._ask(agent, meeting, f"What do you want to say? Be concise.\n\n{agent.name}: ")
    print(colored(f"{agent.name} ({agent.role}) SPEAKS: ", "green") + colored(output, "red"))
    meeting.transcript.append(f"{agent.name} SPEAKS: {output}")

class EndMeeting(_Action):
  binary_prompt="Have all goals for the meeting been resolved, meaning that the meeting can be ended?"

  @classmethod
  def follow_up(cls, agent, meeting):
    meeting.summary = cls._ask(agent, meeting, "Summarize the most important facts from this meeting. Be as concise as possible.")
    meeting.finished = True

class ScheduleMeeting(_Action):
  binary_prompt="Are there any questions / concerns that have been brought up that are out-of-scope for this meeting?"

  @classmethod
  def follow_up(cls, agent, meeting) -> None:
    meeting_goal = cls._ask(agent, meeting, "Generate a concise meeting goal to address any question / concern that has been brought up.")
    # TODO: figure out who to include in the meeting participants
    # TODO: is this meeting already planned?
    print(colored(f"{agent.name} ({agent.role}) SCHEDULES MEETING: ", "green") + meeting_goal)
    meeting.transcript.append(f"{agent.name} SCHEDULES MEETING: {meeting_goal}")

    from meeting import Meeting
    meeting.company.meetings.append(
      Meeting(
        goal=meeting_goal,
        participants=meeting.participants,
        secretary=meeting.secretary,
        company=meeting.company
      )
    )

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
