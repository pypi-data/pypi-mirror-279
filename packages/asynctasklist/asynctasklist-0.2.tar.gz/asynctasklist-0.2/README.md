<!--

steps to build:

 - increment build number
 - run `python3 -m pip wheel ./`

-->

# asynctasklist

[![PyPI](https://img.shields.io/pypi/v/asynctasklist.svg)](https://pypi.org/project/asynctasklist/)
[![Tests](https://github.com/moojor224/asynctasklist/actions/workflows/test.yml/badge.svg)](https://github.com/moojor224/asynctasklist/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/moojor224/asynctasklist?include_prereleases&label=changelog)](https://github.com/moojor224/asynctasklist/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/moojor224/asynctasklist/blob/main/LICENSE)

a simple tasklist library for running tasks pseudo-asynchronously
 - note: 

## Installation

<!-- Install this library using `pip`:
```bash
pip install asynctasklist
``` -->


## Basic TaskList Usage


```python
from asynctasklist import TaskList, Task
import time

# initialize the tasklist variable
tasks = TaskList()

# template function to return a new instance of a function
def makeTask(timeout, callback):
    startTime = 0 # initialize startTime variable

    def init():
        nonlocal startTime
        startTime = round(time.time() * 1000) # set the start time to the time when this task is first run

    def task():
        if round(time.time() * 1000) - startTime >= timeout: # check if timeout duration has passed
            callback() # run some code
            return True # return True since to task is done
        return False # return False since to task is not done
    return Task(init=init, task=task) # return a new task

# define callback function
def run():
    print("timeout is done")
    pass

# add a new task to the list
tasks.add(makeTask(1000, run)) # print message after 1 second
tasks.add(makeTask(2000, run)) # print message 2 seconds after the first message


# if you want to run the tasklist truly asynchronously, run a new thread before the main program loop
import threading
def task_worker():
    while True:
        tasks.execute()

t = threading.Thread(target=task_worker, daemon=True) # set daemon to true to stop thread when program ends
t.start()

# if you want to run the tasklist alongside your main program, simply put `task.execute()` in the main program loop
# main program loop
while True:
    # run main app code
    app.run() # example code
    # update gui
    gui.update() # example code

    # run the tasklist
    tasks.execute()
    if tasks.isDone():
        print("all tasks are done")
        break
    pass

```

 - notes:
   - lambdas can be used in place of functions for inline task initialization
 - ParallelTasks function the same as TaskLists, but instead of running the task one at a time in the order they were added, it runs all tasks at the same time.
   - it is recommended to have a check at the beginning of each task in a ParallelTask to make sure work needs to be done before running the task in case some tasks take longer to finish than the others

## Development

To contribute to this library, clone the ropository, make changes, then submit a pull request
<!-- ```bash
cd asynctasklist
python -m venv venv
source venv/bin/activate
``` -->
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
