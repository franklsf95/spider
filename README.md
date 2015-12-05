# LinkedIn Extraction Project

- Crawler
- Parser
- Analyzer

## Objective

- Loose Coupling - easy to develop/maintain/operate
- Scalable - can run in multiple threads/processes/hosts

## Crawler

- Acts as a user clicking on browser, saving HTML pages to disk
- Input: a recruiter account
- Output: a list of pre-processed HTML pages (~100KB per page)
  - Only saves `<body>`
  - Sanitize `<script>`
- Libraries: `scrapy`,  `lxml`

## Parser

- Input: the pre-processed HTML pages
- Output: entries in a relational database

### Database Structure

- Engine: SQLite/MySQL/… (can also do NoSQL databases)
- Tables:
  - Main "persons" table: `people`
  - "Objects" table: `schools`, `companies`, etc.
  - "Relationships" table: `people_schools` for storing relationships.
- `People` table columns:
  - `id` (index)
  - `url`
  - `name`
  - Other simple attributes (`summary`, etc)
- `Schools` table columns:
  - `id` (index)
  - `name`
  - `location`
  - `p_tier` (maybe? `p_` prefix indicates that this is not from LinkedIn)
- `People_schools` table columns:
  - `id` (index)
  - `person_id` foreign key to `people`
  - `school_id` foreign key to `schools`
  - `start_date`
  - `end_date`
- Reference: http://www.w3schools.com/sql/sql_foreignkey.asp
- Advantage of this design
  - Easy scaling - multiple schools for a person
  - Easy querying - people going to UChicago? `SELECT person_id FROM people_schools WHERE school_id = (?)`
  - Endorsed by **Object-relational Mappers**. (I've used ActiveRecord in Ruby on Rails, SQLAlchemy available for Python)
  - Easily exportable to Stata, etc.

## Analyzer

- Python ORM
- Stata/R/...

## Amount of Work

- Basic crawler: 10 hours
- Extended crawler (multithreading, etc.): 10 hours
- Database ORM infrastructure: 10 hours
- Parser: > 10 hours (need to figure out the complex HTML tree)

## My Schedule

- 10 hours / week
  
  ​