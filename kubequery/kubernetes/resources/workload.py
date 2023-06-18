from typing import Any

from kubernetes import client, config
from kubernetes.client.models import (
    V1CronJob,
    V1CronJobList,
    V1DaemonSet,
    V1DaemonSetList,
    V1Deployment,
    V1DeploymentList,
    V1HorizontalPodAutoscaler,
    V1HorizontalPodAutoscalerList,
    V1Job,
    V1JobList,
    V1Pod,
    V1PodList,
    V1PodTemplate,
    V1PodTemplateList,
    V1ReplicaSet,
    V1ReplicaSetList,
    V1ReplicationController,
    V1ReplicationControllerList,
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
        V1PodTemplate.__name__,
        V1ReplicationController.__name__,
        V1ReplicaSet.__name__,
        V1Deployment.__name__,
        V1StatefulSet.__name__,
        V1DaemonSet.__name__,
        V1Job.__name__,
        V1CronJob.__name__,
        V1HorizontalPodAutoscaler.__name__,
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
            #batch_beta = client.BatchV1beta1Api()
            autoscaling = client.AutoscalingV1Api()
            model = Model(context=context, resource=workload, values={})
            resources: Any

            match workload:
                case "V1Pod":
                    resources = self._select_pod(client=core)
                case "PodTemplate":
                    resources = self._select_pod_template(client=core)
                case "ReplicationController":
                    resources = self._select_replication_controller(client=core)
                case "ReplicaSet":
                    resources = self._select_replicaset(client=apps)
                case "Deployment":
                    resources = self._select_deployment(client=apps)
                case "StatefulSet":
                    resources = self._select_statefulset(client=apps)
                case "DaemonSet":
                    resources = self._select_daemonset(client=apps)
                case "Job":
                    resources = self._select_job(client=batch)
                case "HorizontalPodAutoscaler":
                    resources = self._select_horizontal_pod_autoscaler(client=autoscaling)
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

    def _select_pod_template(self, client: client.CoreV1Api) -> V1PodTemplateList:
        match self.client.namespace:
            case "*":
                return client.list_pod_template_for_all_namespaces()
            case _:
                return client.list_namespaced_pod_template(namespace=self.client.namespace)

    def _select_replication_controller(self, client: client.CoreV1Api) -> V1ReplicationControllerList:
        match self.client.namespace:
            case "*":
                return client.list_replication_controller_for_all_namespaces()
            case _:
                return client.list_namespaced_replication_controller(namespace=self.client.namespace)

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

    def _select_horizontal_pod_autoscaler(self, client: client.AutoscalingV1Api) -> V1HorizontalPodAutoscalerList:
        match self.client.namespace:
            case "*":
                return client.list_horizontal_pod_autoscaler_for_all_namespaces()
            case _:
                return client.list_namespaced_horizontal_pod_autoscaler(namespace=self.client.namespace)
