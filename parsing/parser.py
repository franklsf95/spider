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
        if name_tag is not None:
            person.name = name_tag.text.strip()
        # Get the headline
        headline_tag = sec.find(class_='headline')
        if headline_tag is not None:
            person.headline = headline_tag.text.strip()
        # Get the locality
        dm = sec.find(id='demographics')
        if dm is not None:
            locality_tag = dm.find(class_='locality')
            if locality_tag is not None:
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
        if sec is None:
            return
        items = sec.find_all('li', class_='position')
        for li in items:
            # Create a position object
            exp = PersonExperience()
            exp.person = person
            # Get title
            title = self._extract_li_subitem(li, Title, 'item-title')
            exp.title = title
            # Get company
            company = self._extract_li_subitem(li, Company, 'item-subtitle')
            exp.company = company
            # Get date range
            start, end = self._extract_date_range(li)
            exp.start_date = start
            exp.end_date = end
            # Get description
            exp.description = self._extract_description(li)
            # Done.
            self.session.add(exp)
            self.session.flush()

    def extract_person_educations(self, person):
        """
        Extracts a person's education information from HTML.
        :param person: a Person object
        :return: None
        """
        sec = self.soup.find(id='education')
        if sec is None:
            return
        items = sec.find_all('li', class_='school')
        for li in items:
            # Create an education object
            edu = PersonEducation()
            edu.person = person
            # Get school
            school = self._extract_li_subitem(li, School, 'item-title')
            edu.school = school
            # Get degree
            degree_tag = li.find(class_='item-subtitle')
            if degree_tag is not None:
                edu.degree = degree_tag.text.strip()
            # Get date range
            start, end = self._extract_date_range(li)
            edu.start_date = start
            edu.end_date = end
            # Get description
            edu.description = self._extract_description(li)
            # Done.
            self.session.add(edu)
            self.session.flush()

    def extract_person_certifications(self, person):
        """
        Extracts a person's certifications information from HTML.
        :param person: a Person object
        :return: None
        """
        sec = self.soup.find(id='certifications')
        if sec is None:
            return
        items = sec.find_all('li', class_='certification')
        for li in items:
            # Create a person-certification object
            pc = PersonCertification()
            pc.person = person
            # Get certification
            cert = self._extract_li_subitem(li, Certification, 'item-title')
            pc.certification = cert
            # Get company
            company = self._extract_li_subitem(li, Company, 'item-subtitle')
            pc.company = company
            # Get date range
            start, end = self._extract_date_range(li)
            pc.start_date = start
            pc.end_date = end
            # Get description
            pc.description = self._extract_description(li)
            # Done.
            self.session.add(pc)
            self.session.flush()

    def extract_person_skills(self, person):
        """
        Extracts a person's skills information from HTML.
        :param person: a Person object
        :return: None
        """
        sec = self.soup.find(id='skills')
        if sec is None:
            return
        items = sec.find_all('li', class_='skill')
        for li in items:
            # Create a person-skill object
            ps = PersonSkill()
            ps.person = person
            # Get skill
            skill = self._extract_li_subitem(li, Skill, None)
            ps.skill = skill
            # Done.
            self.session.add(ps)
            self.session.flush()

    def _extract_li_subitem(self, li, model, class_):
        # TODO: Account for class_='external-link'
        """
        Find or create a <model> instance from given HTML element.
        :param li: HTML element
        :param model: Class of model (Title, Company)
        :param class_: CSS class, or None for the li element itself.
        :return: a <model> object
        """
        if class_ is None:
            h = li
        else:
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
        if s is None:
            return None, None
        times = s.find_all('time')
        if times is None:
            return None, None

        def parse_date(i):
            if len(times) <= i:
                return None
            t = times[i].text.strip()
            try:
                result = dateutil.parser.parse(t)
            except ValueError as e:
                result = None
                log.error('[Date range] {}'.format(e))
            return result

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
