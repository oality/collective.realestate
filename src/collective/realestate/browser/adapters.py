# -*- coding: utf-8 -*-
from collective.realestate.utils import get_first_realestate_obj
from DateTime import DateTime
from ftw.calendar.browser.calendarupdateview import CalendarJSONSource
from ftw.calendar.browser.interfaces import IFtwCalendarJSONSourceProvider
from Products.CMFCore.utils import getToolByName
from zope.interface import implements


class RealEstateCalendarJSONSource(CalendarJSONSource):
    implements(IFtwCalendarJSONSourceProvider)

    def get_event_brains(self):
        args = {
            'start': {
                'query': DateTime(self.request.get('end')), 'range': 'max'},
            'end': {
                'query': DateTime(self.request.get('start')), 'range': 'min'}}

        catalog = getToolByName(self.context, 'portal_catalog')
        portal_calendar = getToolByName(self.context, 'portal_calendar',
                                        None)
        if portal_calendar:
            args['portal_type'] = portal_calendar.getCalendarTypes()
        return catalog(
            path={'depth': -1,
                  'query': '/'.join(
                    get_first_realestate_obj().getPhysicalPath())},
            **args
        )
