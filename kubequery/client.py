class Client:
    def __init__(self, contexts: list[str], attributes: list[str], filters: dict[str, str], namespace: str = "default"):
        self.contexts = contexts
        self.namespace = namespace
        self.attributes = attributes
        self.filters = filters
