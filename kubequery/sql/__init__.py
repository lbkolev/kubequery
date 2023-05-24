# "SELECT metadata.name, status.pod_ip FROM Pod WHERE namespace='kube-system' AND cluster IN ('cluster1', 'cluster2')"
# "SELECT kind, metadata FROM StatefulSet WHERE namespace='*' AND cluster='cluster1'"
# "SELECT metadata.labels FROM <CRD>"
