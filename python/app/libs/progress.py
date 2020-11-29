#!/usr/bin/env python
#-*- coding: utf-8 -*-

from kubernetes.client.rest import ApiException
from libs.cluster import KubeCluster

class Progress():

    def __init__(self):
        self.lab = 5        # as this container will deployed in lab 6
                            # we are guessing all is done until lab 5
        self.db = None
        self.kube = None
        self.deploy_name = "example-web-python"


    def checkProgress(self, db):
        try:
            self.kube = KubeCluster()
            self.db = db
        except:
            pass
        else:
            self.checkLab06()


    def checkLab06(self):
        # check if deployment exists
        try:
            self.kube.readDeployment(self.deploy_name)
            replicas = self.kube.readDeploymentScale(self.deploy_name)
            print("%s" % replicas.spec.replicas)
            if replicas.spec.replicas != 3:
                raise ApiException
        except ApiException as error:
            self.lab = 5
            print("Error in processing lab 6: %s" % error)
        else:
            self.lab = 6
            self.checkLab07()


    def checkLab07(self):
        # check if we having a history file
        try:
            podLog = self.kube.readPodLogs(self.deploy_name)
            podLog.index("127.0.0.1")
        except ValueError:
            self.lab = 6
        except ApiException:
            self.lab = 6
        else:
            self.lab = 7
            self.checkLab08()


    def checkLab08(self):
        # check if database exists
        try:
            self.kube.readService("mariadb")
            self.kube.readDeployment("mariadb")
            self.db.query.filter_by(name='test').first()
        except ApiException:
            self.lab = 7
        except:
            self.lab = 7
        else:
            self.lab = 8
            self.checkLab09()


    def checkLab09(self):
        # check for volume claims
        try:
            self.kube.readVolumeClaim("mariadb-data")
        except ApiException:
            self.lab = 8
        else:
            self.lab = 9
            self.checkLab10()


    def checkLab10(self):
        # check statefulsets, daemonsets, jobs, configmaps ...
        try:
            self.kube.readStatefulSet("nginx-cluster") # Do not delete this in lab!
            self.kube.readJob("database-dump")
            self.kube.readConfigMap("javaconfig")
            self.kube.readDeployment("spring-boot-example")
            self.kube.readPodLogs("mariadb", "mysqld-exporter")
        except ApiException:
            self.lab = 9
        else:
            self.lab = 10
