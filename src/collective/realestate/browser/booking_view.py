# -*- coding: utf-8 -*-

from collective.realestate import _
from collective.realestate.utils import get_first_realestate_obj
from plone import api
from Products.Five.browser import BrowserView


class BookingView(BrowserView):

    def __call__(self):
        self.msg = _(u'A small message')
        return self.index()

    def realestate_obj_form_url(self):
        obj = get_first_realestate_obj()
        if obj:
            return '{0}/booking-request'.format(obj.absolute_url())
        else:
            return api.portal.get().absolute_url()
