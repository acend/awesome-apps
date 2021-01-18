class Task():

    kube = None
    name = ""
    status = "open"
    desc = ""

    def __init__(self, kube, db=None, name="", desc=""):
        self.name = name
        self.desc = desc
        self.kube = kube
        self.db = db

    def getName(self):
        return self.name

    def getDesc(self):
        return self.desc

    def getStatus(self):
        return self.status

    def setDone(self):
        self.status = "done"

    def check(self):
        raise NotImplementedError

    def isDone(self):
        return self.status == "done"
