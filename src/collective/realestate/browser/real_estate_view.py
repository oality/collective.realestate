# -*- coding: utf-8 -*-
from collective.realestate import _
from plone import api
from plone.formwidget.geolocation.widget import GeolocationWidget
from Products.Five.browser import BrowserView
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class RealEstateView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('real_estate_view.pt')

    def __call__(self):
        return self.index()

    def get_data_geojson(self):
        widget = GeolocationWidget(self.request)
        if not getattr(self.context, 'geolocation'):
            return ''
        widget.value = (
            self.context.geolocation.latitude,
            self.context.geolocation.longitude
        )
        widget.context = self.context
        return widget.data_geojson

    def get_geo_values(self):
        if not getattr(self.context, 'geolocation'):
            return ('', '')
        return (
            self.context.geolocation.latitude,
            self.context.geolocation.longitude
        )
