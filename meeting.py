#!/usr/bin/env python3

from company import Company
from employees import employees, emily

class Meeting:
  def __init__(self, goal, participants, secretary=emily):
    self.goal = goal
    self.participants = participants
    self.secretary = secretary

    self.pre_prompt = Company.story

    self.pre_prompt += "\n\nYou are in a meeting with the following participants:\n"
    for participant in self.participants:
      self.pre_prompt += f" - {participant.name} ({participant.role}): {participant.short_backstory}\n"
    self.pre_prompt += f"\n{self.secretary.name} is the secretary for this meeting."
    self.pre_prompt += f"\nThe goal for this meeting is: {self.goal}"
    self.pre_prompt += f"\nIf your name is called, it's your turn to speak. This is the current conversation:"

    self.conversation = self.pre_prompt + "\n\n"

  def run_step(self):
    for participant in self.participants:
      self.conversation = participant.run(self.conversation)
    # self.conversation = self.secretary.run(self.conversation)

if __name__ == "__main__":
  meeting = Meeting(
    goal="First monday meeting, all-hands. This is the first week of the company, we need to lay out a roadmap and come up with a plan for what everyone will be working on this sprint.",
    participants=employees,
  )

  for _ in range(3):
    meeting.run_step()

