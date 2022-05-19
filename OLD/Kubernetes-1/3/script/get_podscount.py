#!/usr/bin/env python3.9
from  kubernetes import client , config
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily, CounterMetricFamily, REGISTRY

import time

class CustomCollector():
    
    def collect(self):
        config.load_incluster_config()
        v1 = client.CoreV1Api()
        ret_pod = v1.list_namespaced_pod("default", watch=False)
        value = GaugeMetricFamily("node_kuber_pods", 'running pods count', labels='value')
        value.add_metric(["pods_count"], len(ret_pod.items))
        yield value


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(5)
