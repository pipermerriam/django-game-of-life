import datetime

from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import QuerySet


class Timestampable(models.Model):
    """
    Clone of TimeStampable model from django-fusionbox but which extends from
    the GeoDjango model instead.
    """
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class QuerySetManager(models.GeoManager):
    """
    Clone of QuerySetManager from django-fusionbox that extends from the
    GeoDjango `GeoManager` model.
    """
    use_for_related_fields = True

    def get_query_set(self):
        return self.model.QuerySet(self.model)

    def __getattr__(self, attr, *args):
        if attr.startswith('__') or attr == 'delete':
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)


class Queryable(models.Model):
    """
    Object which merges all parent inner QuerySet classes.  Clone of
    ManagedQuerySet behavior from django-fusionbox with a better name and for
    GeoDjango models.
    """
    objects = QuerySetManager()

    class Meta:
        abstract = True

    class QuerySet(QuerySet):
        pass

    def __new__(cls, name, bases, attrs):
        # Merge the base class QuerySet classes to a single class
        querysets = [attrs.get('QuerySet', False)] + [getattr(base, 'QuerySet', False) for base in bases]
        querysets = filter(bool, querysets)
        if querysets:
            attrs['QuerySet'] = type('QuerySet', tuple(querysets), {})

        # Return the super call to __new__ to models.Model
        return super(Queryable, cls).__new__(cls, name, bases, attrs)
