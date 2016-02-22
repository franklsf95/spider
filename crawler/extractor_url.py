#!/usr/bin/env python
# Extracts real LinkedIn URL from saved LinkedIn pages

import logging
import os
import pprint
import re

# Set up logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def find_url(file_path):
    """
    Extract the LinkedIn URL from the HTML file specified
    :param file_path: str
    :return: an ID string, or None
    """
    try:
        with open(file_path) as file:
            html = file.read()
            r = re.search('<A class="view-public-profile" href="(.*?)">', html)
            if r is None:
                return None
            id_str = r.group(1)
            return id_str
    except FileNotFoundError as e:
        log.error(e)
        return None


def process_all(items):
    """
    Process all results from their local copies
    :param items: list of file names
    :return: results: list of tuples
    """
    root_path = '../tmp/html/'

    results = []
    for filename in items:
        filename = filename.strip()
        file_path = os.path.join(root_path, filename)
        url = find_url(file_path)
        if url is not None:
            suffix = '  LinkedIn'
            name = filename.split(suffix)[0]
            result = (0, name, url)
            results.append(result)

    return results


def main():
    """
    Driver method.
    """
    file_path = '../tmp/html/_html_list.txt'
    with open(file_path) as file:
        items = file.readlines()

    results = process_all(items)

    pprint.pprint(results, width=100)

if __name__ == '__main__':
    main()
