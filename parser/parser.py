#!/usr/bin/env python

import ast
from bs4 import BeautifulSoup
from db.driver import prepare_db_session
from db.models import Person, Position
import json
import logging
import os

# Set up logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def extract_person_overview(person, s):
    """
    Extracts a person's overview information from HTML.
    :param person: a Person object
    :param s: parsed BeautifulSoup object
    :return: None
    """
    ov = s.find(class_='profile-overview-content')
    # Get the name
    name_tag = ov.find(id='name')
    person.name = name_tag.text.strip()
    # Get the headline
    headline_tag = ov.find(class_='headline')
    person.headline = headline_tag.text.strip()
    # Get the locality
    dm = ov.find(id='demographics')
    locality_tag = dm.find(class_='locality')
    person.locality = locality_tag.text.strip()
    # Done.


def parse(title, url, session):
    """
    Parses LinkedIn content and insert into database.
    :param title: title of the LinkedIn page
    :param url: LinkedIn URL
    :param session: SQLAlchemy session
    :return: None
    """
    root_path = '../data/clean_profiles/'
    file_name = "{}.html".format(title)
    file_path = os.path.join(root_path, file_name)
    with open(file_path) as file:
        content = file.read()

    soup = BeautifulSoup(content)

    # 1. Get basic information

    person = Person()
    try:
        extract_person_overview(person, soup)
    except TypeError:
        log.error('TypeError')

    # Add metadata to the person
    meta = {'url': url, 'file_name': file_name}
    person.meta = json.dumps(meta, separators=(',', ':'))

    # 2. Get what?

    # X. Commit changes

    session.add(person)
    session.commit()

    raise ValueError


def parse_all(results, session):
    """
    :param results: list of triplets
    :param session: SQLAlchemy session
    :return: None
    """
    for triplet in results:
        if triplet is None:
            continue
        _, title, url = triplet
        parse(title, url, session)


def main():
    """
    Driver method.
    """
    file_path = '../data/results.py'
    with open(file_path) as file:
        content = file.read()
        people = ast.literal_eval(content)

    session = prepare_db_session()
    parse_all(people, session)


if __name__ == '__main__':
    main()
