# -*- coding: utf-8 -*-
""" Widget interfaces and schema
"""
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IIntRangeSchema(ISchema):
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary=u'eea.faceted.vocabularies.TextCatalogIndexes',
        required=True
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IIntRangeSchema).select(
        u'title',
        u'default',
        u'index',
    )


__all__ = [
    IIntRangeSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
