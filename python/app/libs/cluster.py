#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kubernetes


class KubeCluster():

    def __init__(self):
        kubernetes.config.load_incluster_config()
        self.ns = self.getNamespace()
        self.coreV1 = kubernetes.client.CoreV1Api()
        self.appsV1 = kubernetes.client.AppsV1Api()
        self.betaV1 = kubernetes.client.ExtensionsV1beta1Api()
        self.batchV1 = kubernetes.client.BatchV1Api()

    def getNamespace(self, nsFile=""):
        if not nsFile:
            nsFile = "/run/secrets/kubernetes.io/serviceaccount/namespace"

        with open(nsFile, "r") as reader:
            return reader.read()

    def listPods(self):
        return self.coreV1.list_namespaced_pod(self.ns)

    def readDeployment(self, name):
        return self.appsV1.read_namespaced_deployment(name, self.ns)

    def readDeploymentScale(self, name):
        return self.appsV1.read_namespaced_deployment_scale(name, self.ns)

    def readService(self, name):
        return self.coreV1.read_namespaced_service(name, self.ns)

    def readPodLogs(self, labelName):
        logList = []
        label = "app=%s" % labelName
        for pod in self.coreV1.list_namespaced_pod(self.ns,
                                                   label_selector=label).items:
            log = self.coreV1.read_namespaced_pod_log(pod.metadata.name,
                                                      self.ns)
            logList.append(log)
        return logList

    def readVolumeClaim(self, name):
        return self.coreV1.read_namespaced_persistent_volume_claim(name,
                                                                   self.ns)

    def readStatefulSet(self, name):
        return self.appsV1.read_namespaced_stateful_set(name, self.ns)

    def readConfigMap(self, name):
        return self.coreV1.read_namespaced_config_map(name, self.ns)

    def readJob(self, name):
        return self.batchV1.read_namespaced_job(name, self.ns)
