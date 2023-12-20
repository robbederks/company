#!/usr/bin/env python3

from helpers import colored

from company import Company
from employees import employees, emily

class Meeting:
  def __init__(self, goal, participants, secretary=emily):
    self.goal = goal
    self.participants = participants
    self.secretary = secretary
    self.conversation = []

  def story(self):
    s = Company.story
    s += "\nYou are in a meeting with the following participants:\n"
    for participant in self.participants:
      s += f" - {participant.name} ({participant.role}): {participant.public_backstory}\n"
    s += f"\n{self.secretary.name} is the secretary for this meeting."
    s += f"\nThe goal for this meeting is: {self.goal} This is the current conversation:\n\n  "
    s += '\n  '.join(self.conversation) + '\n'
    return s

  def run(self):
    print(colored("Meeting goal: ", "cyan") + self.goal)

    for participant in self.participants:
      participant.run(meeting=self)

    print(colored("Meeting ended!", "cyan"))

if __name__ == "__main__":
  meeting = Meeting(
    goal="First monday meeting, all-hands. This is the first week of the company, we need to lay out a roadmap and come up with a plan for what everyone will be working on this sprint.",
    participants=employees,
  )
  meeting.run()

