#!/usr/bin/env python3

import sys
import time

import requests

from requests.exceptions import RequestException
from urllib.parse import urljoin

def main():
    try:
        # res = requests.get(host_url, params={'s': thing})
        pass
    except RequestException as e:
        print(e, file=sys.stderr)
        return

    hosts = [
        'https://developers.italia.it',
        'https://docs.italia.it',
        'https://designers.italia.it',
        'https://innovazione.gov.it'
    ]
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
