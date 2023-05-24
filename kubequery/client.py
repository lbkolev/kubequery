class Client:
    def __init__(self, clusters: list[str], namespace: str, attribute: str, filters: dict[str, str]):
        self.clusters = clusters
        self.namespace = namespace
        self.attribute = attribute
        self.filters = filters
