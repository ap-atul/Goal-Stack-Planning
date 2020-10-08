"""
Goal Stack Planning
"""

from lib.logger import Log


class Action:
    """
    Actions that can be taken on the blocks
    """
    STACK = "stack"
    UNSTACK = "unstack"
    PICKUP = "pickup"
    PUTDOWN = "putdown"
    SPACE = " "

    @staticmethod
    def getActions():
        """
        Returns the list of all actions

        Returns
        -------
        list
            list of all the actions
        """
        return [Action.STACK,
                Action.UNSTACK,
                Action.PICKUP,
                Action.PUTDOWN]


class Predicate:
    """
    Different predicates to denote the action to take

    Actions associated with the predicates

        1. ON : stack(a,b), clear(a)
        2. ON_TABLE : put down(a), hold(a)
        3. CLEAR : put down(a), hold(a) ; unstack(a, b), on(a), clear(a)
        4. HOLD: pickup(a), on_table(a), arm_empty; unstack(a, b), on(a), clear(a)
        5. ARM_EMPTY : putdown(a), hold(a)

    """
    ON = "on"
    CLEAR = "clear"
    ARM_EMPTY = "arm_empty"
    HOLDING = "holding"
    ON_TABLE = "on_table"
    SPACE = " "

    @staticmethod
    def getPredicates():
        """
        Returns all the predicates for taking actions

        Returns
        -------
        list
            all predicates
        """
        return [Predicate.ON,
                Predicate.CLEAR,
                Predicate.ARM_EMPTY,
                Predicate.HOLDING,
                Predicate.ON_TABLE]


class Planner:
    """
    Goal Stacking Planning implementation using Predicates and Actions to decide the action
    to be taken on certain predicate and create plan accordingly

    Attributes
    -----------
    __actions: list
        list of all the actions
    __predicates: list
        list of all the predicates
    __goalState: list
        the goal state to achieve
    __startState: list
        input state to start from
    __currentStack: list
        copy of the start state to update and plan
    __planningStack: list
        planner stack having the actions and predicates
    __plan: list
        final plan
    __sep: str
        separtor
    __verbose: bool
        true to print the planning stack
    """
    def __init__(self, verbose=False):
        self.__actions = Action.getActions()
        self.__predicates = Predicate.getPredicates()
        self.__goalState = list()
        self.__startState = list()
        self.__currentStack = list()
        self.__planningStack = list()
        self.__plan = list()
        self.__sep = "^"
        self.__verbose = verbose

    def __preconditionsStack(self, x, y):
        """
        Precondition to stack two values

        Parameters
        ----------
        x : str
            block 1
        y : str
            block 2
        """
        self.__planningStack.append(''.join([Predicate.CLEAR, Predicate.SPACE, str(y)]))

    def __preconditionsUnStack(self, x, y):
        """
        Precondition to unstack two values

        Parameters
        ----------
        x : str
            block 1
        y : str
            block 2
        """
        self.__planningStack.append(''.join([Predicate.ON, Predicate.SPACE, str(x), Predicate.SPACE, str(y)]))
        self.__planningStack.append(''.join([Predicate.CLEAR, Predicate.SPACE, str(x)]))

    def __preconditionsPickUp(self, x):
        """
        Precondition to pick up a value

        Parameters
        ----------
        x : str
            block 1
        """
        self.__planningStack.append(''.join([Predicate.ARM_EMPTY]))
        self.__planningStack.append(''.join([Predicate.ON_TABLE, Predicate.SPACE, str(x)]))

    def __preconditionsPutDown(self, x):
        """
        Precondition to put down a value

        Parameters
        ----------
        x : str
            block 1
        """
        self.__planningStack.append(''.join([Predicate.HOLDING, Predicate.SPACE, str(x)]))

    def __actionOn(self, x, y):
        """
        Action taken when two blocks are on each other

        Parameters
        ----------
        x : str
            block 1
        y : str
            block 2
        """
        self.__planningStack.append(''.join([Action.STACK, Action.SPACE, str(x), Action.SPACE, str(y)]))
        self.__preconditionsStack(x, y)

    def __actionOnTable(self, x):
        """
        Action taken when a block is on the table

        Parameters
        ----------
        x : str
            block 1
        """
        self.__planningStack.append(''.join([Action.PUTDOWN, Action.SPACE, str(x)]))
        self.__preconditionsPutDown(x)

    def __actionClear(self, x):
        """
        Action taken when a block is on some other block and
        has no other block on the top

        Parameters
        ----------
        x : str
            block 1
        """
        check = ''.join([Predicate.ON_TABLE, Predicate.SPACE, str(x)])

        if check in self.__currentStack:
            self.__planningStack.append(''.join([Action.PUTDOWN, Action.SPACE, str(x)]))
            self.__preconditionsPutDown(x)
            return

        check = ''.join([Predicate.ON, Predicate.SPACE])
        temp = list()

        for predicate in self.__currentStack:
            if check in predicate:
                temp = predicate.split()

                if temp[2] == x:
                    break

        y = str(temp[1])
        self.__planningStack.append(''.join([Action.UNSTACK, Action.SPACE, str(y), Action.SPACE, str(x)]))
        self.__preconditionsUnStack(y, x)

    def __actionHolding(self, x):
        """
        Action taken when a block is on the arm

        Parameters
        ----------
        x : str
            block 1
        """
        check = ''.join([Predicate.ON_TABLE, Predicate.SPACE, str(x)])

        if check in self.__currentStack:
            self.__planningStack.append(''.join([Action.PICKUP, Action.SPACE, str(x)]))
            self.__preconditionsPickUp(x)
            return

        check = ''.join([Predicate.ON, Predicate.SPACE])
        temp = list()

        for predicate in self.__currentStack:
            if check in predicate:
                temp = predicate.split()

                if temp[1] == x:
                    break
            else:
                return

        y = str(temp[2])
        self.__planningStack.append(''.join([Action.UNSTACK, Action.SPACE, str(y), Action.SPACE, str(x)]))
        self.__preconditionsUnStack(y, x)

    def __actionArmEmpty(self):
        """
        Action taken when arm is empty
        """
        Log.d(f"Arm is empty :: {self.__planningStack}")
        exit(1)

    def __effectStack(self, x, y):
        """
        Post action effect after stacking

        Parameters
        ----------
        x : str
            block 1
        y : str
            block 2
        """
        self.__currentStack.remove(''.join([Predicate.CLEAR, Predicate.SPACE, str(y)]))

        self.__currentStack.append(''.join([Predicate.ON, Predicate.SPACE, str(x), Predicate.SPACE, str(y)]))
        self.__currentStack.append(''.join([Predicate.CLEAR, Predicate.SPACE, str(x)]))
        self.__currentStack.append(Predicate.ARM_EMPTY)

    def __effectUnStack(self, x, y):
        """
        Post action effect after unstacking

        Parameters
        ----------
        x : str
            block 1
        y : str
            block 2
        """
        self.__currentStack.remove(''.join([Predicate.ON, Predicate.SPACE, str(x), Predicate.SPACE, str(y)]))
        self.__currentStack.remove(''.join([Predicate.CLEAR, Predicate.SPACE, str(x)]))
        self.__currentStack.remove(Predicate.ARM_EMPTY)

        self.__currentStack.append(''.join([Predicate.HOLDING, Predicate.SPACE, str(x)]))
        self.__currentStack.append(''.join([Predicate.CLEAR, Predicate.SPACE, str(y)]))

    def __effectPickUp(self, x):
        """
        Post action effect after picking up

        Parameters
        ----------
        x : str
            block 1
        """
        self.__currentStack.remove(Predicate.ARM_EMPTY)
        self.__currentStack.remove(''.join([Predicate.ON_TABLE, Predicate.SPACE, str(x)]))

        self.__currentStack.append(''.join([Predicate.HOLDING, Predicate.SPACE, str(x)]))

    def __effectPutDown(self, x):
        """
        Post action effect after putting down

        Parameters
        ----------
        x : str
            block 1
        """
        # self.__currentStack.remove(''.join([Predicate.HOLDING, Predicate.SPACE, str(x)]))

        self.__currentStack.append(Predicate.ARM_EMPTY)
        self.__currentStack.append(''.join([Predicate.ON_TABLE, Predicate.SPACE, str(x)]))
        self.__currentStack.append(''.join([Predicate.CLEAR, Predicate.SPACE, str(x)]))

    def getPlan(self, startState: str, goalState: str):
        """
        Run the Goal Stack Planner and creates the final plan to achieve the Goal State

        Parameters
        ----------
        startState : str
            starting state
        goalState : str
            goal state to achieve

        Returns
        -------
        list
            list of actions to be taken to achieve the goal state
        """
        self.__startState = startState.split(self.__sep)
        self.__goalState = goalState.split(self.__sep)
        self.__currentStack = self.__startState.copy()

        # creating the plan stack
        for predicate in self.__goalState:
            self.__planningStack.append(predicate)

        # running for the stack empty
        while len(self.__planningStack) > 0:
            if self.__verbose:
                Log.d(f"Planning Stack :: {self.__planningStack}")
                Log.d(f"Current Stack :: {self.__currentStack}")

            top = self.__planningStack.pop()
            temp = top.split()

            if temp[0] in self.__predicates:
                if top in self.__currentStack:
                    continue

                else:
                    # if it is a predicate
                    if temp[0] == Predicate.ON:
                        self.__actionOn(temp[1], temp[2])

                    elif temp[0] == Predicate.ON_TABLE:
                        self.__actionOnTable(temp[1])

                    elif temp[0] == Predicate.CLEAR:
                        self.__actionClear(temp[1])

                    elif temp[0] == Predicate.HOLDING:
                        self.__actionHolding(temp[1])

                    elif temp[0] == Predicate.ARM_EMPTY:
                        self.__actionArmEmpty()

            if temp[0] in self.__actions:
                # if it is an action
                if temp[0] == Action.STACK:
                    self.__effectStack(temp[1], temp[2])

                elif temp[0] == Action.UNSTACK:
                    self.__effectUnStack(temp[1], temp[2])

                elif temp[0] == Action.PICKUP:
                    self.__effectPickUp(temp[1])

                elif temp[0] == Action.PUTDOWN:
                    self.__effectPutDown(temp[1])

                # add processed action
                self.__plan.append(top)

        if self.__verbose:
            Log.d(f"Final stack :: {self.__currentStack}")

        return self.__plan
