# -*- coding: utf-8 -*-
"""
@author: Vault-of-Procrastination
"""

# In[0]

from time import sleep
from re import findall, M
from itertools import groupby
from operator import itemgetter
from grpc import insecure_channel, Channel
from requests import Session, ConnectionError

# In[1]

def search_servers(servers: list[str], retries: int = 10, delay: float = 0.3) -> Channel:
    session, metrics = Session(), {}
    regex = r'^(?P<metric>[a-z0-9_]*)(?:\s?\{(?P<fields>[A-Za-z0-9,.="]+)\})?\s(?P<value>[\d.]+)$'
    for host in servers:
        try:
            for i in range(retries):
                try:
                    response = session.get(f'http://{host}/metrics')
                    if not response.status_code == 200:
                        continue
                    host_metrics = {x: sum(list(map(itemgetter(1), y))) for x, y in groupby([[x, float(z)] for x, y, z in findall(regex, response.text, M)], itemgetter(0))}
                    if host_metrics['requests'] == host_metrics['threads_count']:
                        raise ValueError
                    metrics[host] = host_metrics
                    break
                except ConnectionError:
                    pass
                sleep(delay)
        except ValueError:
            continue
    if len(metrics) == 0:
        raise ValueError('There is no server to connect')
    min_conn = min([x['requests'] for x in metrics.values()])
    metrics = {k:v for k, v in metrics.items() if v['requests'] == min_conn}
    if len(metrics) > 1:
        max_weight = max([x['weight'] for x in metrics.values()])
        metrics = {k:v for k, v in metrics.items() if v['weight'] == max_weight}
    server = sorted(list(metrics.keys()))[0]
    return insecure_channel(server)


