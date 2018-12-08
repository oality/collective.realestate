# -*- coding: utf-8 -*-
# from collective.realestate import _
from collective.realestate.browser.controlpanel import IRealEstateSettings
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import implements


class MapsConfig(BrowserView):

    # implements(IRealEstateSettings)

    def __init__(self, context, request):
        """ init view """
        self.context = context
        self.request = request

    @property
    def marker_icons(self):
        key = 'collective.realestate.marker_icons'
        return api.portal.get_registry_record(key)

    @property
    def default_location(self):
        key_lat = 'collective.realestate.latitude'
        key_lon = 'collective.realestate.longitude'
        lat = api.portal.get_registry_record(key_lat)
        lon = api.portal.get_registry_record(key_lon)
        # import ipdb; ipdb.set_trace()
        if not lat and not lon:
            return (0.0, 0.0)
        return (lat, lon)

    @property
    def default_maptype(self):
        return ''

    @property
    def show_contents(self):
        return True

    @property
    def layers_active(self):
        return ''

    @property
    def search_active(self):
        return ''
