# -*- coding: utf-8 -*-
from collective.realestate import _
from datetime import timedelta
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IBooking(model.Schema):
    """ Marker interface for Booking
    """
    title = schema.TextLine(
        title=_(u"Customer's name"),
        required=False,
    )

    start = schema.Date(
        title=_(u'Start of booking'),
    )

    end = schema.Date(
        title=_(u'End of booking'),
    )


@implementer(IBooking)
class Booking(Item):
    """
    """

    def get_all_dates(self):
        dates = []
        curr = self.start
        while curr <= self.end:
            dates.append(curr)
            curr = curr + timedelta(days=1)
        return dates
