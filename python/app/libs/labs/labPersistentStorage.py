
import logging

from libs.lab import Lab
from libs.task import Task


class LabPersistentStorage(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 9"
        self.desc = "Persistent Storage"

        super().__init__(kube, db, self.name, self.desc)

        self.addTask(Task1(kube))
        self.addTask(Task2(kube))


class Task1(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "Created"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readVolumeClaim("mariadb-data"):
            self.setDone()


class Task2(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "Mounted"
        self.desc = "Sample description"

    def check(self):
        deploy = self.kube.readDeployment("mariadb")
        if not deploy:  # openshift case
            logging.info("9.2 openshift case")
            deploy = self.kube.readReplicationControllerByPodLabel(
                        "deploymentconfig=mariadb")
        if deploy:
            if deploy.spec.template.spec.volumes:
                for vol in deploy.spec.template.spec.volumes:
                    if vol.name == "mariadb-data":
                        self.setDone()
