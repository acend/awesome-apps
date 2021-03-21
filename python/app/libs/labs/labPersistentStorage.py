
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
        self.desc = "pvc has been created"

    def check(self):
        if self.kube.readVolumeClaim("mariadb-data"):
            self.setDone()


class LabPersistentStorageTask2(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Mounted"
        self.desc = "pvc is mounted to mariadb"

    def check(self):
        deploy = self.kube.readDeployment("mariadb")
        if not deploy:  # openshift case
            logging.info("9.2 openshift case")
            deploy = self.kube.readReplicationControllerByPodLabel(
                        "deploymentconfig=mariadb")

        if deploy:
            if not deploy.spec.template.spec.containers:
                return
            for con in deploy.spec.template.spec.containers:
                if con.volume_mounts:
                    for vol in con.volume_mounts:
                        if (vol.name == "mariadb-data" and
                           vol.mount_path == "/var/lib/mysql"):
                            self.setDone()
