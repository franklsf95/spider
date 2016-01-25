#!/usr/bin/env python

import ast
from db.driver import prepare_db_session
import json
import logging
import os
from parsing.parser import LinkedInParser

# Set up logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def parse(session, title, url):
    """
    Parses LinkedIn content and insert into database.
    :param session: an active SQLAlchemy session
    :param title: title of the LinkedIn page
    :param url: LinkedIn URL
    :return: None
    """
    root_path = '../tmp/clean_profiles/'
    file_name = "{}.html".format(title)
    # file_name = title
    file_path = os.path.join(root_path, file_name)
    with open(file_path) as file:
        content = file.read()

    p = LinkedInParser(session, content)

    # 1. Get person's basic information

    person = p.extract_person_overview()

    # Add metadata to the person
    meta = {'url': url, 'file_name': file_name}
    person.meta = json.dumps(meta, separators=(',', ':'))
    session.flush()

    # 2. Get experiences list
    p.extract_person_experiences(person)

    # 3. Get educations list
    p.extract_person_educations(person)

    # 4. Get certifications list
    p.extract_person_certifications(person)

    # 5. Get skills list
    p.extract_person_skills(person)

    # X. Commit changes

    session.commit()


def parse_all(session, results):
    """
    :param session: an active SQLAlchemy session
    :param results: list of triplets
    :return: None
    """
    for triplet in results:
        if triplet is None:
            continue
        _, title, url = triplet
        parse(session, title, url)


def main():
    """
    Driver method.
    """
    file_path = '../tmp/results.py'
    with open(file_path) as file:
        content = file.read()
        people = ast.literal_eval(content)

    session = prepare_db_session()
    parse_all(session, people)


if __name__ == '__main__':
    main()
