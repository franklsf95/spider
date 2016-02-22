#!/usr/bin/env python

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper


class RepresentableBase(object):
    """
    This class can be used by ``declarative_base``, to add an automatic
    ``__repr__`` method to *all* subclasses of ``Base``. This ``__repr__`` will
    represent values as:
        ClassName(pkey_1=value_1, pkey_2=value_2, ..., pkey_n=value_n)
    where ``pkey_1..pkey_n`` are the primary key columns of the mapped table
    with the corresponding values.
    """

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        mapper = object_mapper(self)
        items = [(p.key, getattr(self, p.key))
                 for p in [mapper.get_property_by_column(c)
                           for c in mapper.primary_key]]
        return "{0}({1})".format(
            self.__class__.__name__,
            ', '.join(['{0}={1!r}'.format(*_) for _ in items]))

    @classmethod
    def get_or_create(cls, session, **kwargs):
        instance = session.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = cls(**kwargs)
            session.add(instance)
            return instance

    # Pre-defined VARCHAR fields
    ShortString = String(255)
    String = String(2048)


Base = declarative_base(cls=RepresentableBase)
