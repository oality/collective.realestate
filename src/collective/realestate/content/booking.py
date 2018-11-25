# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IBooking(model.Schema):
    """ Marker interface for Booking
    """


@implementer(IBooking)
class Booking(Item):
    """
    """
