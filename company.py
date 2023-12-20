#!/usr/bin/env python3

from typing import List

from meeting import Meeting
from about_us import employees, emily
from helpers import DEBUG, colored

class Company:
  def __init__(self) -> None:
    self.meetings: List[Meeting] = [
      Meeting(
        goal="First monday meeting, all-hands. This is the first week of the company, we need to lay out a roadmap and come up with a plan for what everyone will be working on this sprint.",
        participants=employees,
        secretary=emily,
      )
    ]

  def run(self):
    for m in self.meetings:
      m.run()

if __name__ == "__main__":
  Company().run()