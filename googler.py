#!/usr/bin/env python

import json
import logging
import pprint
import re
import requests
from sys import stderr

# logging.basicConfig(level=logging.DEBUG)


def searchGoogle(query, domain):
    """
    :param query: string
    :param domain: the domain name for the URL we are searching in
    :rtype: a Python object returned by JSON parser
    """
    url = 'https://ajax.googleapis.com/ajax/services/search/web'
    params = {'v': '1.0',
              'q': '{0} site:{1}'.format(query, domain)}
    resp = requests.get(url, params)
    data = json.loads(resp.text)
    return data


def findResult(json, domain):
    """
    :param json: JSON data
    :param domain: the domain name for the URL we are looking for
    :rtype: String or None
    """
    try:
        results = json['responseData']['results']
        pattern = '.*{0}.*'.format(domain)
        regex = re.compile(pattern)
        for result in results:
            url = result['url']
            if not regex.match(url) is None:
                return url
    except KeyError:
        print('Bad response from Google.', file=stderr)
        return None
    return None


def main():
    """
    Driver method.

    :rtype: NoneType
    """
    domain = 'linkedin.com'
    people = ['Frank Luan', 'Mutian Liu', 'Wenxuan Liu', 'Zhen Lin']
    for q in people:
        json = searchGoogle(q, domain)
        url = findResult(json, domain)
        print(url)

if __name__ == '__main__':
    main()

