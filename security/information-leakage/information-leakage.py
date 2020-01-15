#!/usr/bin/env python3

import json
import sys
import time

import requests

from requests.exceptions import RequestException
from urllib.parse import urljoin

def main():
    with open('../../HOSTS_URL') as f:
        hosts_url = f.read().strip()

    try:
        res = requests.get(hosts_url)
    except RequestException as e:
        print(e, file=sys.stderr)
        return

    hosts = res.json()

    for host in hosts:
        url_404 = urljoin(host, '01189998819991197253')
        try:
            res = requests.get(url_404)
        except RequestException as e:
            print('ERROR {}: '.format(url_404, e), file=sys.stderr)
            continue

        print('{}: Server {}'.format(host, res.headers['Server']))

if __name__ == '__main__':
    while True:
        main()

        time.sleep(60)
