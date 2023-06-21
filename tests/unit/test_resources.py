#
# def test_get_attr():
#    content = yaml.load(open("tests/assets/core-pod.yaml"), Loader=yaml.FullLoader)
#    V1PodSpec(content["spec"]).containers
#
#    deployment = V1Pod(spec=V1PodSpec(content["spec"]), metadata=content["metadata"])
#
#    label = rgetattr(deployment, "metadata.labels.app")
#    assert label == "nginx"
#
#
from kubequery.client import Client
from kubequery.kubernetes.resources.workload import Workload

class TestWorkload():

    @staticmethod
    def test_select_pod():
        client = Client(
            contexts=["cluster1"], namespace="rand", attributes=["metadata.name", "metadata.labels"], filters={}
        )
        wl = Workload(client)

        pods = wl.select("V1Pod")
        print(pods[0].values)
        assert len(pods) == 1

    @staticmethod
    def test_select_deployment():
        client = Client(
            contexts=["cluster1"], namespace="default", attributes=["metadata.name", "metadata.labels"], filters={}
        )
        wl = Workload(client)

        deployments = wl.select("deployment")
        print(deployments[0].values)
        assert 4 == 4