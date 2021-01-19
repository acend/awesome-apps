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
        self.addTask(LabDatabaseTask3(kube, db))


class LabDatabaseTask1(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Service"
        self.desc = "service mariadb exists"

    def check(self):
        if self.kube.readService("mariadb"):
            self.setDone()


class LabDatabaseTask2(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Deployment"
        self.desc = "deployment mariadb exist"

    def check(self):
        if self.kube.readDeployment("mariadb"):
            self.setDone()
        elif self.kube.readPodByLabel("deploymentconfig=mariadb"):
            logging.info("8.2 openshift case")
            self.setDone()


class LabDatabaseTask3(Task):

    def __init__(self, kube, db):
        Task.__init__(self, kube, db)

        self.name = "Dump Import"
        self.desc = "db contains an specific entry"

    def check(self):
        try:
            if self.db.query.filter_by(name='Daniel').first():
                self.setDone()
        except Exception as x:
            logging.error("DB issue: %s" % x)
