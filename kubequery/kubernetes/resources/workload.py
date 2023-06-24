from typing import Any

from kubernetes import client, config
from kubernetes.client.models import (
    V1CronJob,
    V1CronJobList,
    V1DaemonSet,
    V1DaemonSetList,
    V1Deployment,
    V1DeploymentList,
    V1Job,
    V1JobList,
    V1Pod,
    V1PodList,
    V1ReplicaSet,
    V1ReplicaSetList,
    V1StatefulSet,
    V1StatefulSetList,
)

import kubequery
from kubequery.kubernetes.resources.base import KubernetesResourceBase
from kubequery.kubernetes.utils import rgetattr
from kubequery.model import Model


class Workload(KubernetesResourceBase):
    supported = [
        V1Pod.__name__,
        "pod",
        "pods",
        V1ReplicaSet.__name__,
        "replicaset",
        "replicasets",
        V1Deployment.__name__,
        "deployment",
        "deployments",
        V1StatefulSet.__name__,
        "statefulset",
        "statefulsets",
        V1DaemonSet.__name__,
        "daemonset",
        "daemonsets",
        V1Job.__name__,
        "job",
        "jobs",
        V1CronJob.__name__,
        "cronjob",
        "cronjobs",
    ]

    def __init__(self, client: kubequery.client.Client):
        self.client = client

    def select(self, workload: str) -> list[Model]:
        result: list[Model] = []

        if workload not in self.supported:
            raise kubequery.exceptions.UnsupportedResource(workload)

        for context in self.client.contexts:
            config.load_kube_config(context=context)  # type: ignore[attr-defined]
            core = client.CoreV1Api()
            apps = client.AppsV1Api()
            batch = client.BatchV1Api()
            # batch_beta = client.BatchV1beta1Api()
            model = Model(context=context, resource=workload, values={})
            resources: Any

            match workload.lower():
                case "v1pod" | "pod" | "pods":
                    resources = self._select_pod(client=core)
                case "v1replicaset" | "replicaset" | "replicasets":
                    resources = self._select_replicaset(client=apps)
                case "v1deployment" | "deployment" | "deployments":
                    resources = self._select_deployment(client=apps)
                case "v1statefulset" | "statefulset" | "statefulsets":
                    resources = self._select_statefulset(client=apps)
                case "v1daemonset" | "daemonset" | "daemonsets":
                    resources = self._select_daemonset(client=apps)
                case "v1job" | "job" | "jobs":
                    resources = self._select_job(client=batch)
                case "v1cronjob" | "cronjob" | "cronjobs":
                    resources = self._select_cronjob(client=batch)
                case _:
                    raise NotImplementedError(workload)

            for resource in resources.items:
                if all(rgetattr(resource, k) == v for k, v in self.client.filters.items()):
                    for attribute in self.client.attributes:
                        model.insert(attribute, rgetattr(resource, attribute))

            result.append(model)

        return result

    def _select_pod(self, client: client.CoreV1Api) -> V1PodList:
        match self.client.namespace:
            case "*":
                return client.list_pod_for_all_namespaces()
            case _:
                return client.list_namespaced_pod(namespace=self.client.namespace)

    def _select_replicaset(self, client: client.AppsV1Api) -> V1ReplicaSetList:
        match self.client.namespace:
            case "*":
                return client.list_replica_set_for_all_namespaces()
            case _:
                return client.list_namespaced_replica_set(namespace=self.client.namespace)

    def _select_deployment(self, client: client.AppsV1Api) -> V1DeploymentList:
        match self.client.namespace:
            case "*":
                return client.list_deployment_for_all_namespaces()
            case _:
                return client.list_namespaced_deployment(namespace=self.client.namespace)

    def _select_statefulset(self, client: client.AppsV1Api) -> V1StatefulSetList:
        match self.client.namespace:
            case "*":
                return client.list_stateful_set_for_all_namespaces()
            case _:
                return client.list_namespaced_stateful_set(namespace=self.client.namespace)

    def _select_daemonset(self, client: client.AppsV1Api) -> V1DaemonSetList:
        match self.client.namespace:
            case "*":
                return client.list_daemon_set_for_all_namespaces()
            case _:
                return client.list_namespaced_daemon_set(namespace=self.client.namespace)

    def _select_job(self, client: client.BatchV1Api) -> V1JobList:
        match self.client.namespace:
            case "*":
                return client.list_job_for_all_namespaces()
            case _:
                return client.list_namespaced_job(namespace=self.client.namespace)

    def _select_cronjob(self, client: client.BatchV1Api) -> V1CronJobList:
        match self.client.namespace:
            case "*":
                return client.list_cron_job_for_all_namespaces()
            case _:
                return client.list_namespaced_cron_job(namespace=self.client.namespace)
