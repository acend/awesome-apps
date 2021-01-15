import logging

from libs.lab import Lab
from libs.task import Task


class LabDatabase(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 7"
        self.desc = "Attaching a Database"

        Lab.__init__(self, kube, db, self.name, self.desc)

        self.addTask(LabDatabaseTask1(kube))
        self.addTask(LabDatabaseTask2(kube))
        self.addTask(LabDatabaseTask3(kube))


class LabDatabaseTask1(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Service"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readService("mariadb"):
            self.setDone()


class LabDatabaseTask2(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Deployment"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readDeployment("mariadb"):
            self.setDone()
        elif self.kube.readPodByLabel("deploymentconfig=mariadb"):
            logging.info("8.2 openshift case")
            self.setDone()


class LabDatabaseTask3(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Dump Import"
        self.desc = "Sample description"

    def check(self):
        try:
            if self.db.query.filter_by(name='Daniel').first():
                self.setDone()
        except Exception:
            pass
