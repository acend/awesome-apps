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


class Progress():

    labs = []

    def __init__(self, database):
        self.db = database
        self.kube = None

    def getNamespace(self):
        return self.kube.getNamespace()

    def checkProgress(self):
        try:
            self.kube = KubeCluster()
        except Exception as error:
            logging.error("Error in checkProgress: %s" % error)
            return []

        if self.checkPermission():
            self.labs.clear()
            self.labs.append(LabSizing(self.kube, self.db))
            self.labs.append(LabTroubleshooting(self.kube, self.db))
            self.labs.append(LabDatabase(self.kube, self.db))
            self.labs.append(LabPersistentStorage(self.kube, self.db))
            self.labs.append(LabAdditionalConcepts(self.kube, self.db))

            for lab in self.labs:
                lab.check()
            return [lab for lab in self.labs]
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

        logging.info("Tasks {}".format(task_sum))
        logging.info("Done {}".format(task_done))

        if not self.labs:
            return 0

        return int(task_done / task_sum * 100)
