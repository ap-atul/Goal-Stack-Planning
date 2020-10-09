# Goal Stack Planning
GSP is combination of both the Backward chaining and Forward chaining. GSP considers actions by reasoning in the
backward manner, but commits itself to actions only in the forward manner.It pushes sub goals onto the stack, and 
picks up action only if the preconditions are satisfied

## Algorithm
```console

while stack is not empty:
    if top of stack is predicate:
        if predicate is true:
            pop it
  
    else:
        pop it
        push corresponding action that will satisfy that predicate onto stack
        push preconditions of that action

    if top of stack is action:
        pop it
        perform the action i.e add and delete it's effects from current state.
        add that action to the actual plan
 
```

## Example
Consider below stacks

```

-----                   -----  -----
| B |                   | C |  | B |
-----  -----  -----     -----  -----
| A |  | C |  | D |     | A |  | D |
-----  -----  -----     -----  -----
___________________     ____________
	   Start                Goal     


Plan :: 

stack B D
unstack B A
stack C A

-----------------------------------------------
                  
                  -----
                  | A |
-----             -----
| C |             | B |
-----  -----      -----
| A |  | B |      | C |
-----  -----      ----- 
____________      ______
   Start           Goal


Plan:

unstack C A
putdown C
stack B C
stack A B

```