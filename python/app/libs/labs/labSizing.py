
from libs.lab import Lab
from libs.task import Task


class LabSizing(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 6"
        self.desc = "Scaling"

        super().__init__(kube, db, self.name, self.desc)

        self.addTask(Task1(kube))
        self.addTask(Task2(kube))


class Task1(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "Deployment"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readDeployment("example-web-python"):
            self.setDone()


class Task2(Task):

    def __init__(self, kube):
        super().__init(kube)

        self.name = "Scaled"
        self.desc = "Sample description"

    def check(self):
        replicas = self.kube.readDeploymentScale(self.deploy_name)
        if replicas:
            if replicas.spec.replicas == 3:
                self.setDone()
