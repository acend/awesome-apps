
import logging

from libs.lab import Lab
from libs.task import Task


class LabPersistentStorage(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 8"
        self.desc = "Persistent Storage"

        Lab.__init__(self, kube, db, self.name, self.desc)

        self.addTask(LabPersistentStorageTask1(kube))
        self.addTask(LabPersistentStorageTask2(kube))


class LabPersistentStorageTask1(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Created"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readVolumeClaim("mariadb-data"):
            self.setDone()


class LabPersistentStorageTask2(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Mounted"
        self.desc = "Sample description"

    def check(self):
        name = "mariadb-data"
        deploy = self.kube.readDeployment("mariadb")
        if not deploy:  # openshift case
            logging.info("9.2 openshift case")
            deploy = self.kube.readReplicationControllerByPodLabel(
                        "deploymentconfig=mariadb")
        if deploy:
            if deploy.spec.template.spec.volumes:
                for vol in deploy.spec.template.spec.volumes:
                    if vol.persistent_volume_claim:
                        if vol.persistent_volume_claim.claim_name == name:
                            self.setDone()
