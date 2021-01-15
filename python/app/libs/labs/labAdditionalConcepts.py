
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
        self.addTask(LabAdditionalConceptsTask5(kube))
        self.addTask(LabAdditionalConceptsTask6(kube))
        self.addTask(LabAdditionalConceptsTask7(kube))


class LabAdditionalConceptsTask1(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "StatefulSets: Created"
        self.desc = "Sample description"

    def check(self):
        replicas = self.kube.readStatefulSet("nginx-cluster")
        if replicas:
            self.setDone()


class LabAdditionalConceptsTask2(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "StatefulSets: Scaled"
        self.desc = "Sample description"

    def check(self):
        replicas = self.kube.readStatefulSet("nginx-cluster")
        if replicas and replicas.spec.replicas == 3:
            self.setDone()


class LabAdditionalConceptsTask3(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "CronJobs and Jobs"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readJob("database-dump"):
            self.setDone()


class LabAdditionalConceptsTask4(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "ConfigMap: Created"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readConfigMap("javaconfiguration"):
            self.setDone()


class LabAdditionalConceptsTask5(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "ConfigMap: Created"
        self.desc = "Sample description"

    def check(self):
        deploy = self.kube.readDeployment("spring-boot-example")
        if not deploy:  # openshift case
            logging.info("10.5 openshift case")
            deploy = self.kube.readDeployment(self.deploy_name)
        if deploy:
            if deploy.spec.template.spec.volumes:
                for vol in deploy.spec.template.spec.volumes:
                    if vol.name == "config-volume":
                        self.setDone()


class LabAdditionalConceptsTask6(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "InitContainer"
        self.desc = "Sample description"

    def check(self):
        deploy = self.kube.readDeployment(self.deploy_name)
        if deploy:
            if deploy.spec.template.spec.init_containers:
                for pod in deploy.spec.template.spec.init_containers:
                    if pod.name == "wait-for-db":
                        self.setDone()


class LabAdditionalConceptsTask7(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Sidecar containers"
        self.desc = "Sample description"

    def check(self):
        deploy = self.kube.readDeployment("mariadb")
        if not deploy:  # openshift case
            logging.info("10.6 openshift case")
            deploy = self.kube.readReplicationControllerByPodLabel(
                        "deploymentconfig=mariadb")
        if deploy:
            if deploy.spec.template.spec.containers:
                for pod in deploy.spec.template.spec.containers:
                    if pod.name == "mysqld-exporter":
                        self.setDone()
