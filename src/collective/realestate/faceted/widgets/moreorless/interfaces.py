# -*- coding: utf-8 -*-
""" Widget interfaces and schema
"""
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from zope import schema
from z3c.form import field
from zope.schema.vocabulary import SimpleVocabulary


class IMoreOrLessSchema(ISchema):
    """ Schema
    """

    index = schema.Choice(
        title=_(u"Catalog index"),
        description=_(u"Catalog index to use for search"),
        vocabulary=u"eea.faceted.vocabularies.TextCatalogIndexes",
        required=True,
    )

    moreorless = schema.Choice(
        title=_(u"More or less"),
        description=_(u"More or less than field value"),
        vocabulary=SimpleVocabulary.fromValues([u"more", u"less"]),
        required=True,
    )


class DefaultSchemata(DS):
    """ Schemata default
    """

    fields = field.Fields(IMoreOrLessSchema).select(
        u"title", u"moreorless", u"default", u"index"
    )


__all__ = [
    IMoreOrLessSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
