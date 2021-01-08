#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from libs.cluster import KubeCluster

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)-5s: %(message)s")

job_template = {"name": "", "desc": "", "tasks": []}


class Progress():

    def __init__(self):
        self.db = None
        self.kube = None
        self.deploy_name = "example-web-python"

    def checkProgress(self, db):
        try:
            self.kube = KubeCluster()
            self.db = db
        except Exception as error:
            logging.error("Error in checkProgress: %s" % error)
            return []

        if self.checkPermission():
            return self.checkLab06(labs=[])
        else:
            return []

    def checkPermission(self):
        if self.kube.listPods():
            return True
        else:
            return False

    def calcPercentage(self, labs):
        """
        expect: list of dict
        return: integer
        """
        task_sum = 0
        task_done = 0
        if not labs:
            return 0
        for lab in labs:
            for task in lab["tasks"]:
                task_sum += 1
                if task["status"] == "done":
                    task_done += 1
        return int(task_done / task_sum * 100)

    def checkLab06(self, labs):
        lab = {"name": "", "desc": "", "tasks": []}
        lab["name"] = "Lab 6"
        lab["desc"] = "Scaling"
        task1 = {"name": "Deployment", "status": "open"}
        task2 = {"name": "Scaled", "status": "open"}
        logging.info("Checking: %s" % lab["name"])

        # task 1
        if self.kube.readDeployment(self.deploy_name):
            task1["status"] = "done"

        # task 2
        replicas = self.kube.readDeploymentScale(self.deploy_name)
        if replicas:
            if replicas.spec.replicas == 3:
                task2["status"] = "done"

        lab["tasks"].append(task1)
        lab["tasks"].append(task2)
        labs.append(lab)
        return self.checkLab07(labs)

    def checkLab07(self, labs):
        # check if we having a history file
        lab = {"name": "", "desc": "", "tasks": []}
        lab["name"] = "Lab 7"
        lab["desc"] = "Troubleshooting (badge can toggle)"
        task1 = {"name": "Local access", "status": "open"}
        logging.info("Checking: %s" % lab["name"])

        podLogList = self.kube.readPodLogs(
                        "app=%s" % self.deploy_name)
        if podLogList:
            for podLog in podLogList:
                if podLog.find("127.0.0.1") > 0:
                    task1["status"] = "done"
            del podLogList

        lab["tasks"].append(task1)
        labs.append(lab)
        return self.checkLab08(labs)

    def checkLab08(self, labs):
        # check if database exists
        lab = {"name": "", "desc": "", "tasks": []}
        lab["name"] = "Lab 8"
        lab["desc"] = "Database"
        task1 = {"name": "Service", "status": "open"}
        task2 = {"name": "Deployment", "status": "open"}
        task3 = {"name": "Dump import", "status": "open"}
        logging.info("Checking: %s" % lab["name"])

        if self.kube.readService("mariadb"):
            task1["status"] = "done"

        if self.kube.readDeployment("mariadb"):
            task2["status"] = "done"
        elif self.kube.readPodByLabel("deploymentconfig=mariadb"):
            logging.info("8.2 openshift case")
            task2["status"] = "done"

        try:
            if self.db.query.filter_by(name='Daniel').first():
                task3["status"] = "done"
        except Exception:
            pass

        lab["tasks"].append(task1)
        lab["tasks"].append(task2)
        lab["tasks"].append(task3)
        labs.append(lab)
        return self.checkLab09(labs)

    def checkLab09(self, labs):
        # check for volume claims
        lab = {"name": "", "desc": "", "tasks": []}
        lab["name"] = "Lab 9"
        lab["desc"] = "Persistent storage"
        task1 = {"name": "Created", "status": "open"}
        task2 = {"name": "Mounted", "status": "open"}
        logging.info("Checking: %s" % lab["name"])

        if self.kube.readVolumeClaim("mariadb-data"):
            task1["status"] = "done"

        deploy = self.kube.readDeployment("mariadb")
        if not deploy:  # openshift case
            logging.info("9.2 openshift case")
            deploy = self.kube.readReplicationControllerByPodLabel(
                        "deploymentconfig=mariadb")
        if deploy:
            if deploy.spec.template.spec.volumes:
                for vol in deploy.spec.template.spec.volumes:
                    if vol.name == "mariadb-persistent-storage":
                        task2["status"] = "done"

        lab["tasks"].append(task1)
        lab["tasks"].append(task2)
        labs.append(lab)
        return self.checkLab10(labs)

    def checkLab10(self, labs):
        # check statefulsets, daemonsets, jobs, configmaps ...
        lab = {"name": "", "desc": "", "tasks": []}
        lab["name"] = "Lab 10"
        lab["desc"] = "Additional concepts"
        task1 = {"name": "StatefulSets: Created", "status": "open"}
        task2 = {"name": "StatefulSets: Scaled", "status": "open"}
        task3 = {"name": "CronJobs and Jobs", "status": "open"}
        task4 = {"name": "ConfigMap: Created", "status": "open"}
        task5 = {"name": "ConfigMap: Mounted", "status": "open"}
        task6 = {"name": "InitContainer", "status": "open"}
        task7 = {"name": "Sidecar containers", "status": "open"}
        logging.info("Checking: %s" % lab["name"])

        replicas = self.kube.readStatefulSet("nginx-cluster")
        if replicas:
            task1["status"] = "done"
            if replicas.spec.replicas == 3:
                task2["status"] = "done"

        if self.kube.readJob("database-dump"):
            task3["status"] = "done"

        if self.kube.readConfigMap("javaconfiguration"):
            task4["status"] = "done"

        deploy = self.kube.readDeployment("spring-boot-example")
        if not deploy:  # openshift case
            logging.info("10.5 openshift case")
            deploy = self.kube.readDeployment(self.deploy_name)
        if deploy:
            if deploy.spec.template.spec.volumes:
                for vol in deploy.spec.template.spec.volumes:
                    if vol.name == "config-volume":
                        task5["status"] = "done"

        deploy = self.kube.readDeployment(self.deploy_name)
        if deploy:
            if deploy.spec.template.spec.init_containers:
                for pod in deploy.spec.template.spec.init_containers:
                    if pod.name == "wait-for-db":
                        task6["status"] = "done"

        deploy = self.kube.readDeployment("mariadb")
        if not deploy:  # openshift case
            logging.info("10.6 openshift case")
            deploy = self.kube.readReplicationControllerByPodLabel(
                        "deploymentconfig=mariadb")
        if deploy:
            if deploy.spec.template.spec.containers:
                for pod in deploy.spec.template.spec.containers:
                    if pod.name == "mysqld-exporter":
                        task7["status"] = "done"

        lab["tasks"].append(task1)
        lab["tasks"].append(task2)
        lab["tasks"].append(task3)
        lab["tasks"].append(task4)
        lab["tasks"].append(task5)
        lab["tasks"].append(task6)
        lab["tasks"].append(task7)
        labs.append(lab)
        return labs
