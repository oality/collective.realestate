# -*- coding: utf-8 -*-
from collective.realestate import _
from plone import api
from Products.Five.browser import BrowserView

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class RealEstateView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('real_estate_view.pt')

    def __call__(self):
        return self.index()

    def get_general_condition(self):
        key = 'collective.realestate.condition'
        text = api.portal.get_registry_record(key)
        import ipdb; ipdb.set_trace()
        return text
