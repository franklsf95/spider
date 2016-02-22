#!/usr/bin/env python

import ast
import csv
import logging
import os
import re

# Set up logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def make_filename(title):
    """
    Translate title into a valid filename
    :param title: str
    :return: str
    """
    MAX_LEN = 60
    cleaned = str.replace(title, '/', '-')
    truncated = cleaned[:MAX_LEN]
    with_ext = "{}.html".format(truncated)
    return with_ext


def find_company_id(file_path):
    """
    Extract the company ID from the HTML file specified
    :param file_path: str
    :return: an ID string, or None
    """
    try:
        with open(file_path) as file:
            html = file.read()
            r = re.search('\?companyId=(\d*)&amp;', html)
            if r is None:
                return None
            id_str = r.group(1)
            return id_str
    except FileNotFoundError:
        log.error("File not found: {}".format(file_path))
        return None


def process_all(items):
    """
    Process all results from their local copies
    :param items: list of triplets
    :return: results: list of tuples
    """
    root_path = '../tmp/companies/'

    results = []
    for i, triplet in enumerate(items):
        seq = i + 1
        if triplet is None:
            results.append((seq, None, None))
            continue
        conf, title, url = triplet
        if conf < 40:
            log.warning("Skipping {}".format(url))
            results.append((seq, None, None))
            continue

        file_path = os.path.join(root_path, make_filename(title))
        result = find_company_id(file_path)

        suffix = ' | LinkedIn'
        name = title.split(suffix)[0]
        results.append((seq, name, result))

    return results



def main():
    """
    Driver method.
    """
    file_path = '../tmp/company_links.py'
    with open(file_path) as file:
        content = file.read()
        items = ast.literal_eval(content)

    results = process_all(items)

    out_path = '../tmp/company_ids.csv'
    with open(out_path, 'w+') as file:
        writer = csv.writer(file)
        for row in results:
            writer.writerow(list(row))

if __name__ == '__main__':
    main()
