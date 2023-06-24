from typing import Any

import kubequery.exceptions as exceptions


class Model:
    def __init__(self, context, resource: str, values: dict[str, list[Any]]):
        self.context = context
        self.resource_type = resource

        #    {
        #        "metadata.labels": ["app=nginx", "app=demo"],
        #        "metadata.name": ["demo", "nginx"],
        #    }
        self.values = values

    def __eq__(self, model: object) -> bool:
        if not isinstance(model, Model):
            raise exceptions.InvalidObject(model)

        return self.values == model.values

    def __setitem__(self, key: str, value: Any) -> None:
        self.values[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.values[key]

    def insert(self, key: str, value: Any) -> None:
        if key not in self.values.keys():
            self.values[key] = []
        self.values[key].append(value)

    def __str__(self) -> str:
        return {
            "context": self.context,
            "resource_type": self.resource_type,
            "values": self.values,
        }
