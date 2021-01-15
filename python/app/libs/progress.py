#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from libs.cluster import KubeCluster

from libs.labs.labSizing import LabSizing
from libs.labs.labTroubleshooting import LabTroubleshooting
from libs.labs.labDatabase import LabDatabase
from libs.labs.labPersistentStorage import LabPersistentStorage
from libs.labs.labAdditionalConcepts import LabAdditionalConcepts

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)-5s: %(message)s")

job_template = {"name": "", "desc": "", "tasks": []}


DEPLOY_NAME = "example-web-python"


class Progress():

    labs = []

    def __init__(self):
        self.db = None
        self.kube = None

        self.labs.append(LabSizing(self.kube))
        self.labs.append(LabTroubleshooting(self.kube))
        self.labs.append(LabDatabase(self.kube))
        self.labs.append(LabPersistentStorage(self.kube))
        self.labs.append(LabAdditionalConcepts(self.kube))

    def getNamespace(self):
        return self.kube.getNamespace()

    def checkProgress(self, db):
        try:
            self.kube = KubeCluster()
            self.db = db
        except Exception as error:
            logging.error("Error in checkProgress: %s" % error)
            return []

        if self.checkPermission():
            return [lab.getStatus() for lab in self.labs]
        else:
            return []

    def checkPermission(self):
        if self.kube.listPods():
            return True
        else:
            return False

    def calcPercentage(self):
        """
        expect: list of dict
        return: integer
        """

        task_sum = sum([lab.countTasks() for lab in self.labs])
        task_done = sum([lab.countDone() for lab in self.labs])

        if not self.labs:
            return 0

        return int(task_done / task_sum * 100)
