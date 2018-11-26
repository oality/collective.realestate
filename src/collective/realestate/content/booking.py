# -*- coding: utf-8 -*-
from collective.realestate import _
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IBooking(model.Schema):
    """ Marker interface for Booking
    """
    start = schema.Date(
        title=_(u'Start of booking'),
        required=True
    )

    end = schema.Date(
        title=_(u'End of booking'),
        required=True
    )


@implementer(IBooking)
class Booking(Item):
    """
    """
