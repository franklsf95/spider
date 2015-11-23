#!/usr/bin/env python

import csv
import json
import logging
import pprint
import re
import requests
from sys import stderr

logging.basicConfig(level=logging.DEBUG)


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


def readPeople(file_path, limit=5):
    """
    Read the names and education of people from the given CSV file.
    :param file_path: string
    :param limit: int
    :rtype: a list of strings as search keywords.
    """
    ret = []
    with open(file_path) as file:
        reader = csv.reader(file)
        _ = next(reader)  # Skip the headers
        cnt = 0
        for row in reader:
            info = row[1:4]  # name, location, title
            keyword = '  '.join(info)
            ret.append(keyword)

            cnt += 1
            if cnt >= limit:
                break
    return ret


def main():
    """
    Driver method.

    :rtype: NoneType
    """
    people = readPeople('data/people.csv')
    pprint.pprint(people)


    domain = 'linkedin.com'
    for q in people:
        json = searchGoogle(q, domain)
        url = findResult(json, domain)
        print(url)

if __name__ == '__main__':
    main()

