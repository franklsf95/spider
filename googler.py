#!/usr/bin/env python

import csv
import json
import logging
import os
import pprint
import re
import requests

# Retrieve API Keys

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')

# Set up logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def searchGoogle(keyword, site, start=0):
    """
    Run a google search with given parameters and return the JSON result

    :param query: string
    :param domain: the domain name for the URL we are searching in
    :rtype: a Python object returned by JSON parser
    """
    log.info('Searching Google with keyword={0}, site={1}, start={2}'.format(keyword, site, start))
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {'key': GOOGLE_API_KEY,
              'cx': GOOGLE_CSE_ID,
              'q': '{0} site:{1}'.format(keyword, site)}
    if start > 0:
        params['start'] = start
    resp = requests.get(url, params)
    data = json.loads(resp.text)
    return data


def findLinkedInURL(name, items):
    """
    :param name: the name of the person
    :param items: a list of search result items
    :rtype: (str, str) or None
    """
    site = 'linkedin.com'
    candidates = []

    # Step 1: Filter candidates

    for item in items:
        if not item['kind'] == 'customsearch#result':
            log.warn('Google returned result of different kind: {0}'.format(item['kind']))
            continue
        link = item['link']
        title = item['title'].lower()
        if not re.search(site, link):
            log.debug('Not from LinkedIn: {0}'.format(link))
            continue
        # Whitelist - confidence level 10
        if re.search('/in/', link) \
                or (re.search('/pub/', link) and not re.search('/pub/dir/', link)):
            log.debug('Profile detected - confidence 10')
            c = (10, item)
            candidates.append(c)
            continue
        # Blacklist
        if re.search('/pub/dir/', link) or re.search('/title/', link):
            log.debug('Not personal profile: {0}'.format(link))
            continue
        if re.search('top', title) or re.search('profiles', title):
            log.debug('Not personal profile: {0}'.format(title))
            continue
        # Passed blacklist - confidence level 5
        log.debug('Profile detected - confidence 5')
        c = (5, item)
        candidates.append(c)
        continue

    # Step 2: Match names
    names = name.split(' ')
    for part in names:
        # First name or last name
        for i, cand in enumerate(candidates):
            conf, item = cand
            if re.search(part, item['title']):
                # Add confidence if we find part of the name
                conf += 20
                candidates[i] = (conf, item)

    # Step 3: Choose the best result

    best = max(candidates, key=lambda c: c[0])
    if best is None:
        return None
    else:
        conf, item = best
        return conf, item['title'], item['link']


def getLinkedInURL(triplet):
    """
    Search Google to get the LinkedIn URL of the given person

    :param triplet: a tuple of strings: (name, location, title)
    :return: (str, str) or None
    """
    site = 'linkedin.com'
    offset = 0
    search_limit = 30  # Limit of results returned by Google

    keyword = ' '.join(triplet)
    name = triplet[0]
    while offset < search_limit:
        json = searchGoogle(keyword, site, start=offset)
        try:
            items = json['items']
        except (TypeError, KeyError):
            log.error('Bad response from Google: {0}'.format(json))
            return None
        offset += len(items)
        result = findLinkedInURL(name, items)
        if not result is None:
            return result
    return None


def readPeople(file_path, limit):
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
            triplet = [s.strip() for s in row[1:4]]  # name, location, title
            ret.append(triplet)
            cnt += 1
            if cnt >= limit:
                break
    return ret


def main():
    """
    Driver method.

    :rtype: NoneType
    """
    people = readPeople('data/people.csv', limit=10)
    pprint.pprint(people)

    results = []
    for p in people:
        result = getLinkedInURL(p)
        results.append(result)
    pprint.pprint(results)

if __name__ == '__main__':
    main()
