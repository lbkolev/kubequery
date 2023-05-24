from abc import ABC, abstractmethod
from typing import Any

from kubequery.client import Client


class KubernetesResourceBase(ABC):
    @abstractmethod
    def __init__(self, client: Client):
        self.client = client

    @abstractmethod
    def select(self) -> list[dict[Any]] | None:
        pass
