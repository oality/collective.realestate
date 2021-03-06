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
class RealEstateFor(object):
    """
    """

    def __call__(self, context):
        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]
        terms = []
        terms.append(
            SimpleTerm(value='sale', token='sale', title=_(u'Sale')))
        terms.append(
            SimpleTerm(value='rent', token='rent', title=_(u'Rent')))
        return SimpleVocabulary(terms)


RealEstateForFactory = RealEstateFor()
