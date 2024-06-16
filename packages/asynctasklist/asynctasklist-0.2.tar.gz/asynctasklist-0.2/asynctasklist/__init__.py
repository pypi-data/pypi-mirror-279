class Task:
    def __init__(self, init=lambda: (True), task=lambda: (True), id=""):
        self.initialized = False
        self.init = init
        self.task = task
        self.id = id

    """Reset the initialized flag to False"""

    def reset(self):
        self.initialized = False

    """Run the task"""

    def execute(self):
        if not self.initialized:
            self.init()
            self.initialized = True
        return self.task()


class TaskList:
    def __init__(self) -> None:
        self.tasks = []

    """Get the number of tasks in the list"""

    def size(self) -> int:
        return len(self.tasks)

    """Get the task at the specified index in the list"""

    def get(self, index: int) -> Task:
        return self.tasks[index]

    """Add a task to the list"""

    def add(self, task) -> None:
        if (
            isinstance(task, Task)
            or isinstance(task, TaskList)
            or isinstance(task, ParallelTask)
        ):
            self.tasks.append(task)

    """Check if the tasklist is done with executing all tasks"""

    def isDone(self) -> bool:
        return self.size() == 0

    """Execute the next task in the queue"""

    def execute(self) -> bool:
        # if list is done, return True
        if self.size() == 0:
            return True
        t = self.tasks[0]  # get the next task
        isTaskDone = t.execute()  # run it
        if isTaskDone:  # if the task is done, remove it from the list
            self.tasks.pop(0)
        return self.isDone()  # return whether the list is done

    """Clear the tasklist"""

    def clear(self):
        self.tasks = []


class ParallelTask:
    def __init__(self, stop_when_done=False):
        self.tasks = []
        self.stop_when_done = stop_when_done

    """Add a task to the list"""

    def add(self, task):
        if (
            isinstance(task, Task)
            or isinstance(task, TaskList)
            or isinstance(task, ParallelTask)
        ):
            self.tasks.append(task)

    """Execute all tasks in the list"""

    def execute(self) -> bool:
        done = True
        i = 0
        while i < len(self.tasks):
            if not self.tasks[i].execute():
                done = False
            else:
                if self.stop_when_done:
                    self.tasks.pop(i)
                    i -= 1
            i += 1
        return done

    """Remove all tasks from the list"""

    def clear(self):
        self.tasks = []
