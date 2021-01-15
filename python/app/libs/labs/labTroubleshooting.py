from libs.lab import Lab
from libs.task import Task


class LabTroubleshooting(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 7"
        self.desc = "Troubleshooting (badge can toggle)"

        super().__init__(kube, db, self.name, self.desc)

        self.addTask(Task1(kube))


class Task1(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "Local access"
        self.desc = "Sample description"

    def check(self):

        podLogList = self.kube.readPodLogs("app=%s" % "example-web-python")
        if podLogList:
            for podLog in podLogList:
                if podLog.find("127.0.0.1") > 0:
                    self.setDone()
            del podLogList
