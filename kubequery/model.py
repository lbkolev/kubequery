from typing import Any

import kubequery.exceptions as exceptions


class Model:
    def __init__(self, context: str, resource: str, values: dict[str, Any]):
        self.context = context
        self.resource_type = resource

        #    {
        #        "metadata.labels": ["app=nginx", "app=demo"],
        #        "name": ["demo", "nginx"],
        #    }
        self.values = values

    def __eq__(self, model: object) -> bool:
        if not isinstance(model, Model):
            raise exceptions.InvalidObject(model)

        return self.resource_type == model.resource_type

    def insert(self, key: str, value: Any) -> None:
        if key not in self.values.keys():
            self.values[key] = []
        self.values[key].append(value)
