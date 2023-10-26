
import logging

from libs.lab import Lab
from libs.task import Task


class LabAdditionalConcepts(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 9"
        self.desc = "Additional Concepts"

        Lab.__init__(self, kube, db, self.name, self.desc)

        self.addTask(LabAdditionalConceptsTask1(kube))
        self.addTask(LabAdditionalConceptsTask2(kube))
        self.addTask(LabAdditionalConceptsTask3(kube))
        self.addTask(LabAdditionalConceptsTask4(kube))


class LabAdditionalConceptsTask1(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "CronJobs and Jobs"
        self.desc = "job database-dump exist"

    def check(self):
        if self.kube.readJob("database-dump"):
            self.setDone()


class LabAdditionalConceptsTask2(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "ConfigMap: Created"
        self.desc = "configmap javaconfiguration is created"

    def check(self):
        if self.kube.readConfigMap("javaconfiguration"):
            self.setDone()


class LabAdditionalConceptsTask3(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "ConfigMap: Mounted"
        self.desc = "deployment has a configmap mounted"

    def check(self):
        deploy = self.kube.readDeployment("spring-boot-example")
        if not deploy:  # openshift case
            logging.info("10.5 openshift case")
            deploy = self.kube.readDeployment("example-web-app")
        if deploy:
            if deploy.spec.template.spec.volumes:
                for vol in deploy.spec.template.spec.volumes:
                    if vol.name == "config-volume":
                        self.setDone()


class LabAdditionalConceptsTask4(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "InitContainer"
        self.desc = "initcontainer wait-for-db exist in deployment"

    def check(self):
        deploy = self.kube.readDeployment("example-web-app")
        if deploy:
            if deploy.spec.template.spec.init_containers:
                for pod in deploy.spec.template.spec.init_containers:
                    if pod.name == "wait-for-db":
                        self.setDone()
