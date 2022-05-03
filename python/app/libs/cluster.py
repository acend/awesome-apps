#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import kubernetes
from kubernetes.client.rest import ApiException


class KubeCluster():

    def __init__(self):
        self.debug = os.getenv("DEBUG", "false")
        try:
            kubernetes.config.load_incluster_config()
        except Exception:
            print("ERROR: could not load k8s config")
        else:
            self.ns = self.getNamespace()
            self.coreV1 = kubernetes.client.CoreV1Api()
            self.appsV1 = kubernetes.client.AppsV1Api()
            self.batchV1 = kubernetes.client.BatchV1Api()

    def getNamespace(self, nsFile=""):
        if not nsFile:
            nsFile = "/run/secrets/kubernetes.io/serviceaccount/namespace"

        with open(nsFile, "r") as reader:
            return reader.read()

    def listPods(self):
        try:
            return self.coreV1.list_namespaced_pod(self.ns)
        except ApiException:
            return None

    def readPodByLabel(self, label):
        try:
            for pod in self.coreV1.list_namespaced_pod(
                        self.ns, label_selector=label).items:
                return self.coreV1.read_namespaced_pod(
                        pod.metadata.name, self.ns)
        except ApiException:
            return None

    def readDeployment(self, name):
        try:
            return self.appsV1.read_namespaced_deployment(name, self.ns)
        except ApiException:
            return None

    def readReplicationControllerByPodLabel(self, label):
        try:
            for pod in self.coreV1.list_namespaced_pod(
                        self.ns, label_selector=label).items:
                result = self.coreV1.read_namespaced_pod(
                            pod.metadata.name, self.ns)
                for ref in result.metadata.owner_references:
                    return self.coreV1.read_namespaced_replication_controller(
                            ref.name, self.ns)
        except ApiException:
            return None

    def readDeploymentScale(self, name):
        try:
            return self.appsV1.read_namespaced_deployment_scale(name, self.ns)
        except ApiException:
            return None

    def readService(self, name):
        try:
            return self.coreV1.read_namespaced_service(name, self.ns)
        except ApiException:
            if self.debug == "true":
                print(f"DEBUG: could not get service {name}")
            return None

    def readPodLogs(self, label):
        logList = []
        try:
            for pod in self.coreV1.list_namespaced_pod(
                        self.ns, label_selector=label).items:
                log = self.coreV1.read_namespaced_pod_log(
                        pod.metadata.name, self.ns)
                logList.append(log)
            return logList
        except ApiException:
            if self.debug == "true":
                print(f"DEBUG: could not get label {label}")
            return None

    def readVolumeClaim(self, name):
        try:
            return self.coreV1.read_namespaced_persistent_volume_claim(
                    name, self.ns)
        except ApiException:
            if self.debug == "true":
                print(f"DEBUG: could not get claim {name}")
            return None

    def readStatefulSet(self, name):
        try:
            return self.appsV1.read_namespaced_stateful_set(name, self.ns)
        except ApiException:
            return None

    def readConfigMap(self, name):
        try:
            return self.coreV1.read_namespaced_config_map(name, self.ns)
        except ApiException:
            return None

    def readJob(self, name):
        try:
            return self.batchV1.read_namespaced_job(name, self.ns)
        except ApiException:
            return None
