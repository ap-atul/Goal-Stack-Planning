from lib.logger import Log
from lib.planner import Planner

startState = input("Enter the start state :: ")
goalState = input("Enter the goal state :: ")
print()

planner = Planner(verbose=False)
plan = planner.getPlan(startState=startState, goalState=goalState)
Log.e(f"Final plane derived ::")
for p in plan:
    Log.i(p)
