
import logging

from libs.lab import Lab
from libs.task import Task


class LabAdditionalConcepts(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 8"
        self.desc = "Database"

        super().__init__(kube, db, self.name, self.desc)

        self.addTask(Task1(kube))
        self.addTask(Task2(kube))
        self.addTask(Task3(kube))
        self.addTask(Task4(kube))
        self.addTask(Task5(kube))
        self.addTask(Task6(kube))
        self.addTask(Task7(kube))


class Task1(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "StatefulSets: Created"
        self.desc = "Sample description"

    def check(self):
        replicas = self.kube.readStatefulSet("nginx-cluster")
        if replicas:
            self.setDone()


class Task2(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "StatefulSets: Scaled"
        self.desc = "Sample description"

    def check(self):
        replicas = self.kube.readStatefulSet("nginx-cluster")
        if replicas and replicas.spec.replicas == 3:
            self.setDone()


class Task3(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "CronJobs and Jobs"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readJob("database-dump"):
            self.setDone()


class Task4(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "ConfigMap: Created"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readConfigMap("javaconfiguration"):
            self.setDone()


class Task5(Task):

    def __init__(self, kube):
        super().__init(kube)

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


class Task6(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "InitContainer"
        self.desc = "Sample description"

    def check(self):
        deploy = self.kube.readDeployment(self.deploy_name)
        if deploy:
            if deploy.spec.template.spec.init_containers:
                for pod in deploy.spec.template.spec.init_containers:
                    if pod.name == "wait-for-db":
                        self.setDone()


class Task7(Task):

    def __init__(self, kube):
        super().__init(kube)

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
