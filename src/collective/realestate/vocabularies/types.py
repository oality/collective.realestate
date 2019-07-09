# -*- coding: utf-8 -*-

# from plone import api
from collective.realestate import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class RealEstateTypes(object):
    """
    """

    def __call__(self, context):
        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        terms = []
        types = {
            "appart": _(u"Apartment"),
            "house": _(u"House / Villa"),
            "garage": _(u"Garage"),
            "lots": _(u"Lots / Land"),
            "businesses": _(u"Businesses"),
        }
        for id, item in types.items():
            terms.append(SimpleTerm(value=id, token=id, title=item))
        return SimpleVocabulary(terms)


RealEstateTypesFactory = RealEstateTypes()
