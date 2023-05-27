from abc import ABC, abstractmethod

from kubequery.client import Client
from kubequery.model import Model


class KubernetesResourceBase(ABC):
    @abstractmethod
    def __init__(self, client: Client):
        self.client = client

    @abstractmethod
    def select(self, workload: str) -> list[Model]:
        pass
