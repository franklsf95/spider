#!/usr/bin/env python
# Search Google for LinkedIn URL of company pages

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
        if re.search('/company/', url):
            log.debug('Company detected - confidence 10')
            c = (40, item)
            candidates.append(c)
            continue
        # Black list
        if re.search('/jobs/', url) or re.search('/title/', url):
            log.debug('Not company profile: {0}'.format(url))
            continue
        # Passed blacklist - confidence level 5
        log.debug('Potential company detected - confidence 5')
        c = (5, item)
        candidates.append(c)
        continue

    # Step 2: Match names

    # First name or last name
    for i, pair in enumerate(candidates):
        conf, item = pair
        if re.search(name, item['title'], re.IGNORECASE):
            # Add confidence if we find part of the name
            conf += 10
            candidates[i] = (conf, item)

    # Step 3: Choose the best result

    if len(candidates) == 0:
        return None
    best = max(candidates, key=lambda x: x[0])
    conf, item = best
    return conf, item['title'], item['link']


def get_linkedin_url(name):
    """
    Search Google to get the LinkedIn URL of the given person
    :param name: str
    :return: (str, str) or None
    """
    site = 'linkedin.com'
    offset = 0
    search_limit = 10  # Limit of results returned by Google

    keyword = name
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


def read_companies(file_path, start=0, end=None):
    """
    Read the company names from provided text file
    :param file_path: string
    :param start: int
    :param end: int or None
    :return: a list of strings as search keywords.
    """
    with open(file_path) as file:
        lines = file.readlines()
        ret = [ln.strip() for ln in lines[start:end]]
    return ret


def main():
    """
    Driver method.
    """
    companies = read_companies('../input/companies.txt', start=1001)
    pprint.pprint(companies)

    results = []
    for item in companies:
        result = get_linkedin_url(item)
        results.append(result)

    pprint.pprint(results)
    with open('../tmp/company_links.py', 'a+') as file:
        pprint.pprint(results, stream=file, width=1000)

if __name__ == '__main__':
    main()
