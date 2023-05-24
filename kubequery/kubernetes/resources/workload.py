from typing import Any

from kubernetes import client, config
from kubernetes.client.models.v1_pod import V1Pod

from kubequery import exceptions
from kubequery.client import Client
from kubequery.kubernetes.resources.base import KubernetesResourceBase
from kubequery.kubernetes.utils import rgetattr


class Workload(KubernetesResourceBase):
    supported = [
        "Pod",
        "PodTemplate",
        "ReplicationController",
        "ReplicaSet",
        "Deployment",
        "StatefulSet",
        "ControllerRevision",
        "DaemonSet",
        "Job",
        "CronJob",
        "HorizontalPodAutoscaler",
        "PriorityClass",
        "PodSchedulingContext",
        "ResourceClaim",
        "ResourceClaimTemplate",
        "ResourceClass",
    ]

    def __init__(self, client: Client):
        self.client = client

    def select(self, workload: str) -> list[Any]:
        result = []

        if workload not in self.supported:
            raise exceptions.UnsupportedResource(workload)

        match workload:
            case "Pod":
                result = self._select_pod()
            case _:
                raise NotImplemented(workload)

        return result

    def _select_pod(self) -> list[Any]:
        result = []

        for cluster in self.client.clusters:
            config.load_kube_config(context=cluster)
            v1 = client.CoreV1Api()
            resources: V1Pod

            match self.client.namespace.lower():
                case None:
                    resources = v1.list_namespaced_pod()
                case "all":
                    resources = v1.list_pod_for_all_namespaces()
                case _:
                    resources = v1.list_namespaced_pod(namespace=self.client.namespace)

            for pod in resources.items:
                if all(rgetattr(pod, k) == v for k, v in self.client.filters.items()):
                    result.append(pod)

        return result
