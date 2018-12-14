# -*- coding: utf-8 -*-
""" Widget interfaces and schema
"""
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets.interfaces import CountableSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IIntselectSchema(ISchema):
    """ Schema
    """
    text = schema.TextLine(
        title=_(u'Text to display after number'),
        description=_(u'Text to display after number in select box'),
        required=False
    )

    title2 = schema.TextLine(
        title=_(u'Default input text'),
        description=_(u'Default text to display in select box'),
        required=False
    )

    sortreversed = schema.Bool(
        title=_(u'Reverse options'),
        description=_(u'Sort options reversed'),
        required=False
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IIntselectSchema).select(
        u'title',
        u'title2',
        u'index',
        u'text',
        u'default'
    )


class DisplaySchemata(FacetedSchemata):
    """ Schemata display
    """
    label = u'display'
    fields = field.Fields(IIntselectSchema).select(
        u'sortreversed',
    )


__all__ = [
    IIntselectSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    CountableSchemata.__name__,
    DisplaySchemata.__name__,
]
