from django.contrib.gis.db import models

from fusionbox.behaviors import ManagedQuerySet


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


class Queryable(ManagedQuerySet):
    objects = QuerySetManager()

    class Meta:
        abstract = True
