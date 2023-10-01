
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
        self.objn = "backend-ingress-deny"

    def check(self):
        if self.kube.readNetworkPolicy(self.objn):
            self.setDone()
        else:
            logging.info("netpol openshift case")
            ns = f"{self.kube.ns}-netpol"
            if self.kube.readNetworkPolicy(self.objn, ns):
                self.setDone()


class LabAdditionalConceptsTask2(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Allow policy: created"
        self.desc = "network policy exists"
        self.objn = "backend-allow-ingress-frontend"

    def check(self):
        if self.kube.readNetworkPolicy(self.objn):
            self.setDone()
        else:
            logging.info("netpol openshift case")
            ns = f"{self.kube.ns}-netpol"
            if self.kube.readNetworkPolicy(self.objn, ns):
                self.setDone()


class LabAdditionalConceptsTask3(Task):

    def __init__(self, kube):
        Task.__init__(self, kube)

        self.name = "Pod: created"
        self.desc = "special pod exists"

    def check(self):
        if self.kube.readPod("security-context-demo"):
            self.setDone()
