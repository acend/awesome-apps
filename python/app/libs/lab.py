class Lab():

    kube = None
    db = None
    name = ""
    desc = ""
    tasks = list()

    def __init__(self, kube, db, name, desc):
        self.kube = kube
        self.db = db
        self.name = name
        self.desc = desc
        self.tasks = list()

    def addTask(self, task):

        self.tasks.append(task)

    def getName(self):
        return self.name

    def getDesc(self):
        return self.desc

    def check(self):
        for task in self.tasks:
            task.check()

    def getStatus(self):
        return [task for task in self.tasks]

    def countTasks(self):
        return len(self.tasks)

    def countDone(self):
        return len([task for task in self.tasks if task.isDone()])
