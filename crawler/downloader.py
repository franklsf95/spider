import ast
import logging
import os
import requests

# Set up logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


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
    resp = requests.get(url)
    with open(file_path, 'w+') as file:
        file.write(resp.text)
        log.info("Successfully saved {}.".format(url))


def download_all(results):
    """
    Download all results to local files
    :param results: list of triplets
    :return: None
    """
    root_path = './profiles/'
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    for triplet in results:
        if triplet is None:
            continue
        conf, title, url = triplet
        file_path = os.path.join(root_path, "{}.html".format(title))
        download(url, file_path)


def main():
    """
    Driver method.
    """
    results = []
    file_path = './results.py'
    with open(file_path) as file:
        content = file.read()
        results = ast.literal_eval(content)
    download_all(results)


if __name__ == '__main__':
    main()
