#!/usr/bin/env python

from bs4 import BeautifulSoup
import dateutil.parser
from db.models import *
import logging
from urllib.parse import urlparse

# Set up logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class LinkedInParser(object):
    """
    A LinkedIn HTML parser.
    """

    def __init__(self, session, html):
        """
        :param session: an active SQLAlchemy session
        :param html: string
        """
        self.session = session
        self.soup = BeautifulSoup(html, 'lxml')

    def extract_person_overview(self):
        """
        Extracts a person's overview information from HTML.
        :return: a Person object
        """
        person = Person()
        sec = self.soup.find(id='topcard')
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
        self.session.add(person)
        return person

    def extract_person_experiences(self, person):
        """
        Extracts a person's experiences information from HTML.
        :param person: a Person object
        :return: None
        """
        sec = self.soup.find(id='experience')
        items = sec.find_all('li', class_='position')
        for li in items:
            # Create a position object
            position = Position()
            position.person = person
            # Get title
            title = self._extract_li_subitem(li, Title, 'item-title')
            position.title = title
            # Get company
            company = self._extract_li_subitem(li, Company, 'item-subtitle')
            position.company = company
            # Get date range
            start, end = self._extract_date_range(li)
            position.start_date = start
            position.end_date = end
            # Get description
            position.description = self._extract_description(li)
            # Done.
            self.session.add(position)
            self.session.flush()

    def extract_person_educations(self, person):
        """
        Extracts a person's education information from HTML.
        :param person: a Person object
        :return: None
        """
        sec = self.soup.find(id='education')
        items = sec.find_all('li', class_='school')
        for li in items:
            # Create an education object
            education = Education()
            education.person = person
            # Get school
            # school = self._extract_li_subitem(li, School, 'item-title')
            # position.school = school

    def _extract_li_subitem(self, li, model, class_):
        """
        Find or create a <model> instance from given HTML element.
        :param li: HTML element
        :param model: Class of model (Title, Company)
        :param class_: CSS class
        :return: a <model> object
        """
        h = li.find(class_=class_)
        if h is None:
            return None
        a = h.find('a')
        if a is None:
            name = h.text.strip()
            url = None
        else:
            name = a.text.strip()
            url = a['href']
            url = urlparse(url).path

        # Find or create <instance>
        instance = model.get_or_create(self.session, name=name, url=url)
        return instance

    @staticmethod
    def _extract_date_range(li):
        """
        Extract the start date and end date from given HTML element.
        :param li: HTML element
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

    @staticmethod
    def _extract_description(li):
        """
        Extract the description field from given HTML element.
        :param li: HTML element
        :return: string
        """
        p = li.find(class_='description')
        if p is None:
            return None
        return p.text.strip()
