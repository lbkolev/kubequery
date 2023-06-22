#
# def test_get_attr():
#    content = yaml.load(open("tests/assets/core-pod.yaml"), Loader=yaml.FullLoader)
#    V1PodSpec(content["spec"]).containers
#
#    deployment = V1Pod(spec=V1PodSpec(content["spec"]), metadata=content["metadata"])
#
#    label = rgetattr(deployment, "metadata.labels.app")
#    assert label == "nginx"
#
#
import pytest

from pprint import pprint

from kubequery.model import Model
from kubequery.client import Client
from kubequery.kubernetes.resources.workload import Workload


class TestWorkload():

    @staticmethod
    @pytest.mark.parametrize("namespace, attributes, filters, expected", [
        ("default", ["spec.dns_policy"], {"spec.service_account": "default", "metadata.name": "web-0"}, {"spec.dns_policy": ["ClusterFirst"]}),
        ("rand", ["metadata.name", "metadata.labels"], {}, {}),
    ])
    def test_select_pod(namespace, attributes, filters, expected):
        client = Client(
            contexts=["minikube"], namespace=namespace, attributes=attributes, filters=filters
        )
        wl = Workload(client)

        resp = wl.select("V1Pod")

        pprint(resp[0].values)
        assert len(resp) == 1
        assert resp[0].values == expected

    @staticmethod
    @pytest.mark.parametrize("namespace, attributes, filters, expected", [
        ("default", ["spec.replicas", "spec.progress_deadline_seconds"], {"metadata.name": "nginx-app"}, {"spec.replicas": [3], "spec.progress_deadline_seconds": [600]}),
        ("rand", ["metadata.name", "metadata.labels"], {"spec.replicas": 3}, {}),
    ])
    def test_select_deployment(namespace, attributes, filters, expected):
        client = Client(
            contexts=["minikube"], namespace=namespace, attributes=attributes, filters=filters
        )
        wl = Workload(client)

        resp = wl.select("deployment")
        
        pprint(resp[0].values)
        assert len(resp) == 1
        assert resp[0].values == expected


    @staticmethod
    def test_select_replicaset():
        ...

    @staticmethod
    def test_select_statefulset():
        ...

    @staticmethod
    def test_select_daemonset():
        ...

    @staticmethod
    def test_select_job():
        ...

    @staticmethod
    def test_select_cronjob():
        ...