#!/usr/bin/env python

import ast
from bs4 import BeautifulSoup
import dateutil.parser
from db.driver import prepare_db_session
from db.models import *
import json
import logging
import os

# Set up logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def extract_person_overview(session, s):
    """
    Extracts a person's overview information from HTML.
    :param session: an active SQLAlchemy session
    :param s: parsed BeautifulSoup object
    :return: a Person object
    """
    person = Person()
    sec = s.find(id='topcard')
    # Get the name
    name_tag = sec.find(id='name')
    person.name = name_tag.text.strip()
    # Get the headline
    headline_tag = sec.find(class_='headline')
    person.headline = headline_tag.text.strip()
    # Get the locality
    dm = sec.find(id='demographics')
    locality_tag = dm.find(class_='locality')
    person.locality = locality_tag.text.strip()
    # Done.
    print(person)
    print('------------')
    session.add(person)
    return person


def extract_person_experiences(session, person, s):
    """
    Extracts a person's experiences information from HTML.
    :param session: an active SQLAlchemy session
    :param person: a Person object
    :param s: parsed BeautifulSoup object
    :return: None
    """
    sec = s.find(id='experience')
    items = sec.find_all('li', class_='position')
    for li in items:
        # Create a position object
        position = Position()
        position.person = person
        # Get title
        title = extract_position_title(session, li)
        position.title = title
        # Get company

        # Get date range
        start, end = extract_position_date_range(session, li)
        position.start_date = start
        position.end_date = end
        # Done.
        session.add(position)


def extract_position_title(session, li):
    """
    Find or create a title from given HTML element.
    :param session: an active SQLAlchemy session
    :param li: parsed BeautifulSoup object
    :return: a Title object
    """
    h4 = li.find('h4', class_='item-title')
    a = h4.find('a')
    name = a.text.strip()
    url = a['href']
    # Trim URL
    domain = 'linkedin.com'
    i = url.find(domain)
    if i != -1:
        end = i + len(domain)
        url = url[end:]
    i = url.find('?')
    if i != -1:
        url = url[:i]

    # Find or create title
    title = Title.get_or_create(session, name=name, url=url)
    return title


def extract_position_date_range(session, li):
    """
    Extract the start date and end date from given HTML element.
    :param session:
    :param li:
    :return: (date, date), date can be None
    """
    s = li.find(class_='date-range')
    times = s.find_all('time')

    def parse_date(i):
        if len(times) <= i:
            return None
        t = times[i].text.strip()
        return dateutil.parser.parse(t)

    start = parse_date(0)
    end = parse_date(1)
    return start, end


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
    file_path = os.path.join(root_path, file_name)
    with open(file_path) as file:
        content = file.read()

    soup = BeautifulSoup(content, 'lxml')

    # 1. Get person's basic information

    try:
        person = extract_person_overview(session, soup)
    except TypeError:
        log.error('TypeError')

    # Add metadata to the person
    meta = {'url': url, 'file_name': file_name}
    person.meta = json.dumps(meta, separators=(',', ':'))

    # 2. Get experiences list

    extract_person_experiences(session, person, soup)

    # X. Commit changes

    session.commit()

    print('-----------query')
    print(session.query(Person).count())

    raise ValueError


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
