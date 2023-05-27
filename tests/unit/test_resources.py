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
# def test_select_pod():
#    client = Client(
#        contexts=["cluster1"], namespace="default", attributes=["metadata.name", "metadata.labels"], filters={}
#    )
#    wl = Workload(client)
#
#    pods = wl.select("Pod")
#    assert len(pods) == 1
#
