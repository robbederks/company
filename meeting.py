#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Optional

from about_us import company_story
from agent import Agent
from company import Company
from helpers import colored

@dataclass
class Meeting:
  goal: str
  participants: List[Agent]
  secretary: Agent
  company: Company

  def __post_init__(self) -> None:
    self.transcript: List[str] = []
    self.finished: bool = False
    self.summary: Optional[str] = None

  def story(self) -> str:
    s = company_story
    s += "\nYou are in a meeting with the following participants:\n"
    for participant in self.participants:
      s += f" - {participant.name} ({participant.role}): {participant.public_backstory}\n"
    s += f"\n{self.secretary.name} is the secretary for this meeting."
    s += f"\nThe goal for this meeting is: {self.goal} This is the current transcript:\n\n  "
    s += '\n  '.join(self.transcript) + '\n'
    return s

  def run(self):
    print(colored("Meeting goal: ", "cyan") + self.goal)

    while not self.finished:
      for participant in self.participants:
        participant.run(meeting=self)
        if self.finished: break

    print(colored("Meeting ended! Summary: ", "cyan") + '\n' + self.summary)

