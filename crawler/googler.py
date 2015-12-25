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


def search_google(keyword, site, start=0):
    """
    Run a google search with given parameters and return the JSON result
    :param keyword: string
    :param site: the domain name for the URL we are searching in
    :param start: offset for search result
    :return: a Python object returned by JSON parser
    """
    log.info('Searching Google with keyword={}, site={}, start={}'.format(
            keyword, site, start))
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {'key': GOOGLE_API_KEY,
              'cx': GOOGLE_CSE_ID,
              'q': '{0} site:{1}'.format(keyword, site)}
    if start > 0:
        params['start'] = start
    resp = requests.get(url, params)
    data = json.loads(resp.text)
    return data


def find_linkedin_url(name, items):
    """
    :param name: the name of the person
    :param items: a list of search result items
    :return: (str, str) or None
    """
    site = 'linkedin.com'
    candidates = []

    # Step 1: Filter candidates

    for item in items:
        if not item['kind'] == 'customsearch#result':
            log.warn('Google returned result of different kind: {}'.format(
                    item['kind']))
            continue
        url = item['link']
        title = item['title'].lower()
        if not re.search(site, url):
            log.debug('Not from LinkedIn: {0}'.format(url))
            continue
        # White list - confidence level 10
        if re.search('/in/', url) or \
                (re.search('/pub/', url) and not re.search('/pub/dir/', url)):
            log.debug('Profile detected - confidence 10')
            c = (10, item)
            candidates.append(c)
            continue
        # Black list
        if re.search('/pub/dir/', url) or re.search('/title/', url):
            log.debug('Not personal profile: {0}'.format(url))
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
        for i, pair in enumerate(candidates):
            conf, item = pair
            if re.search(part, item['title']):
                # Add confidence if we find part of the name
                conf += 20
                candidates[i] = (conf, item)

    # Step 3: Choose the best result

    best = max(candidates, key=lambda x: x[0])
    if best is None:
        return None
    else:
        conf, item = best
        return conf, item['title'], item['link']


def get_linkedin_url(triplet):
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
        result = search_google(keyword, site, start=offset)
        try:
            items = result['items']
        except (TypeError, KeyError):
            log.error('Bad response from Google: {0}'.format(result))
            return None
        offset += len(items)
        result = find_linkedin_url(name, items)
        if result is not None:
            return result
    return None


def read_people(file_path, limit):
    """
    Read the names and education of people from the given CSV file.
    :param file_path: string
    :param limit: int
    :return: a list of strings as search keywords.
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
    """
    people = read_people('../input/people.csv', limit=10)
    pprint.pprint(people)

    results = []
    for p in people:
        result = get_linkedin_url(p)
        results.append(result)
    pprint.pprint(results)

if __name__ == '__main__':
    main()
