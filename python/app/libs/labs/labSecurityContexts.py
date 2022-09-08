
from libs.lab import Lab
from libs.task import Task


class LabSecurityContexts(Lab):

    def __init__(self, kube, db):

        self.name = "Lab 10"
        self.desc = "Security Contexts"

        Lab.__init__(self, kube, db, self.name, self.desc)

        self.addTask(LabAdditionalConceptsTask1(kube))
        self.addTask(LabAdditionalConceptsTask2(kube))
        self.addTask(LabAdditionalConceptsTask3(kube))


class LabAdditionalConceptsTask1(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Deny policy: created"
        self.desc = "network policy exists"

    def check(self):
        if self.kube.readNetworkPolicy("backend-ingress-deny"):
            self.setDone()


class LabAdditionalConceptsTask2(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Allow policy: created"
        self.desc = "network policy exists"

    def check(self):
        if self.kube.readNetworkPolicy("backend-allow-ingress-frontend"):
            self.setDone()


class LabAdditionalConceptsTask3(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Pod: created"
        self.desc = "special pod exists"

    def check(self):
        if self.kube.readPod("security-context-demo"):
            self.setDone()
