# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import json


class LeadimageViewlet(ViewletBase):

    def available(self):
        return False

    def index(self):
        return ''


class BookingsViewlet(ViewletBase):
    """ A viewlet which renders files """

    index = ViewPageTemplateFile('bookings.pt')

    def get_data(self):
        dates = []
        brains = api.content.find(context=self.context, portal_type='Booking')
        for brain in brains:
            obj_dates = brain.getObject().get_all_dates()
            dates += obj_dates
        # return json.dumps([date.__str__() for date in dates])
        return [date.__str__() for date in dates]


class GeneralCondViewlet(ViewletBase):

    def index(self):
        key = 'collective.realestate.condition'
        text = api.portal.get_registry_record(key)
        # import ipdb; ipdb.set_trace()
        return text if text else ''
