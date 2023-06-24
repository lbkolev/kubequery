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
        ("rand", ["metadata.name", "metadata.labels"], {"spec.replicas": 69}, {}),
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
    @pytest.mark.parametrize("namespace, attributes, filters, expected", [
        ("default", ["spec.replicas", "spec.template.spec.scheduler_name"], {"metadata.name": "frontend"}, {"spec.replicas": [3], "spec.template.spec.scheduler_name": ["default-scheduler"]}),
        ("rand", ["metadata.name", "metadata.labels"], {"spec.replicas": 69}, {}),
    ])
    def test_select_replicaset(namespace, attributes, filters, expected):
        client = Client(
            contexts=["minikube"], namespace=namespace, attributes=attributes, filters=filters
        )
        wl = Workload(client)
        resp = wl.select("replicasets")

        pprint(resp[0].values)
        assert len(resp) == 1
        assert resp[0].values == expected

    @staticmethod
    @pytest.mark.parametrize("namespace, attributes, filters, expected", [
        ("default", ["spec.update_strategy.type"], {}, {"spec.update_strategy.type": ["RollingUpdate"]}),
        ("rand", ["metadata.name", "metadata.labels"], {"spec.replicas": 69}, {}),
    ])
    def test_select_statefulset(namespace, attributes, filters, expected):
        client = Client(
            contexts=["minikube"], namespace=namespace, attributes=attributes, filters=filters
        )
        wl = Workload(client)
        resp = wl.select("statefulset")

        pprint(resp[0].values)
        assert len(resp) == 1
        assert resp[0].values == expected

    @staticmethod
    @pytest.mark.parametrize("namespace, attributes, filters, expected", [
        ("kube-system", ["spec.template.metadata.creation_timestamp"], {"metadata.name": "kube-proxy"}, {"spec.template.metadata.creation_timestamp": [None]}),
        ("rand", ["metadata.name", "metadata.labels"], {}, {}),
    ])
    def test_select_daemonset(namespace, attributes, filters, expected):
        client = Client(
            contexts=["minikube"], namespace=namespace, attributes=attributes, filters=filters
        )
        wl = Workload(client)
        resp = wl.select("daemonset")

        pprint(resp[0].values)
        assert len(resp) == 1
        assert resp[0].values == expected

    @staticmethod
    @pytest.mark.parametrize("namespace, attributes, filters, expected", [
        ("default", ["spec.completions", "spec.parallelism", "spec.completion_mode"], {"metadata.name": "pi"}, {"spec.completions": [1], "spec.parallelism": [1], "spec.completion_mode": ["NonIndexed"]}),
        ("rand", ["metadata.name", "metadata.labels"], {}, {}),
    ])
    def test_select_job(namespace, attributes, filters, expected):
        client = Client(
            contexts=["minikube"], namespace=namespace, attributes=attributes, filters=filters
        )
        wl = Workload(client)
        resp = wl.select("jobs")

        pprint(resp[0].values)
        assert len(resp) == 1
        assert resp[0].values == expected

    @staticmethod
    @pytest.mark.parametrize("namespace, attributes, filters, expected", [
        ("default", ["spec.schedule", ], {"metadata.name": "hello"}, {"spec.schedule": ["* * * * *"]}),
        ("rand", ["metadata.name", "metadata.labels"], {}, {}),
    ])
    def test_select_cronjob(namespace, attributes, filters, expected):
        client = Client(
            contexts=["minikube"], namespace=namespace, attributes=attributes, filters=filters
        )
        wl = Workload(client)
        resp = wl.select("cronjob")

        pprint(resp[0].values)
        assert len(resp) == 1
        assert resp[0].values == expected