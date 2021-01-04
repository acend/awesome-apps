#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from kubernetes.client.rest import ApiException
from libs.cluster import KubeCluster

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)-5s: %(message)s")


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
        try:
            self.kube.listPods()
            return True
        except ApiException as error:
            logging.error("Error with permissions: %s" % error)
            return False

    def checkLab06(self, labs):
        lab = {"name": "", "desc": "", "tasks": []}
        lab["name"] = "Lab 6"
        lab["desc"] = "Scaling"
        task1 = {"name": "Deployment", "status": "open"}
        task2 = {"name": "Replicas", "status": "open"}
        try:
            logging.info("Checking: %s" % lab["name"])
            self.kube.readDeployment(self.deploy_name)
            task1["status"] = "done"

            replicas = self.kube.readDeploymentScale(self.deploy_name)
            if replicas.spec.replicas == 3:
                task2["status"] = "done"
        except ApiException as error:
            logging.error("Error in processing lab 6: %s" % error)

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
        try:
            logging.info("Checking: %s" % lab["name"])
            podLogList = self.kube.readPodLogs(self.deploy_name)
            for podLog in podLogList:
                if podLog.find("127.0.0.1") > 0:
                    task1["status"] = "done"
        except ApiException as error:
            logging.error("Error in processing lab 7: %s" % error)
        finally:
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
        try:
            logging.info("Checking: %s" % lab["name"])
            self.kube.readService("mariadb")
            task1["status"] = "done"

            self.kube.readDeployment("mariadb")
            task2["status"] = "done"

            if self.db.query.filter_by(name='Daniel').first():
                task3["status"] = "done"
        except ApiException as error:
            logging.error("Error in processing lab 8: %s" % error)
        except Exception as error:
            logging.error("Error in processing lab 8: %s" % error)

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
        try:
            logging.info("Checking: %s" % lab["name"])
            self.kube.readVolumeClaim("mariadb-data")
            task1["status"] = "done"

            deploy = self.kube.readDeployment("mariadb")
            if deploy.spec.template.spec.volumes:
                for vol in deploy.spec.template.spec.volumes:
                    if vol.name == "mariadb-persistent-storage":
                        task2["status"] = "done"
        except ApiException as error:
            logging.error("Error in processing lab 9: %s" % error)

        lab["tasks"].append(task1)
        lab["tasks"].append(task2)
        labs.append(lab)
        return self.checkLab10(labs)

    def checkLab10(self, labs):
        # check statefulsets, daemonsets, jobs, configmaps ...
        lab = {"name": "", "desc": "", "tasks": []}
        lab["name"] = "Lab 10"
        lab["desc"] = "Additional concepts"
        task1 = {"name": "1-StatefulSets", "status": "open"}
        task2 = {"name": "3-CronJobs and Jobs", "status": "open"}
        task3 = {"name": "4-ConfigMap: ConfigMap", "status": "open"}
        task4 = {"name": "4-ConfigMap: Deployment", "status": "open"}
        task5 = {"name": "7-Sidecar containers", "status": "open"}
        try:
            logging.info("Checking: %s" % lab["name"])
            self.kube.readStatefulSet("nginx-cluster")
            task1["status"] = "done"

            self.kube.readJob("database-dump")
            task2["status"] = "done"

            self.kube.readConfigMap("javaconfiguration")
            task3["status"] = "done"

            self.kube.readDeployment("spring-boot-example")
            task4["status"] = "done"

            deploy = self.kube.readDeployment("mariadb")
            if deploy.spec.template.spec.containers:
                for pod in deploy.spec.template.spec.containers:
                    if pod.name == "mysqld-exporter":
                        task5["status"] = "done"
        except ApiException as error:
            logging.error("Error in processing lab 10: %s" % error)

        lab["tasks"].append(task1)
        lab["tasks"].append(task2)
        lab["tasks"].append(task3)
        lab["tasks"].append(task4)
        lab["tasks"].append(task5)
        labs.append(lab)
        return labs
