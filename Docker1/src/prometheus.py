from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily, CounterMetricFamily, REGISTRY

import random
import time
import re
import os

class CustomCollector():
    
    def collect(self):
        with open("/result/result.txt") as f:
            result = f.readlines()[-1]
            #print(result)
        result_list = result.split()
        try:
            _bytes = float(result_list[0])/1000000
            _speed = float(result_list[-2])
            if result_list[-1] == 'kB/s':
                _speed /= 1000
        except Exception:
            _bytes = -1
            _speed = -1

        value = GaugeMetricFamily("DD_RESULT", 'result of dd operation', labels='value')
        value.add_metric(["copied"], _bytes)
        value.add_metric(["speed"], _speed)
        yield value


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(5)
