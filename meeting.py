#!/usr/bin/env python3

from helpers import colored

from company import Company
from employees import employees, emily

class Meeting:
  def __init__(self, goal, participants, secretary=emily):
    self.goal = goal
    self.participants = participants
    self.secretary = secretary

    self.meeting_story = Company.story

    self.meeting_story += "\nYou are in a meeting with the following participants:\n"
    for participant in self.participants:
      self.meeting_story += f" - {participant.name} ({participant.role}): {participant.public_backstory}\n"
    self.meeting_story += f"\n{self.secretary.name} is the secretary for this meeting."
    self.meeting_story += f"\nThe goal for this meeting is: {self.goal}"
    self.meeting_story += f"\n\nIf your name is called, it's your turn to speak. This is the current conversation:"

    self.conversation = []

  def run(self):
    print(colored("Meeting goal: ", "cyan") + self.goal)

    for participant in self.participants:
      participant.run(self.meeting_story, self.conversation)

    print(colored("Meeting ended!", "cyan"))

if __name__ == "__main__":
  meeting = Meeting(
    goal="First monday meeting, all-hands. This is the first week of the company, we need to lay out a roadmap and come up with a plan for what everyone will be working on this sprint.",
    participants=employees,
  )
  meeting.run()

