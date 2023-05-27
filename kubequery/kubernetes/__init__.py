import itertools

from .resources import Workload

__workload_resources__ = [x.__class__.__name__ for x in Workload.supported]

__service_resources__ = [
    "Service",
    "Endpoints",
    "EndpointSlice",
    "Ingress",
    "IngressClass",
]

__config_and_storage_resources__ = [
    "ConfigMap",
    "Secret",
    "Volume",
    "PersistentVolumeClaim",
    "PersistentVolume",
    "StorageClass",
    "VolumeAttachment",
    "CSIDriver",
    "CSINode",
    "CSIStorageCapacity",
]

__authentication_resources__ = [
    "ServiceAccount",
    "TokenRequest",
    "TokenReview",
    "CertificateSigningRequest",
    "ClusterTrustBundle",
    "SelfSubjectReview",
]

__authorization_resources__ = [
    "LocalSubjectAccessReview",
    "SelfSubjectAccessReview",
    "SelfSubjectRulesReview",
    "SubjectAccessReview",
    "SelfSubjectReview",
    "ClusterRole",
    "ClusterRoleBinding",
    "Role",
    "RoleBinding",
]

__policy_resources__ = [
    "LimitRange",
    "ResourceQuota",
    "NetworkPolicy",
    "PodDisruptionBudget",
    "IPAddress",
]

__supported_resources__ = {
    "Workload": __workload_resources__,
    "Service": __service_resources__,
    "ConfigAndStorage": __config_and_storage_resources__,
    "Authentication": __authentication_resources__,
    "Authorization": __authorization_resources__,
    "Policy": __policy_resources__,
}

__all_resources__ = list(itertools.chain(*__supported_resources__.values()))
