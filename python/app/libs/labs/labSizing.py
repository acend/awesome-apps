
from libs.lab import Lab
from libs.task import Task


class LabSizing(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 5"
        self.desc = "Scaling"

        Lab.__init__(self, kube, db, self.name, self.desc)

        self.addTask(LabSizingTask1(kube))
        self.addTask(LabSizingTask2(kube))


class LabSizingTask1(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Deployment"
        self.desc = "Sample description"

    def check(self):
        if self.kube.readDeployment("example-web-python"):
            self.setDone()


class LabSizingTask2(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Scaled"
        self.desc = "Sample description"

    def check(self):
        replicas = self.kube.readDeploymentScale(self.deploy_name)
        if replicas:
            if replicas.spec.replicas == 3:
                self.setDone()
