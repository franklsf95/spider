#!/usr/bin/env python

import ast
import logging
import os
import requests

# Set up logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/'
              '537.36 (KHTML, like Gecko) Chrome/49.0.2593.0 Safari/537.36'
              )


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


def download(url, file_path, overwrite=False):
    """
    Downloads the content of <url> to <file_path>.
    :param url: url to download
    :param file_path: file to save to
    :param overwrite: whether to overwrite existing files
    :return: None
    """
    if not overwrite:
        if os.path.isfile(file_path):
            log.error("File exists: {}. Abort.".format(file_path))
            return
    # Fake browser visit
    headers = {'User-Agent': USER_AGENT}
    resp = requests.get(url, headers=headers)
    with open(file_path, 'wb+') as file:
        for chunk in resp.iter_content():
            file.write(chunk)
        log.info("Successfully saved {}.".format(url))


def download_all(results, offset=0):
    """
    Download all results to local files
    :param results: list of triplets
    :param offset: int
    :return: None
    """
    root_path = '../tmp/companies/'
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    for triplet in results[offset:]:
        if triplet is None:
            continue
        conf, title, url = triplet
        file_path = os.path.join(root_path, make_filename(title))
        download(url, file_path)


def main():
    """
    Driver method.
    """
    file_path = '../tmp/company_links.py'
    with open(file_path) as file:
        content = file.read()
        people = ast.literal_eval(content)
    download_all(people)


if __name__ == '__main__':
    main()
