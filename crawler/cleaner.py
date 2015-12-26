#!/usr/bin/env python

from bs4 import BeautifulSoup
from glob import glob
import logging
import os

# Set up logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def clean_up(content):
    """
    Trims the HTML for only useful information
    :param content: input HTML string
    :return: a string
    """
    soup = BeautifulSoup(content, 'lxml')
    sub_soup = soup.find(id='profile')
    # Remove code and scripts
    for tag in ['code', 'script']:
        for s in sub_soup.find_all(tag):
            s.decompose()

    # Return result
    result = sub_soup.prettify()
    return result


def main():
    """
    Driver method.
    """
    root_path = '../tmp/clean_profiles/'
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    files = glob('../tmp/profiles/*.html')
    for file_path in files:
        with open(file_path, 'r') as file:
            content = file.read()
        content = clean_up(content)

        file_name = os.path.basename(file_path)
        output_path = os.path.join(root_path, file_name)
        with open(output_path, 'w') as file:
            file.write(content)
        log.info("Cleaned up {}.".format(file_path))


if __name__ == '__main__':
    main()
