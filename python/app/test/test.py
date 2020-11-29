import os, kubernetes
from libs.ldap_controller import LdapController


testdata  = "kubeexample"
testvalue = 1

#kube_cluster
def test_loadClusters():
    kubeCluster.loadClusters(section = "example")
    assert kubeCluster.clusters != []


