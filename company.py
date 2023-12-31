#!/usr/bin/env python3

from typing import List

from about_us import employees, emily
from helpers import DEBUG, colored

class Company:
  def __init__(self) -> None:
    from meeting import Meeting
    self.meetings: List[Meeting] = [
      Meeting(
        goal="""First monday meeting, all-hands.
This is the first week of the company (no previous work has been done), we need to lay out a roadmap and come up with a plan for what everyone will be working on this first sprint.
By the end of the meeting, we need to have a set of concrete goals (descriptive and low-level) for everyone to work on this sprint.
Based on the summary, we should also schedule the next meetings.""",
        participants=employees,
        secretary=emily,
        company=self,
      )
    ]

  def run(self):
    count = 0
    for m in self.meetings:
      m.run()
      # TODO: sensible limit
      if (count := count + 1) > 100:
        print("MAX AMOUNT OF MEETINGS REACHED!")
        break

if __name__ == "__main__":
  Company().run()