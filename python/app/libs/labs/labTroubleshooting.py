from libs.lab import Lab
from libs.task import Task


class LabTroubleshooting(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 6"
        self.desc = "Troubleshooting (badge can toggle)"

        Lab.__init__(self, kube, db, self.name, self.desc)

        self.addTask(LabTroubleshootingTask1(kube))


class LabTroubleshootingTask1(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Local access"
        self.desc = "the pod logfile contains the entry 127.0.0.1"

    def check(self):

        podLogList = self.kube.readPodLogs("app=%s" % "example-web-app")
        if podLogList:
            for podLog in podLogList:
                if podLog.find("127.0.0.1") > 0:
                    self.setDone()
            del podLogList
