import logging

from libs.lab import Lab
from libs.task import Task


class LabDatabase(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 8"
        self.desc = "Database"

        super().__init__(kube, db, self.name, self.desc)

        self.addTask(Task1(kube))
        self.addTask(Task2(kube))
        self.addTask(Task3(kube))


class Task1(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "Service"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readService("mariadb"):
            self.setDone()


class Task2(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "Deployment"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readDeployment("mariadb"):
            self.setDone()
        elif self.kube.readPodByLabel("deploymentconfig=mariadb"):
            logging.info("8.2 openshift case")
            self.setDone()


class Task3(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "Dump Import"
        self.desc = "Sample description"

    def check(self):
        try:
            if self.db.query.filter_by(name='Daniel').first():
                self.setDone()
        except Exception:
            pass
