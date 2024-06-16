class Task:
    def __init__(self, init=lambda:(True), task=lambda:(True), id=""):
        self.initialized = False
        self.init = init
        self.task = task
        self.id = id

    def reset(self):
        self.initialized = False

    def execute(self):
        if not self.initialized:
            self.init()
            self.initialized = True
        return self.task()


class TaskList:
    def __init__(self, *tasks):
        self.tasks = list(tasks)

    def size(self):
        return len(self.tasks)

    def get(self, index):
        return self.tasks[index]

    def add(self, task):
        self.tasks.append(task)

    def isDone(self):
        return self.size() == 0

    def execute(self):
        if self.size() == 0:
            return True
        t = self.tasks[0]
        isTaskDone = t.execute()
        if isTaskDone:
            self.tasks.pop(0)
        return self.isDone()

    def clear(self):
        self.tasks = []


class ParallelTask(Task):
    def __init__(self, stop_when_done, *tasks):
        self.list = list(tasks)
        self.stop_when_done = stop_when_done

    def execute(self):
        done = True
        i = 0
        while i < len(self.list):
            if not self.list[i].execute():
                done = False
            else:
                if self.stop_when_done:
                    self.list.pop(i)
                    i -= 1
            i += 1
        return done

    def clear(self):
        self.list = []

